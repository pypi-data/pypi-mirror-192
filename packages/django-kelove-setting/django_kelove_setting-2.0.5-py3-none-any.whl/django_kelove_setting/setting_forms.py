"""
settings.py
By IT小强xqitw.cn <mail@xqitw.cn>
At 1/24/21 11:44 AM
"""

import json
from hashlib import md5
from asgiref.sync import sync_to_async

from django.db import ProgrammingError, OperationalError
from django.forms.models import ModelForm, model_to_dict
from django.forms.fields import CharField
from django.forms.widgets import HiddenInput
from django.conf import settings
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

from .models import Settings as SettingsModel

SETTINGS_CACHE_VERSION = 'DJANGO_KELOVE_SETTING_CACHE_VERSION'


class Settings(ModelForm):
    """
    配置表单基类
    """

    settings_title: str = _('未命名')

    settings_val = CharField(widget=HiddenInput(), required=False)

    fieldsets = ()

    def __init__(self, data=None, files=None, **kwargs):
        initial = kwargs.get('initial', {})
        instance = kwargs.get('instance', None)
        initial = {
            **initial,
            **self.init_form_initial(instance=instance)
        }
        for k, v in initial.items():
            setattr(instance, k, v)
        kwargs['initial'] = initial
        super().__init__(data=data, files=files, **kwargs)

    def clean(self):
        settings_val = self.get()
        for key, val in self.cleaned_data.items():
            if key != 'settings_val' and key in self.changed_data:
                settings_val[key] = val

        self.cleaned_data['settings_val'] = settings_val
        return super().clean()

    def init_form_data(self, data=None, instance=None):
        """
        初始化表单数据
        :param data:
        :param instance:
        :return:
        """

        # 表单数据已存在时，不做处理
        if data is not None:
            return data
        return self.init_form_initial(instance=instance)

    def init_form_initial(self, instance=None):
        """
        初始化表单初始值
        :param instance:
        :return:
        """

        data = {}

        if not instance:
            return data

        # 查询结果转为字典
        instance_data = model_to_dict(instance)

        # 循环处理配置值
        settings_val = instance_data.get('settings_val', {})
        if not settings_val:
            settings_val = {}
        if isinstance(settings_val, str):
            try:
                settings_val = json.loads(settings_val)
            except json.JSONDecodeError:
                settings_val = {}

        for field_name, field_info in self.base_fields.items():
            if field_name == 'settings_val':
                continue
            try:
                data[field_name] = settings_val.get(field_name, self.get_initial(field_info))
            except AttributeError:
                pass

        data['settings_key'] = instance_data['settings_key']
        data['settings_title'] = instance_data['settings_title']
        return data

    @classmethod
    def get_settings_key(cls):
        """
        获取当前配置类标识
        :return:
        """

        return '{module}.{name}'.format(
            module=cls.__module__,
            name=cls.__name__
        )

    @classmethod
    def get_settings_title(cls, is_full=True):
        """
        获取当前配置类名称
        :param is_full:
        :return:
        """

        if not is_full:
            return cls.settings_title
        return '{base_name}【{module}.{name}】'.format(
            base_name=cls.settings_title,
            module=cls.__module__,
            name=cls.__name__
        )

    @classmethod
    def get_cache_key(cls):
        """
        获取缓存标识
        :return:
        """

        return 'settings_{file}_{key}_cache'.format(
            file=md5(__file__.encode()).hexdigest(),
            key=md5(cls.get_settings_key().encode()).hexdigest()
        )

    @classmethod
    def delete_cache(cls):
        """
        删除缓存
        :return:
        """

        cache_key = cls.get_cache_key()
        cache.delete(cache_key, version=SETTINGS_CACHE_VERSION)

    @classmethod
    def get_form_db(cls) -> dict:
        """
        数据库中实时获取数据
        :return:
        """
        try:
            data = SettingsModel.objects.get(settings_key=cls.get_settings_key())
            data = data.settings_val
        except (SettingsModel.DoesNotExist, ProgrammingError, OperationalError):
            data = {}
        return data

    @classmethod
    def get_from_initial(cls):
        initial_data = {}
        for key, val in cls.base_fields.items():
            if key == 'settings_val':
                continue
            try:
                initial_data[key] = cls.get_initial(val)
            except AttributeError:
                pass
        return initial_data

    @classmethod
    def get(cls) -> dict:
        """
        获取配置
        :return:
        """
        initial_data = cls.get_from_initial()
        cache_version = SETTINGS_CACHE_VERSION
        cache_key = cls.get_cache_key()
        cache_data = cache.get(key=cache_key, default=None, version=cache_version)
        if cache_data is not None:
            return {**initial_data, **cache_data}
        cache_data = {**initial_data, **cls.get_form_db()}
        cache.set(key=cache_key, value=cache_data, timeout=3600 * 24 * 365, version=cache_version)
        return cache_data

    @classmethod
    def get_item(cls, key: str, default=None):
        """
        获取单个配置
        :param key:
        :param default:
        :return:
        """

        return cls.get().get(key, default)

    @classmethod
    @sync_to_async
    def aget(cls):
        return cls.get()

    @classmethod
    async def aget_item(cls, key: str, default=None):
        data = await cls.aget()
        return data.get(key, default)

    @classmethod
    def get_initial(cls, field):
        """
        获取初始值
        :param field:
        :return:
        """

        value = getattr(field, 'initial')
        if callable(value):
            value = value()
        return value

    @classmethod
    def get_initial_with_default(cls, field, default):
        """
        获取初始值，不存在时返回 default
        :param field:
        :param default:
        :return:
        """

        value = getattr(field, 'initial', default)
        if callable(value):
            value = value()
        return value

    @classmethod
    def change_django_settings(cls):
        """
        刷新django设置
        :return:
        """

        for key, val in cls.get().items():
            setattr(settings, key, val)

    def update_choices(self, field, value):
        """
        动态更新可选项
        :param field:
        :param value:
        :return:
        """
        self.fields[field].choices = value
        self.fields[field].widget.choices = value
        self.base_fields[field].choices = value
        self.base_fields[field].widget.choices = value

    def save(self, commit=True):
        self.delete_cache()
        return super().save(commit)

    @classmethod
    def get_fieldsets(cls, model_admin, request, obj=None):
        return cls.fieldsets

    class Meta:
        """
        Meta
        """

        model = SettingsModel
        fields = ['settings_val']

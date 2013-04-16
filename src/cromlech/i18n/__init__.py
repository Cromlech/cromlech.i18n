# -*- coding: utf-8 -*-

LOCALE_KEY = 'CROMLECH_I18N_LOCALE'
LOCALIZER_KEY = 'CROMLECH_I18N_LOCALIZER'

from crom.registry import Registry
i18n_registry = Registry()

from .interfaces import ILocale
from .utils import Language, getLanguage

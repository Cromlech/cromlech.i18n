# -*- coding: utf-8 -*-

LOCALE_KEY = 'CROMLECH_I18N_LOCALE'
LOCALIZER_KEY = 'CROMLECH_I18N_LOCALIZER'

from crom import Registry
i18n_registry = Registry()

from .interfaces import ILocalizer, ITranslationDirectory
from .utils import Language, getLanguage
from .translations import (load_translations_directories,
                           reload_translations_directories,
                           register_translations_directory)

# -*- coding: utf-8 -*-

LOCALE_KEY = 'CROMLECH_I18N_LOCALE'
LOCALIZER_KEY = 'CROMLECH_I18N_LOCALIZER'
COMPILE_MO_FILES_KEY = 'cromlech_compile_mo_files'

from crom import Registry
i18n_registry = Registry()

from .interfaces import ILanguage, ILocalizer, ITranslationDirectory
from .utils import Language, getLanguage
from .translations import (load_translations_directories,
                           reload_translations_directories,
                           register_translations_directory)

# -*- coding: utf-8 -*-

LOCALE_KEY = 'CROMLECH_I18N_LOCALE'
LOCALIZER_KEY = 'CROMLECH_I18N_LOCALIZER'
COMPILE_MO_FILES_KEY = 'cromlech_compile_mo_files'

from crom import Registry
i18n_registry = Registry()

from .interfaces import ILocale, ILanguage, ILocalizer, ITranslationDirectory
from .utils import setLocale, getLocale, getLocalizer, setLocalizer, translate
from .utils import accept_languages, get_environ_language, normalize_language
from .localize import get_localizer, make_localizer, Localizer
from .translations import (load_translations_directories,
                           reload_translations_directories,
                           register_translations_directory)


class Locale(object):

    def __init__(self, locale, localizer=None):
        self.locale = locale
        self.localizer = localizer

    def __enter__(self):
        setLocale(self.locale)
        if self.localizer is not None:
            setLocalizer(self.localizer)

    def __exit__(self, type, value, traceback):
        setLocale()
        setLocalizer()


class EnvironLocale(Locale):

    def __init__(self, environ, default='en_US'):
        self.locale = get_environ_language(environ) or default
        self.localizer = get_localizer(self.locale)

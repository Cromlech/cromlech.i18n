# -*- coding: utf-8 -*-

import threading
from . import LOCALE_KEY
from .interfaces import ILanguage
from cromlech.browser import IRequest
from zope.interface import ComponentLookupError


class LocaleSettings(threading.local):
    """Language resolution.
    """
    locale = None
    language = None


locale_settings = LocaleSettings()


def normalize_lang(lang):
    lang = lang.strip().lower()
    lang = lang.replace('_', '-')
    lang = lang.replace(' ', '')
    return lang


def resolveLocale(environ, default=None):
    return environ.get(LOCALE_KEY, default)


def setLocale(locale=None):
    locale_settings.locale = locale
    locale_settings.language = normalize_lang(locale)


def getLocale():
    return locale_settings.locale 


def getLanguage():
    return locale_settings.language


class Language(object):

    def __init__(self, language):
        setLanguage(language)

    def __enter__(self):
        return getLanguage()
        
    def __exit__(self, type, value, traceback):
        return setLanguage()

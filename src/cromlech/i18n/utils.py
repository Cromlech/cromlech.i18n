# -*- coding: utf-8 -*-

import re
import sys
import threading
from . import LOCALE_KEY, i18n_registry
from .interfaces import ILocalizer


class LocaleSettings(threading.local):
    """Language resolution.
    """
    locale = None
    localizer = None


locale_settings = LocaleSettings()


def persist_locale(environ, locale):
    environ[LOCALE_KEY] = locale


def resolve_locale(environ, default=None):
    return environ.get(LOCALE_KEY, default)


def query_localizer(locale, registry=i18n_registry, default=None):
    return ILocalizer.component(
        name=locale, lookup=i18n_registry, default=default)


def setLocalizer(localizer=None):
    locale_settings.localizer = localizer


def getLocalizer():
    return locale_settings.localizer


def setLocale(locale=None, registry):
    locale_settings.locale = locale
 

def getLocale():
    return locale_settings.locale


class Locale(object):

    def __init__(self, locale):
        locale = locale

    def __enter__(self):
        setLocale(self.locale)
        localizer = query_localizer(locale)
        setLocalizer(localizer)
        return self.locale

    def __exit__(self, type, value, traceback):
        setLocale()
        setLocalizer()


def accept_languages(browser_pref_langs):

    browser_pref_langs = browser_pref_langs.split(',')
    i = 0
    langs = []
    length = len(browser_pref_langs)

    for lang in browser_pref_langs:
        lang = lang.strip()
        if lang:
            l = lang.split(';', 2)
            quality = []
            if len(l) == 2:
                try:
                    q = l[1]
                    if q.startswith('q='):
                        q = q.split('=', 2)[1]
                        quality = float(q)
                except:
                    pass
            if quality == []:
                quality = float(length-i)
            language = l[0]
            langs.append((quality, language))
            if '-' in language:
                baselanguage = language.split('-')[0]
                langs.append((quality-0.001, baselanguage))
            i = i + 1

    # Sort and reverse it
    langs.sort()
    langs.reverse()

    # Filter quality string
    langs = map(lambda x: x[1], langs)
    return langs

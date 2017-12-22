# -*- coding: utf-8 -*-

import threading
from locale import normalize
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


def setLocale(locale=None):
    locale_settings.locale = locale


def getLocale():
    return locale_settings.locale


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
                quality = float(length - i)
            language = l[0]
            langs.append((quality, language))
            if '-' in language:
                baselanguage = language.split('-')[0]
                langs.append((quality - 0.001, baselanguage))
            i = i + 1

    # Sort and reverse it
    langs.sort()
    langs.reverse()

    # Filter quality string
    langs = map(lambda x: x[1], langs)
    return langs


def normalize_language(langcode):
    langcode = langcode.replace('-', '_')
    localename = normalize(langcode)
    if not '.' in localename:
        # This is not a valid or recognized language name
        return None, None
    return localename.split(".")


def normalized_lang(func):
    def normalize_locale(*args):
        lang = func(*args)
        if lang is not None:
            locale, encoding = normalize_language(lang)
            return locale
        return lang
    return normalize_locale


@normalized_lang
def get_environ_language(environ, restricted=None):

        def best_language(preferred):
            for lang in preferred:
                if lang in restricted:
                    return lang
            return None

        http_accepted = environ.get('HTTP_ACCEPT_LANGUAGE')
        if http_accepted:
            languages = accept_languages(http_accepted)
            if languages:
                languages = list(languages)
                if restricted:
                    return best_language(languages)
                return languages[0]
        return None


def translate(message, *args):
    localizer = getLocalizer()
    if localizer is None:
        return message
    return localizer.translate(message, *args)

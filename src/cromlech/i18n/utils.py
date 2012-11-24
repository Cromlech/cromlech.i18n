# -*- coding: utf-8 -*-

import threading
from . import LOCALE_KEY
from cromlech.browser import IRequest


class LocaleSettings(threading.local):
    """Language resolution.
    """
    language = None


locale_settings = LocaleSettings()


def setLanguage(lang=None):
    locale_settings.language = lang
  

def getLanguage():
    return locale_settings.language


class Language(object):

    def __init__(self, language):
        setLanguage(language)

    def __enter__(self):
        return getLanguage()
        
    def __exit__(self, type, value, traceback):
        return setLanguage()


def accept_languages(browser_pref_langs):

    browser_pref_langs = browser_pref_langs.split(',')
    i = 0
    langs = []
    length = len(browser_pref_langs)
 
    for lang in browser_pref_langs:
        lang = lang.strip().lower().replace('_', '-')
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

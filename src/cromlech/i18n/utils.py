# -*- coding: utf-8 -*-

import threading
from grokcore.component import adapter, implementer
from cromlech.browser import IRequest
from cromlech.i18n import ILanguage, IAllowedLanguages
from zope.component import queryUtility
from zope.i18n.config import ALLOWED_LANGUAGES
from zope.i18n.interfaces import INegotiator
from zope.component import getGlobalSiteManager


class Language(threading.local):
    """Language resolution.
    """
    prefered = None


language = Language()


def setLanguage(lang=None):
    """Sets the thread local language preference.
    """
    language.prefered = lang


def getLanguage():
    """Gets the thread local language preference.
    """
    return language.prefered


def negotiate(context, preferences=''):
    """This method returns a prefered language based on the allowed languages,
    and on the request, passed as 'context'. This could be a good idea to 
    """
    languages = queryUtility(IAllowedLanguages, name=preferences)
    if languages is None:
        languages = ALLOWED_LANGUAGES
    if languages is not None:
        negotiator = queryUtility(INegotiator)
        if negotiator is not None:
            return negotiator.getLanguage(languages, context)
    return None


@adapter(IRequest)
@implementer(ILanguage)
def HTTPRequestLanguage(request):
    """A specific implementation of an ILanguage resolver for IRequest.
    It uses a thread local object as a cache, for the request lifetime.
    If your preferences are context-dependant, please consider overriding
    this with your own implementation.
    """
    language = getLanguage()
    if language is None:
        language = negotiate(request)
        setLanguage(language)
    return language


def register_allowed_languages(languages, name='', registry=None):
    """This utilitarian method is only useful when setting up
    `IAllowedLanguages` as utilities. This is the out-of-the-box
    behavior. Make sure to use this method when you create your application
    to set up the global/root preferences for your i18n translations.
    """
    if registry is None:
        registry = getGlobalSiteManager()
    registry.registerUtility(frozenset(languages), IAllowedLanguages, name)

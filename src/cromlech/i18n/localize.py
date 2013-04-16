# -*- coding: utf-8 -*-

import os
import gettext

from translationstring import Translator, Pluralizer
from zope.interface import implementer

from .utils import getLocale, resolve_locale, normalize_lang
from .translations import Translations
from . import LOCALIZER_KEY, i18n_registry
from .interfaces import ILocalizer, ITranslationDirectory


@implementer(ILocalizer)
class Localizer(object):

    def __init__(self, locale_name, translations):
        self.locale_name = locale_name
        self.translations = translations
        self.pluralizer = None
        self.translator = None

    def translate(self, tstring, domain=None, mapping=None):
        if self.translator is None:
            self.translator = Translator(self.translations)
        return self.translator(
            tstring, domain=domain, mapping=mapping)

    def pluralize(self, singular, plural, n, domain=None, mapping=None):
        if self.pluralizer is None:
            self.pluralizer = Pluralizer(self.translations)
        return self.pluralizer(
            singular, plural, n, domain=domain, mapping=mapping)


def make_localizer(locale, translation_directories):
    """ Create a :class:`cromlech.i18n.localizer.Localizer` object
    corresponding to the provided locale name from the
    translations found in the list of translation directories."""
    translations = Translations()
    translations._catalog = {}

    if '_' in locale:
        locales_to_try = locale.split('_')[0], locale
    else:
        locales_to_try = (locale,)

    # intent: order locales left to right in least specific to most specific,
    # e.g. ['de', 'de_DE']. This services the intent of creating a
    # translations object that returns a "more specific" translation for a
    # region, but will fall back to a "less specific" translation for the
    # locale if necessary. Ordering from least specific to most specific
    # allows us to call translations.add in the below loop to get this
    # behavior.
    for tdir in translation_directories:
        locale_dirs = []
        for lname in locales_to_try:
            ldir = os.path.realpath(os.path.join(tdir, lname))
            if os.path.isdir(ldir):
                locale_dirs.append(ldir)

        for locale_dir in locale_dirs:
            messages_dir = os.path.join(locale_dir, 'LC_MESSAGES')
            if not os.path.isdir(os.path.realpath(messages_dir)):
                continue
            for mofile in os.listdir(messages_dir):
                mopath = os.path.realpath(os.path.join(messages_dir,
                                                       mofile))
                if mofile.endswith('.mo') and os.path.isfile(mopath):
                    with open(mopath, 'rb') as mofp:
                        domain = mofile[:-3]
                        dtrans = Translations(mofp, domain)
                        translations.add(dtrans)

    return Localizer(locale_name=locale, translations=translations)


def get_localizer(locale, registry=i18n_registry):
    localizer = ILocalizer.component(
        name=locale, default=None, lookup=registry)

    if localizer is None:
        tdirs = ITranslationDirectory.subscription(lookup=registry)
        localizer = make_localizer(locale, tdirs)
        i18n_registry.register(tuple(), ILocalizer, locale, localizer)

    return localizer


def get_environ_localizer(environ, registry=i18n_registry):

    localizer = environ.get(LOCALIZER_KEY)
    if localizer is None:
        locale = resolve_locale(environ, getLocale())
        if locale is None:
            raise NotImplementedError("Can't resolve a localizer")

        localizer = get_localizer(locale, registry)
        environ[LOCALIZER_KEY] = localizer

    return localizer

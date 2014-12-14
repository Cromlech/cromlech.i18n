# -*- coding: utf-8 -*-

import os
import sys
import gettext
from .interfaces import ITranslationDirectory
from . import i18n_registry
from pkg_resources import iter_entry_points

PY3 = sys.version_info[0] == 3
TEST_TRANSLATIONS_PATH = os.path.join(os.path.dirname(__file__), "locales")


class Translations(gettext.GNUTranslations, object):
    """An extended translation catalog class (ripped off from Babel) """

    DEFAULT_DOMAIN = 'messages'

    def __init__(self, fileobj=None, domain=DEFAULT_DOMAIN):
        """Initialize the translations catalog.

        :param fileobj: the file-like object the translation should be read
        from
        """
        # germanic plural by default; self.plural will be overwritten by
        # GNUTranslations._parse (called as a side effect if fileobj is
        # passed to GNUTranslations.__init__) with a "real" self.plural for
        # this domain; see https://github.com/Pylons/pyramid/issues/235
        self.plural = lambda n: int(n != 1)
        gettext.GNUTranslations.__init__(self, fp=fileobj)
        self.files = list(filter(None, [getattr(fileobj, 'name', None)]))
        self.domain = domain
        self._domains = {}

    @classmethod
    def load(cls, dirname=None, locales=None, domain=DEFAULT_DOMAIN):
        """Load translations from the given directory.

        :param dirname: the directory containing the ``MO`` files
        :param locales: the list of locales in order of preference (items in
        this list can be either `Locale` objects or locale
        strings)
        :param domain: the message domain
        :return: the loaded catalog, or a ``NullTranslations`` instance if no
        matching translations were found
        :rtype: `Translations`
        """
        if locales is not None:
            if not isinstance(locales, (list, tuple)):
                locales = [locales]
            locales = [str(l) for l in locales]
        if not domain:
            domain = cls.DEFAULT_DOMAIN
        filename = gettext.find(domain, dirname, locales)
        import pytest
        pytest.set_trace()
        if not filename:
            return gettext.NullTranslations()
        with open(filename, 'rb') as fp:
            return cls(fileobj=fp, domain=domain)

    def __repr__(self):
        return '<%s: "%s">' % (type(self).__name__,
                               self._info.get('project-id-version'))

    def add(self, translations, merge=True):
        """Add the given translations to the catalog.

        If the domain of the translations is different than that of the
        current catalog, they are added as a catalog that is only accessible
        by the various ``d*gettext`` functions.

        :param translations: the `Translations` instance with the messages to
        add
        :param merge: whether translations for message domains that have
        already been added should be merged with the existing
        translations
        :return: the `Translations` instance (``self``) so that `merge` calls
        can be easily chained
        :rtype: `Translations`
        """
        domain = getattr(translations, 'domain', self.DEFAULT_DOMAIN)
        if merge and domain == self.domain:
            return self.merge(translations)

        existing = self._domains.get(domain)
        if merge and existing is not None:
            existing.merge(translations)
        else:
            translations.add_fallback(self)
            self._domains[domain] = translations

        return self

    def merge(self, translations):
        """Merge the given translations into the catalog.

        Message translations in the specified catalog override any messages
        with the same identifier in the existing catalog.

        :param translations: the `Translations` instance with the messages to
        merge
        :return: the `Translations` instance (``self``) so that `merge` calls
        can be easily chained
        :rtype: `Translations`
        """
        if isinstance(translations, gettext.GNUTranslations):
            self._catalog.update(translations._catalog)
            if isinstance(translations, Translations):
                self.files.extend(translations.files)

        return self

    def dgettext(self, domain, message):
        """Like ``gettext()``, but look the message up in the specified
        domain.
        """
        return self._domains.get(domain, self).gettext(message)

    def ldgettext(self, domain, message):
        """Like ``lgettext()``, but look the message up in the specified
        domain.
        """
        return self._domains.get(domain, self).lgettext(message)

    def dugettext(self, domain, message):
        """Like ``ugettext()``, but look the message up in the specified
        domain.
        """
        if PY3:  # pragma: no cover
            return self._domains.get(domain, self).gettext(message)
        else:  # pragma: no cover
            return self._domains.get(domain, self).ugettext(message)

    def dngettext(self, domain, singular, plural, num):
        """Like ``ngettext()``, but look the message up in the specified
        domain.
        """
        return self._domains.get(domain, self).ngettext(singular, plural, num)

    def ldngettext(self, domain, singular, plural, num):
        """Like ``lngettext()``, but look the message up in the specified
        domain.
        """
        return self._domains.get(domain, self).lngettext(singular, plural, num)

    def dungettext(self, domain, singular, plural, num):
        """Like ``ungettext()`` but look the message up in the specified
        domain.
        """
        if PY3:   # pragma: no cover
            return self._domains.get(domain, self).ngettext(
                singular, plural, num)
        else:   # pragma: no cover
            return self._domains.get(domain, self).ungettext(
                singular, plural, num)


def register_translations_directory(path, registry=i18n_registry):
    i18n_registry.subscribe(tuple(), ITranslationDirectory, path)


def register_test_translations(registry=i18n_registry):
    register_translations_directory(TEST_TRANSLATIONS_PATH, registry)


def clean_test_translations_directory():
    """removes all the .mo - for test purposes
    """
    for root, dirs, files in os.walk(TEST_TRANSLATIONS_PATH):
        for filename in files:
            if filename.endswith('.mo'):
                path = os.path.join(root, filename)
                os.remove(path)


_loaded = False


def load_translations_directories(registry=i18n_registry):
    """Goes through all available components loaders and call them.
    """
    global _loaded
    if _loaded:
        return
    for loader_entry in iter_entry_points(
            'cromlech.i18n.translation_directory'):
        loader = loader_entry.load()
        if not callable(loader):
            raise TypeError(
                'Entry point %r should be a callable to register translations'
                % loader_entry.name)
        loader(registry)
    _loaded = True


def reload_translations_directories(registry=i18n_registry):
    """Reload all components.

    Mainly used by testing layers.
    """
    global _loaded
    _loaded = False
    load_translations_directories(registry)

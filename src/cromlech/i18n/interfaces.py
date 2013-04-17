# -*- coding: utf-8 -*-

from zope.interface import Interface


class ILanguage(Interface):
    """Interface representive a language name.
    """
    def __str__():
        """Returns the language as a string.
        """


class ILocalizer(Interface):
    """Returns the target locale to render translated elements.
    """
    def __str__():
        """Returns the locale code as a string.
        """

    def translate(tstring, domain, mapping):
        """
        """


class ITranslationDirectory(Interface):
    """
    """
    def __str__():
        """Returns the absolute path of the directory.
        """

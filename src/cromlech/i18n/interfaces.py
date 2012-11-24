# -*- coding: utf-8 -*-

from zope.interface import Interface


class ILocale(Interface):
    """Returns the target locale to render translated elements.
    """
    def __str__():
        """Returns a locale code as a string.
        """

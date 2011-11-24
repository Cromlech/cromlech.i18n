# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.interface.common.sequence import IReadSequence


class IAllowedLanguages(IReadSequence):
    """A configuration component used to restrain the available
    languages for the application. This represents an iterable of
    language codes strings.
    """


class ILanguage(Interface):
    """Returns the target language to render translated elements.
    The returns language is ought to be a member of the languages
    defined in a `IAllowedLanguages` component.
    """
    def __call__(context):
        """Returns a language code as a string. This must be a valid
        language, existing in the IAllowedLanguages (if available).
        eg. 'fr' or 'en'
        """

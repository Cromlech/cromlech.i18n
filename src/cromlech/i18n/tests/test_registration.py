# -*- coding: utf-8 -*-

import translationstring
import cromlech.i18n.localize
from cromlech.i18n import i18n_registry
from cromlech.i18n import load_translations_directories
from cromlech.i18n import ITranslationDirectory, ILocalizer
from cromlech.i18n.localize import create_localizer
from cromlech.i18n.translations import clean_test_translations_directory


def setup_module(module):
    load_translations_directories(i18n_registry, allow_tests=True)


def teardown_module(module):
    clean_test_translations_directory()


def test_localizer():

    brake = translationstring.TranslationString(
        'handbrake', domain='cromlech.i18n')

    tap = translationstring.TranslationString(
        'tap', domain='cromlech.i18n')

    # do not exist on fr_CA, should fallback on fr
    sir = translationstring.TranslationString(
        'sir', domain='cromlech.i18n')

    # No auto compiling
    frfr_localizer = create_localizer('fr_FR')
    assert frfr_localizer.translate(brake) == u'handbrake'

    # Auto compiling
    cromlech.i18n.localize.COMPILE_MO_FILES = True
    frfr_localizer = create_localizer('fr_FR')
    frca_localizer = create_localizer('fr_CA')
    
    assert frfr_localizer.translate(brake) == u'frein à main'
    assert frca_localizer.translate(brake) == u'brake à bras'

    assert frfr_localizer.translate(tap) == u'robinet'
    assert frca_localizer.translate(tap) == u'champlure'

    # Fallbacks: fr_CA will fallback on 'fr' if not found in fr_CA
    # The fr_CA is cut into a list like : fr, fr_CA,
    # ordered from least specific to more specific
    assert frca_localizer.translate(sir) == u'monsieur'

    # translation string do have a simple API
    # we can have a zope.i18nmessage
    from zope.i18nmessageid import MessageFactory
    _ = MessageFactory('cromlech.i18n')

    brake = _(u'handbrake')
    assert frfr_localizer.translate(brake) == u'frein à main'
    assert frca_localizer.translate(brake) == u'brake à bras'

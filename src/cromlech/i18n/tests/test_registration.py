# -*- coding: utf-8 -*-

import translationstring
from cromlech.i18n import i18n_registry
from cromlech.i18n import load_translations_directories
from cromlech.i18n import ITranslationDirectory, ILocalizer
from cromlech.i18n.localize import get_localizer


def setup_module(module):
    load_translations_directories(i18n_registry)


def teardown_module(module):
    pass


def test_all():
    assert list(ITranslationDirectory.subscription(lookup=i18n_registry))


def test_localizer():
    frfr_localizer = get_localizer('fr_FR')
    frca_localizer = get_localizer('fr_CA')
    assert frfr_localizer, frca_localizer

    brake = translationstring.TranslationString(
        'handbrake', domain='cromlech.i18n')

    tap = translationstring.TranslationString(
        'tap', domain='cromlech.i18n')

    # do not exist on fr_CA, should fallback on fr
    sir = translationstring.TranslationString(
        'sir', domain='cromlech.i18n')

    assert frfr_localizer.translate(brake) == u'frein à main'
    assert frca_localizer.translate(brake) == u'brake à bras'

    assert frfr_localizer.translate(tap) == u'robinet'
    assert frca_localizer.translate(tap) == u'champlure'

    assert frfr_localizer.translate(sir) == u'monsieur'
    assert frca_localizer.translate(sir) == u'monsieur'

    

# -*- coding: utf-8 -*-

from . import Locale
from .utils import get_environ_language


default = 'en'


def locale_settings(app, global_conf, allowed=default, default=default):

    allowed_langs = set((lang.strip() for lang in allowed.split(',')))

    def locale_filter(environ, start_response):
        language = get_environ_language(environ, restricted=allowed_langs)
        with Locale(language):
            return app(environ, start_response)

    return locale_filter

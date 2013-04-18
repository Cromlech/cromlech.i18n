# -*- coding: utf-8 -*-

from .utils import Locale, get_environ_language


default = 'en'


def locale_settings(app, global_conf, allowed=default, default=default):        

    allowed_langs = set((lang.strip() for lang in allowed.split(',')))

    def locale_filter(environ, start_response):
        language = get_environ_language(environ)
        with Locale(language):
            return app(environ, start_response)

    return locale_filter

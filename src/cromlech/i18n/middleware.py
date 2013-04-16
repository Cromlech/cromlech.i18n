# -*- coding: utf-8 -*-

from .utils import Language, accept_languages


default = 'en'


def locale_settings(app, global_conf, allowed=default, default=default):        

    allowed_langs = set((lang.strip() for lang in allowed.split(',')))

    def locale_filter(environ, start_response):

        def best_language(preferred):
            for lang in preferred:
                if lang in allowed_langs:
                    return lang
            return None

        preferred = accept_languages(environ['HTTP_ACCEPT_LANGUAGE'])
        language = best_language(preferred) or default
        with Language(language):
            return app(environ, start_response)

    return locale_filter

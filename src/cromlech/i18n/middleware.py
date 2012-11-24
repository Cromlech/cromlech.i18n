# -*- coding: utf-8 -*-

from .interfaces import ILocale


def locale_settings(app, global_conf, allowed, default):

    def locale_filter(environ, start_response):
        import pdb
        pdb.set_trace()
        return app(environ, start_response)
    
    return locale_filter

# -*- coding: utf-8 -*-

from . import domains_registry
from .interfaces import ITranslationDomain
from .domain import TranslationDomain


def register_domain(domain, name, registry=domains_registry):
    registry.register(tuple(), ITranslationDomain, name, domain)


def register_catalogs(catalogs, name, registry=domains_registry):
    domain = ITranslationDomain.component(
        name=name, lookup=registry, default=None)

    if domain is None:
        domain = TranslationDomain(name)
        register_domain(domain, name, registry)

    for catalog in catalogs:
        domain.addCatalog(catalog)
    # make sure we have a TEST catalog for each domain:
    domain.addCatalog(TestMessageCatalog(name))



def registerTranslations(_context, directory, domain='*'):
    path = os.path.normpath(directory)
    domains = {}

    loaded = False
    # Gettext has the domain-specific catalogs inside the language directory,
    # which is exactly the opposite as we need it. So create a dictionary that
    # reverses the nesting.
    for language in os.listdir(path):
        lc_messages_path = os.path.join(path, language, 'LC_MESSAGES')
        if os.path.isdir(lc_messages_path):
            # Preprocess files and update or compile the mo files
            if config.COMPILE_MO_FILES:
                for domain_path in glob(os.path.join(lc_messages_path,
                                                     '%s.po' % domain)):
                    domain_file = os.path.basename(domain_path)
                    name = domain_file[:-3]
                    compile_mo_file(name, lc_messages_path)
            for domain_path in glob(os.path.join(lc_messages_path,
                                                 '%s.mo' % domain)):
                loaded = True
                domain_file = os.path.basename(domain_path)
                name = domain_file[:-3]
                if not name in domains:
                    domains[name] = {}
                domains[name][language] = domain_path
    if loaded:
        logger.debug('register directory %s' % directory)

    # Now create TranslationDomain objects and add them as utilities
    for name, langs in domains.items():
        catalogs = []
        for lang, file in langs.items():
            catalogs.append(GettextMessageCatalog(lang, name, file))



        # register the necessary actions directly (as opposed to using
        # `zope.component.zcml.utility`) since we need the actual utilities
        # in place before the merging can be done...
        _context.action(
            discriminator = None,
            callable = handler,

            args = (catalogs, name))

    # also register the interface for the translation utilities
    domains_registry(

    provides = ITranslationDomain

    _context.action(
        discriminator = None,
        callable = provideInterface,
        args = (provides.__module__ + '.' + provides.getName(), provides))

domains_registry

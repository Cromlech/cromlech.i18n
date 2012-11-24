# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


version = '1.0-dev'

install_requires = [
    'setuptools',
    'zope.interface',
    'zope.i18nmessageid',
    'cromlech.browser >= 0.5',
    ]

tests_require = [
    ]

setup(name='cromlech.i18n',
      version=version,
      description="Localization handling for Cromlech.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='',
      license='ZPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['cromlech',],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      install_requires=install_requires,
      entry_points="""
      # -*- Entry points: -*-
      [paste.filter_app_factory]
      locale = cromlech.i18n.middleware:locale_settings
      """,
      )

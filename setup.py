# -*- coding: utf-8 -*-
"""Installer for the medialog.hilversum package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='medialog.hilversum',
    version='1.0a1',
    description="Contenttypes scripts and templates for Proloog",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone CMS',
    author='Espen Moe-Nilssen',
    author_email='espen@medialog.no',
    url='https://github.com/collective/medialog.hilversum',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/medialog.hilversum',
        'Source': 'https://github.com/collective/medialog.hilversum',
        'Tracker': 'https://github.com/collective/medialog.hilversum/issues',
        # 'Documentation': 'https://medialog.hilversum.readthedocs.io/en/latest/',
    },
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['medialog'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'pandas', 
        'numpy',
        'openpyxl',
        'chardet',
        'plone.api>=1.8.4',
        'plone.app.dexterity',
        'collective.collectionfilter',
        'medialog.magneticpopup',
        'medialog.controlpanel',
        'plone.app.jquery'
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing>=5.0.0',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = medialog.hilversum.locales.update:update_locale
    """,
)

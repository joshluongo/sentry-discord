#!/usr/bin/env python
"""
sentry-discord
============

An extension for `Discord <https://www.discordapp.com>`_ which creates Discord alerts.

:copyright: (c) 2015 by Sentry Team, see AUTHORS for more details.
:license: Apache 2.0, see LICENSE for more details.
"""
from setuptools import setup, find_packages


install_requires = [
    'sentry>=5.0.0',
]

setup(
    name='sentry-discord',
    version='0.2.0',
    author='Josh Luongo',
    author_email='josh@jrapps.com.au',
    url='https://github.com/joshluongo/sentry-discord',
    description='A Sentry extension which posts notifications to Discord (https://www.discordapp.com/).',
    long_description=open('README.rst').read(),
    license='Apache 2.0',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        'sentry.apps': [
            'sentry_discord = sentry_discord',
        ],
        'sentry.plugins': [
            'sentry_discord = sentry_discord.plugin:DiscordPlugin',
        ]
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)

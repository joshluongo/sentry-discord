from __future__ import absolute_import

try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('sentry-discord').version
except Exception, e:
    VERSION = 'unknown'

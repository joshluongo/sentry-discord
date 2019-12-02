"""
sentry_discord.plugin
~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2019 by Josh Luongo, see AUTHORS for more details.
:license: Apache 2.0, see LICENSE for more details.
"""
from __future__ import absolute_import

import logging
import sentry_discord

from django import forms
from django.utils.html import escape
from requests import HTTPError

from sentry import http
from sentry.plugins.bases import notify
from sentry.utils import json


class DiscordOptionsForm(notify.NotificationConfigurationForm):
    webhook_url = forms.CharField(
        max_length=255,
        label='Discord Webhook URL',
        widget=forms.TextInput(
            attrs={'class': 'span6', 'placeholder': 'e.g. https://discordapp.com/api/webhooks/x/x'}),
        help_text='You can get this under the channel options in Discord.',
        required=True,
    )


class DiscordPlugin(notify.NotificationPlugin):
    author = 'Josh Luongo'
    author_url = 'https://jrapps.com.au'
    resource_links = (
        ('Bug Tracker', 'https://github.com/joshluongo/sentry-discord/issues'),
        ('Source', 'https://github.com/joshluongo/sentry-discord'),
    )

    title = 'Discord'
    slug = 'discord'
    description = 'Create Discord alerts out of notifications.'
    conf_key = 'discord'
    version = sentry_discord.VERSION
    project_conf_form = DiscordOptionsForm

    logger = logging.getLogger('sentry.plugins.discord')

    def is_configured(self, project):
        return all((
            self.get_option(k, project)
            for k in ('webhook_url')
        ))

    def get_form_initial(self, project=None):
        return {
            'webhook_url': 'https://discordapp.com/api/webhooks/x/x',
        }

    def build_payload(self, group, event, triggering_rules):
        return {
            'content': event.message + '\n\n' + group.get_absolute_url(),
        }

    def notify_users(self, group, event, fail_silently=False, triggering_rules=None, **kwargs):
        if not self.is_configured(group.project):
            return

        webhook_url = self.get_option('webhook_url', group.project)

        payload = self.build_payload(group, event, triggering_rules)

        headers = {'Content-Type': 'application/json'}

        resp = http.safe_urlopen(webhook_url, json=payload, headers=headers)
        if not resp.ok:
            raise HTTPError(
                'Unsuccessful response from Discord: %s' % resp.json())

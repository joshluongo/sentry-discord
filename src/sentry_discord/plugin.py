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

LEVEL_TO_COLOR = {
    "debug": "cfd3da",
    "info": "2788ce",
    "warning": "f18500",
    "error": "f43f20",
    "fatal": "d20f2a",
}

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
        return bool(self.get_option("webhook_url", project))

    def get_form_initial(self, project=None):
        return {
            'webhook_url': 'https://discordapp.com/api/webhooks/x/x',
        }

    def color_for_event(self, event):
        return "#" + LEVEL_TO_COLOR.get(event.get_tag("level"), "error")

    def notify(self, notification):
        event = notification.event
        group = event.group
        project = group.project

        if not self.is_configured(project):
            return

        webhook = self.get_option("webhook_url", project)

        # Make it a slack comptaible webhook because im lazy.
        if not webhook.endswith("/slack"):
            webhook += "/slack"

        username = "Sentry"
        icon_url = ""
        channel = ""

        title = event.title.encode("utf-8")
        # TODO(dcramer): we'd like this to be the event culprit, but Sentry
        # does not currently retain it
        if group.culprit:
            culprit = group.culprit.encode("utf-8")
        else:
            culprit = None
        project_name = project.get_full_name().encode("utf-8")

        fields = []

        # They can be the same if there is no culprit
        # So we set culprit to an empty string instead of duplicating the text
        fields.append({"title": "Culprit", "value": culprit, "short": False})
        fields.append({"title": "Project", "value": project_name, "short": True})

        payload = {
            "attachments": [
                {
                    "fallback": "[%s] %s" % (project_name, title),
                    "title": title,
                    "title_link": group.get_absolute_url(params={"referrer": "slack"}),
                    "color": self.color_for_event(event),
                    "fields": fields,
                }
            ]
        }

        if username:
            payload["username"] = username.encode("utf-8")

        if channel:
            payload["channel"] = channel

        if icon_url:
            payload["icon_url"] = icon_url

        values = {"payload": json.dumps(payload)}

        # Apparently we've stored some bad data from before we used `URLField`.
        webhook = webhook.strip(" ")
        return http.safe_urlopen(webhook, method="POST", data=values, timeout=5)

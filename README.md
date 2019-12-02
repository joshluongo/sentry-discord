sentry-discord
===============

An extension for [Discord](https://www.discordapp.com/) which creates discord alerts our of Sentry events.

This is based on [sentry-opsgenie](https://github.com/getsentry/sentry-opsgenie) and the [legacy slack plugin](https://github.com/getsentry/sentry/blob/master/src/sentry_plugins/slack/plugin.py)

Install
-------

### Sentry >= 9.0
You will have to install the package via Git:

```
pip install https://github.com/joshluongo/sentry-discord/archive/master.zip
```

You can now configure alerts via the plugin configuration panel within your project.
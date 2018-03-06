# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


def make_many_uris(apps, schema_editor):
    Client = apps.get_model("oauth2app", "Client")
    for client in Client.objects.all():
        if client.redirect_uri:
            client.redirect_uris = [client.redirect_uri, ]
            client.save()


def rollback_many_uris(apps, schema_editor):
    Client = apps.get_model("oauth2app", "Client")
    for client in Client.objects.all():
        if client.redirect.uris:
            client.redirect_uri = client.redirect_uris[0]
            client.save()


class Migration(migrations.Migration):

    dependencies = [
        ('oauth2app', '0002_client_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='redirect_uris',
            field=jsonfield.fields.JSONField(null=True),
        ),
        migrations.RunPython(make_many_uris, rollback_many_uris),
        migrations.RemoveField(
            model_name='client',
            name='redirect_uri',
        ),
    ]

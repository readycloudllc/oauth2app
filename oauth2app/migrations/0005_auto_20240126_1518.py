# Generated by Django 2.2.17 on 2024-01-26 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth2app', '0004_auto_20190926_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='throttle_limit_get',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='throttle_limit_other',
            field=models.IntegerField(null=True),
        ),
    ]

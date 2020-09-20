# Generated by Django 3.0.8 on 2020-09-20 11:45

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0007_message_is_readed'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='words',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, null=True, size=10),
        ),
    ]

# Generated by Django 3.0.8 on 2020-09-06 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0010_rented_is_checked'),
    ]

    operations = [
        migrations.AddField(
            model_name='rented',
            name='is_canceled',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]

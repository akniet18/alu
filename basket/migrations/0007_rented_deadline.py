# Generated by Django 3.0.8 on 2020-08-26 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0006_auto_20200826_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='rented',
            name='deadline',
            field=models.DateField(blank=True, null=True),
        ),
    ]

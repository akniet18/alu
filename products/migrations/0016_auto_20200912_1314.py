# Generated by Django 3.0.8 on 2020-09-12 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20200912_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='leave',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='pickup',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]

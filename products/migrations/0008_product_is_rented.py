# Generated by Django 3.0.8 on 2020-08-23 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20200816_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_rented',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]

# Generated by Django 3.0.8 on 2020-09-12 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_product_in_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_14_owner',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='price_30_owner',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

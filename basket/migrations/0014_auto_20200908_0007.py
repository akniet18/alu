# Generated by Django 3.0.8 on 2020-09-07 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_product_count_day'),
        ('basket', '0013_auto_20200907_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rented',
            name='product',
            field=models.ManyToManyField(blank=True, related_name='rented_obj', to='products.Product'),
        ),
    ]
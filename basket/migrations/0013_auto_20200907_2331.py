# Generated by Django 3.0.8 on 2020-09-07 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_product_count_day'),
        ('basket', '0012_rented_get_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rented',
            old_name='count_day',
            new_name='amount',
        ),
        migrations.RemoveField(
            model_name='rented',
            name='product',
        ),
        migrations.AddField(
            model_name='rented',
            name='product',
            field=models.ManyToManyField(blank=True, to='products.Product'),
        ),
    ]

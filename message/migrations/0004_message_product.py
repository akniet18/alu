# Generated by Django 3.0.8 on 2020-09-09 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_product_count_day'),
        ('message', '0003_message_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Product'),
        ),
    ]

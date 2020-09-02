# Generated by Django 3.0.8 on 2020-08-16 09:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0004_auto_20200811_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rented',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_day', models.IntegerField()),
                ('rented_day', models.DateTimeField(auto_now_add=True)),
                ('get_product', models.SmallIntegerField(blank=True, choices=[(1, 'Достовка'), (2, 'Самовывоз')], null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rented_product', to='products.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='i_rent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basket_product', to='products.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_basket', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
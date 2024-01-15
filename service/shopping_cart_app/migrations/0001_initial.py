# Generated by Django 4.2.7 on 2024-01-08 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CartProductRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('product_cost', models.PositiveIntegerField(null=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='shopping_cart_app.cart')),
            ],
        ),
    ]

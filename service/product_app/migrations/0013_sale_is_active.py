# Generated by Django 4.2.7 on 2024-01-20 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0012_alter_category_managers_sale_expire_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
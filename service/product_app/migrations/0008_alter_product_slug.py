# Generated by Django 4.2.7 on 2024-01-16 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0007_alter_category_sub_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='django-db-models-fields-charfield', unique=True),
        ),
    ]
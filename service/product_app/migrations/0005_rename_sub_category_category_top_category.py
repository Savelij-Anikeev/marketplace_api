# Generated by Django 4.2.7 on 2024-01-15 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0004_alter_category_sub_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='sub_category',
            new_name='top_category',
        ),
    ]

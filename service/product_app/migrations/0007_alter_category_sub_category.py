# Generated by Django 4.2.7 on 2024-01-16 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0006_remove_category_top_category_category_sub_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='sub_category',
            field=models.ManyToManyField(blank=True, null=True, to='product_app.category'),
        ),
    ]

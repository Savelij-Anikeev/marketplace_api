# Generated by Django 4.2.7 on 2024-01-15 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0003_alter_product_options_category_sub_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product_app.category'),
        ),
    ]

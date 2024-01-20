# Generated by Django 4.2.7 on 2024-01-20 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0014_alter_product_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sale',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='products', to='product_app.sale'),
        ),
    ]
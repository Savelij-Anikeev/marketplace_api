# Generated by Django 4.2.7 on 2024-01-09 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]

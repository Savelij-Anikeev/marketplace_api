# Generated by Django 4.2.7 on 2024-01-15 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0008_rename_content_type_1_userpostrelation_content_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('default', 'default'), ('vendor_staff', 'vendor_staff'), ('vendor_manager', 'vendor_manager')], default='default', max_length=24),
        ),
    ]

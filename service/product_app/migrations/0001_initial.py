# Generated by Django 4.2.7 on 2024-01-08 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_actions_app', '0001_initial'),
        ('vendor_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('basepost_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='user_actions_app.basepost')),
                ('name', models.CharField(max_length=128)),
            ],
            bases=('user_actions_app.basepost', models.Model),
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('basepost_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='user_actions_app.basepost')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=1024)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=100)),
                ('final_cost', models.DecimalField(decimal_places=2, default=0, max_digits=100)),
                ('amount', models.PositiveIntegerField(default=0)),
                ('specs', models.JSONField(null=True)),
                ('tags', models.CharField(blank=True, max_length=256, null=True)),
                ('slug', models.SlugField(default='django-db-models-fields-charfield')),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.category')),
                ('sale', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='product_app.sale')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor_app.vendor')),
            ],
            bases=('user_actions_app.basepost', models.Model),
        ),
    ]

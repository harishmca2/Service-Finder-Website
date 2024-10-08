# Generated by Django 5.0.3 on 2024-06-03 20:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=15, null=True)),
                ('image', models.FileField(null=True, upload_to='')),
                ('gender', models.CharField(max_length=15, null=True)),
                ('type', models.CharField(max_length=15, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=15, null=True)),
                ('image', models.FileField(null=True, upload_to='')),
                ('gender', models.CharField(max_length=15, null=True)),
                ('type', models.CharField(max_length=15, null=True)),
                ('status', models.CharField(max_length=15, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=15, null=True)),
                ('experience', models.CharField(max_length=15, null=True)),
                ('location', models.CharField(max_length=150, null=True)),
                ('description', models.CharField(max_length=200, null=True)),
                ('provider', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='servicefinder.provider')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apply_date', models.DateField(null=True)),
                ('status', models.CharField(max_length=20, null=True)),
                ('statu', models.CharField(max_length=20, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='servicefinder.customeruser')),
                ('serviceman', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='servicefinder.provider')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='servicefinder.service')),
            ],
        ),
    ]

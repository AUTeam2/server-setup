# Generated by Django 2.2.8 on 2019-12-16 07:18

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_module', '0004_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inbound_payload', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
    ]

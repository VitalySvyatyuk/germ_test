# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-11 12:26
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='image_list',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(blank=True), size=None),
        ),
    ]
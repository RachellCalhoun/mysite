# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-23 10:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_skills'),
    ]

    operations = [
        migrations.RenameField(
            model_name='skills',
            old_name='skill',
            new_name='title',
        ),
    ]

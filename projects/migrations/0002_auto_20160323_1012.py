# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-23 10:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='description',
            new_name='text',
        ),
    ]

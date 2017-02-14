# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mycmd', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saltuserfile',
            name='salt_host',
        ),
        migrations.RemoveField(
            model_name='saltuserfile',
            name='update_dir',
        ),
    ]

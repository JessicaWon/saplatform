# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CloudServerStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('update_time', models.DateTimeField(default=datetime.datetime.now)),
                ('server_ip', models.CharField(max_length=60)),
                ('server_status', models.CharField(max_length=60)),
                ('server_status_reason', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='GameServer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(default=datetime.datetime.now)),
                ('update_time', models.DateTimeField(default=datetime.datetime.now)),
                ('engineer_name', models.CharField(max_length=60)),
                ('project_name', models.CharField(max_length=60)),
                ('gameserver_id', models.CharField(max_length=60)),
                ('project_dir', models.CharField(max_length=60)),
                ('cloud_server_eth0_ip', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='SaltUpdateFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(default=datetime.datetime.now)),
                ('update_time', models.DateTimeField(default=datetime.datetime.now)),
                ('engineer_name', models.CharField(max_length=60)),
                ('upload_file', models.FileField(upload_to=b'./upload/')),
                ('update_dir', models.CharField(max_length=60)),
                ('project_name', models.CharField(max_length=60)),
                ('project_dir', models.CharField(max_length=60)),
                ('salt_command', models.CharField(max_length=60)),
                ('salt_selected_gameserver', models.CharField(max_length=60)),
                ('salt_outcome', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='SaltUserFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(default=datetime.datetime.now)),
                ('update_time', models.DateTimeField(default=datetime.datetime.now)),
                ('upload_file', models.FileField(upload_to=b'./upload/')),
                ('update_dir', models.CharField(max_length=60)),
                ('salt_command', models.CharField(max_length=50)),
                ('salt_host', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='userCmd',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('u_cmd', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='userFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('f_title', models.CharField(max_length=30)),
                ('u_file', models.FileField(upload_to=b'./upload/')),
            ],
        ),
        migrations.CreateModel(
            name='userHost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('u_host', models.CharField(max_length=50)),
            ],
        ),
    ]

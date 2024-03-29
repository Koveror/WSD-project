# Generated by Django 2.1.5 on 2019-02-12 07:21

from django.db import migrations
from django.contrib.auth.models import Group

def make_developer_group(apps, schema_editor):
    developer_group = Group(name="Developer")
    developer_group.save()

class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0008_auto_20190208_1151'),
    ]

    operations = [
        migrations.RunPython(make_developer_group),
    ]

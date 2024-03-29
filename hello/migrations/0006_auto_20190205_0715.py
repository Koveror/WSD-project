# Generated by Django 2.1.5 on 2019-02-05 07:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0005_auto_20190201_1355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchases',
            name='id',
        ),
        migrations.AddField(
            model_name='purchases',
            name='pid',
            field=models.IntegerField(default=None, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='gameid',
            field=models.IntegerField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True),
        ),
    ]

# Generated by Django 2.1.5 on 2019-02-01 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0004_game_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='genre',
            new_name='primarygenre',
        ),
        migrations.AddField(
            model_name='game',
            name='secondarygenre',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]

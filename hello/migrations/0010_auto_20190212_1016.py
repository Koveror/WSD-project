# Generated by Django 2.1.5 on 2019-02-12 08:16

from django.db import migrations, models
import hello.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0009_add_developer_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='gameid',
            field=models.CharField(default=uuid.uuid4, max_length=200, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='numberSold',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[hello.models.validate_positive]),
        ),
        migrations.AlterField(
            model_name='score',
            name='score',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[hello.models.validate_positive]),
        ),
    ]
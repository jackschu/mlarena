# Generated by Django 2.2 on 2019-04-13 05:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='description',
            new_name='desc',
        ),
    ]

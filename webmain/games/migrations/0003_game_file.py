# Generated by Django 2.2 on 2019-04-13 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_auto_20190413_0525'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='file',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]

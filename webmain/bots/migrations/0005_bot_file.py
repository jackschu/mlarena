# Generated by Django 2.2 on 2019-04-13 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0004_bot_last_played'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot',
            name='file',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]

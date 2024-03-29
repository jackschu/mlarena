# Generated by Django 2.1.5 on 2019-04-14 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0006_merge_20190414_0350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matchrecord',
            name='did_bot1_win',
        ),
        migrations.AddField(
            model_name='matchrecord',
            name='winner_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='game',
            name='game_file',
            field=models.FileField(null=True, upload_to='games/files/'),
        ),
        migrations.AlterField(
            model_name='game',
            name='renderer_file',
            field=models.FileField(null=True, upload_to='games/files/'),
        ),
    ]

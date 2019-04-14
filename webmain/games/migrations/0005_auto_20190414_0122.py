# Generated by Django 2.1.5 on 2019-04-14 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_auto_20190413_0815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='bot1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bot1', to='bots.Bot'),
        ),
        migrations.AlterField(
            model_name='match',
            name='bot2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bot2', to='bots.Bot'),
        ),
        migrations.AlterField(
            model_name='match',
            name='game',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='games.Game'),
        ),
    ]

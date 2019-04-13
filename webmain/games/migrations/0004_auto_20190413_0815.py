# Generated by Django 2.1.5 on 2019-04-13 08:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0003_bot_games_played'),
        ('games', '0003_game_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameFrame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frame_num', models.IntegerField()),
                ('state', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('bot1', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bot1', to='bots.Bot')),
                ('bot2', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bot2', to='bots.Bot')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='games.Game')),
            ],
        ),
        migrations.CreateModel(
            name='MatchRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('did_bot1_win', models.BooleanField()),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.Match')),
            ],
        ),
        migrations.AddField(
            model_name='gameframe',
            name='match_record',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.MatchRecord'),
        ),
    ]
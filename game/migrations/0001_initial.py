# Generated by Django 2.2 on 2020-11-24 23:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import read_statistic.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GameType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('introduction', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('lastupdate_time', models.DateTimeField(auto_now=True)),
                ('price', models.FloatField()),
                ('avatar', models.ImageField(upload_to='')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('game_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='game.GameType')),
            ],
            options={
                'ordering': ['-create_time'],
            },
            bases=(models.Model, read_statistic.models.ReadNum_Expand),
        ),
    ]

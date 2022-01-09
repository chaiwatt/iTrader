# Generated by Django 4.0 on 2022-01-09 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BackTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol_id', models.CharField(max_length=200)),
                ('timeframe_id', models.CharField(max_length=200)),
                ('startbar', models.CharField(max_length=200)),
                ('barrange', models.CharField(max_length=200)),
                ('internal', models.CharField(max_length=200)),
                ('testtime', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'back_tests',
            },
        ),
        migrations.CreateModel(
            name='CurrentView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol_id', models.CharField(max_length=200)),
                ('timeframe_id', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'current_views',
            },
        ),
        migrations.CreateModel(
            name='Symbol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('broker', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=1)),
            ],
            options={
                'db_table': 'symbols',
            },
        ),
        migrations.CreateModel(
            name='SymbolData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol_id', models.CharField(max_length=200)),
                ('timeframe_id', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'symbol_datas',
            },
        ),
        migrations.CreateModel(
            name='TimeFrame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'time_frames',
            },
        ),
    ]

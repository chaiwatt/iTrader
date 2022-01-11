# Generated by Django 4.0 on 2022-01-11 04:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BackTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'back_tests',
            },
        ),
        migrations.CreateModel(
            name='BackTestInterval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interval', models.IntegerField()),
            ],
            options={
                'db_table': 'backtest_interval',
            },
        ),
        migrations.CreateModel(
            name='BackTestSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.IntegerField()),
            ],
            options={
                'db_table': 'backtest_sizes',
            },
        ),
        migrations.CreateModel(
            name='Broker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'brokers',
            },
        ),
        migrations.CreateModel(
            name='MyAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('server', models.CharField(max_length=100)),
                ('account_type', models.CharField(max_length=1)),
                ('broker', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='chart.broker')),
            ],
            options={
                'db_table': 'my_accounts',
            },
        ),
        migrations.CreateModel(
            name='Symbol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=1)),
                ('broker', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='chart.broker')),
            ],
            options={
                'db_table': 'symbols',
            },
        ),
        migrations.CreateModel(
            name='TimeFrame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'time_frames',
            },
        ),
        migrations.CreateModel(
            name='SymbolData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='chart.symbol')),
                ('timeframe', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='chart.timeframe')),
            ],
            options={
                'db_table': 'symbol_datas',
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myaccount', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='chart.myaccount')),
            ],
            options={
                'db_table': 'settings',
            },
        ),
        migrations.CreateModel(
            name='CurrentView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='chart.symbol')),
                ('timeframe', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='chart.timeframe')),
            ],
            options={
                'db_table': 'current_views',
            },
        ),
        migrations.CreateModel(
            name='BackTestSymbol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('backtest', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='chart.backtest')),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='chart.symbol')),
            ],
            options={
                'db_table': 'back_test_symbols',
            },
        ),
        migrations.CreateModel(
            name='BackTestOHLC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('open', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('close', models.FloatField()),
                ('tick', models.FloatField()),
                ('backtest', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='chart.backtest')),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='chart.symbol')),
            ],
            options={
                'db_table': 'back_test_ohlcs',
            },
        ),
        migrations.AddField(
            model_name='backtest',
            name='backtestsize',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='chart.backtestsize'),
        ),
        migrations.AddField(
            model_name='backtest',
            name='interval',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='chart.backtestinterval'),
        ),
        migrations.AddField(
            model_name='backtest',
            name='timeframe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='chart.timeframe'),
        ),
    ]

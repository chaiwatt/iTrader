# Generated by Django 4.0.1 on 2022-02-03 10:27

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
                ('symbolname', models.CharField(default=None, max_length=100)),
                ('timeframename', models.CharField(default=None, max_length=100)),
                ('status', models.CharField(default=0, max_length=1)),
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
                ('broker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chart.broker')),
            ],
            options={
                'db_table': 'my_accounts',
            },
        ),
        migrations.CreateModel(
            name='SearchType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trend', models.CharField(default=1, max_length=1)),
                ('pattern', models.CharField(default=0, max_length=1)),
            ],
            options={
                'db_table': 'search_types',
            },
        ),
        migrations.CreateModel(
            name='Symbol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=1)),
                ('broker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chart.broker')),
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
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chart.symbol')),
                ('timeframe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chart.timeframe')),
            ],
            options={
                'db_table': 'symbol_datas',
            },
        ),
        migrations.CreateModel(
            name='StdBarSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbolname', models.CharField(default=None, max_length=100)),
                ('timeframe', models.CharField(default=None, max_length=10)),
                ('value', models.FloatField(max_length=15, null=True)),
                ('stoplostpip', models.IntegerField(default=20)),
                ('stoplostpercent', models.FloatField(default=0.015)),
                ('lotsizeoffset', models.FloatField(default=1)),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chart.symbol')),
            ],
            options={
                'db_table': 'std_bar_sizes',
            },
        ),
        migrations.CreateModel(
            name='Spec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('parameter', models.CharField(max_length=100)),
                ('entry_value', models.CharField(max_length=20)),
                ('exit_value', models.CharField(max_length=20)),
                ('parameter_type', models.CharField(max_length=20)),
                ('compare_reverse', models.CharField(default=1, max_length=1)),
                ('status', models.CharField(default=1, max_length=1)),
                ('spec_type', models.CharField(default=1, max_length=1)),
                ('order_type', models.CharField(default=0, max_length=1)),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chart.symbol')),
            ],
            options={
                'db_table': 'specs',
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reportsymbolsort', models.CharField(default=1, max_length=1)),
                ('firstfoundstatus', models.CharField(default=1, max_length=1)),
                ('demobalance', models.FloatField(default=1000)),
                ('spreadlimit', models.IntegerField(default=15)),
                ('spreadpricelimit', models.FloatField(default=20)),
                ('stoplostpip', models.IntegerField(default=20)),
                ('stoplostpercent', models.FloatField(default=0.015)),
                ('myaccount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chart.myaccount')),
            ],
            options={
                'db_table': 'settings',
            },
        ),
        migrations.CreateModel(
            name='SearchReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_type', models.CharField(default=None, max_length=100)),
                ('symbolname', models.CharField(default=None, max_length=10)),
                ('timeframename', models.CharField(default=None, max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chart.symbol')),
                ('timeframe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chart.timeframe')),
            ],
            options={
                'db_table': 'search_reports',
            },
        ),
        migrations.CreateModel(
            name='LotSizeFactor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeframename', models.CharField(max_length=10)),
                ('factor', models.FloatField(default=1)),
                ('timeframe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chart.timeframe')),
            ],
            options={
                'db_table': 'lot_size_factors',
            },
        ),
        migrations.CreateModel(
            name='CurrentView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chart.symbol')),
                ('timeframe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chart.timeframe')),
            ],
            options={
                'db_table': 'current_views',
            },
        ),
        migrations.CreateModel(
            name='BackTestOHLCTimeframe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeframename', models.CharField(default=None, max_length=100)),
                ('date', models.DateTimeField()),
                ('open', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('close', models.FloatField()),
                ('tick', models.FloatField()),
                ('backtest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chart.backtest')),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chart.symbol')),
                ('timeframe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chart.timeframe')),
            ],
            options={
                'db_table': 'back_test_ohlc_timeframes',
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
                ('backtest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chart.backtest')),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chart.symbol')),
            ],
            options={
                'db_table': 'back_test_ohlcs',
            },
        ),
        migrations.AddField(
            model_name='backtest',
            name='backtestsize',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chart.backtestsize'),
        ),
        migrations.AddField(
            model_name='backtest',
            name='interval',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chart.backtestinterval'),
        ),
        migrations.AddField(
            model_name='backtest',
            name='symbol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chart.symbol'),
        ),
        migrations.AddField(
            model_name='backtest',
            name='timeframe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chart.timeframe'),
        ),
    ]

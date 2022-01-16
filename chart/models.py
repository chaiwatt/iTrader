from django.db import models
# from django_unixdatetimefield import UnixDateTimeField

class Broker(models.Model):
    name=models.CharField(max_length=50)
    class Meta:
        db_table = "brokers" 

class MyAccount(models.Model):
    broker=models.ForeignKey(Broker, on_delete=models.CASCADE)
    login=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    server=models.CharField(max_length=100)
    account_type=models.CharField(max_length=1)
    class Meta:
        db_table = "my_accounts" 

class Setting(models.Model):
    myaccount=models.ForeignKey(MyAccount, on_delete=models.CASCADE)
    class Meta:
        db_table = "settings" 

class TimeFrame(models.Model):
    name=models.CharField(max_length=10)
    class Meta:
        db_table = "time_frames" 

class Symbol(models.Model):
    broker=models.ForeignKey(Broker, on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    status=models.CharField(max_length=1)
    class Meta:
        db_table = "symbols"

class BackTestInterval(models.Model):
    interval=models.IntegerField()
    class Meta:  
        db_table = "backtest_interval"         

class SymbolData(models.Model):
    symbol=models.ForeignKey(Symbol, on_delete=models.CASCADE)
    timeframe=models.ForeignKey(TimeFrame, on_delete=models.CASCADE)
    class Meta:
        db_table = "symbol_datas"

class CurrentView(models.Model):
    symbol=models.ForeignKey(Symbol, on_delete=models.CASCADE)
    timeframe=models.ForeignKey(TimeFrame, on_delete=models.CASCADE)
    class Meta:
        db_table = "current_views"

class BackTestSize(models.Model):
    size=models.IntegerField()
    class Meta:
        db_table = "backtest_sizes"

class BackTest(models.Model):
    code=models.CharField(max_length=100)
    symbolname=models.CharField(max_length=100, default = None)
    symbol=models.ForeignKey(Symbol, on_delete=models.CASCADE)
    timeframe=models.ForeignKey(TimeFrame, on_delete=models.CASCADE)
    timeframename=models.CharField(max_length=100, default = None)
    backtestsize=models.ForeignKey(BackTestSize, on_delete=models.CASCADE)
    interval=models.ForeignKey(BackTestInterval, on_delete=models.CASCADE)
    status=models.CharField(max_length=1, default = 0)
    class Meta:
        db_table = "back_tests"

# class BackTestSymbol(models.Model):
#     backtest=models.ForeignKey(BackTest, on_delete=models.CASCADE)
#     symbol=models.ForeignKey(Symbol, on_delete=models.CASCADE)
#     class Meta:  
#         db_table = "back_test_symbols"

class BackTestOHLC(models.Model):
    backtest=models.ForeignKey(BackTest, on_delete=models.CASCADE)
    symbol=models.ForeignKey(Symbol, on_delete=models.CASCADE)
    date=models.DateTimeField()
    open=models.FloatField()
    high=models.FloatField()
    low=models.FloatField()
    close=models.FloatField()
    tick=models.FloatField()
    class Meta:
        db_table = "back_test_ohlcs"


class TestSpec(models.Model):
    spec_type=models.CharField(max_length=10)
    aligator_trend=models.CharField(max_length=10)
    ma5_slope=models.FloatField()
    ma5_std=models.FloatField()
    ma8_slope=models.FloatField()
    ma8_std=models.FloatField()
    ma13_slope=models.FloatField()
    ma13_std=models.FloatField()
    ma100_slope=models.FloatField()
    ma100_arrow_above=models.BooleanField(default=False)
    ma100_arrow_below=models.BooleanField(default=True)
    macd_cross=models.CharField(max_length=10)
    macd_trend=models.CharField(max_length=10)
    rsi=models.FloatField()
    ma8_percent_diff_ma5=models.FloatField()
    ma8_percent_diff_ma13=models.FloatField()
    ssma3line_uptrend=models.BooleanField(default=True)
    ssma3line_downtrend=models.BooleanField(default=False)
    class Meta:
        db_table = "test_specs"

        
class Spec(models.Model):
    parameter=models.CharField(max_length=10)
    value=models.CharField(max_length=10)
    parameter_type=models.CharField(max_length=10)
    class Meta:
        db_table = "specs"


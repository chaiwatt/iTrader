from django.db import models
from django_unixdatetimefield import UnixDateTimeField

class TimeFrame(models.Model):
    name=models.CharField(max_length=200)
    class Meta:  
        db_table = "time_frames" 

class Symbol(models.Model):
    name=models.CharField(max_length=200)
    broker=models.CharField(max_length=200)
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
    timeframe=models.ForeignKey(TimeFrame, on_delete=models.CASCADE)
    backtestsize=models.ForeignKey(BackTestSize, on_delete=models.CASCADE)
    interval=models.ForeignKey(BackTestInterval, on_delete=models.CASCADE)
    class Meta:  
        db_table = "back_tests"      

class BackTestSymbol(models.Model):
    backtest=models.ForeignKey(BackTest, on_delete=models.CASCADE)
    symbol=models.ForeignKey(Symbol, on_delete=models.CASCADE)
    class Meta:  
        db_table = "back_test_symbols"         

class BackTestOHLC(models.Model):
    symbol=models.ForeignKey(Symbol, on_delete=models.CASCADE)
    date=models.DateTimeField()
    open=models.FloatField()
    high=models.FloatField()
    low=models.FloatField()
    close=models.FloatField()
    tick=models.FloatField()
    class Meta:  
        db_table = "back_test_ohlcs"         
 
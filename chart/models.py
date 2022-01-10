from django.db import models

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
    interval=models.IntegerField()
    class Meta:  
        db_table = "back_tests"      

class BackTestSymbol(models.Model):
    backtest=models.ForeignKey(BackTest, on_delete=models.CASCADE)
    symbol=models.ForeignKey(Symbol, on_delete=models.CASCADE)
    class Meta:  
        db_table = "back_test_symbols"              
 
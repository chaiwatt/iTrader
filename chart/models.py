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
    symbol_id=models.CharField(max_length=200)
    timeframe_id=models.CharField(max_length=200)
    class Meta:  
        db_table = "symbol_datas" 

class CurrentView(models.Model):
    symbol_id=models.CharField(max_length=200)
    timeframe_id=models.CharField(max_length=200)

    class Meta:  
        db_table = "current_views"

class BackTest(models.Model):
    symbol_id=models.CharField(max_length=200)
    timeframe_id=models.CharField(max_length=200)
    startbar=models.CharField(max_length=200)
    barrange=models.CharField(max_length=200)
    interval=models.CharField(max_length=200)

    class Meta:  
        db_table = "back_tests"        

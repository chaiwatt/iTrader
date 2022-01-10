from django.shortcuts import render,redirect
from datetime import datetime
import pandas as pd
import MetaTrader5 as mt5
from django.http import JsonResponse
from json import dumps
from .models import CurrentView,Symbol,TimeFrame,BackTest,BackTestSize,BackTestSymbol,BackTestInterval,BackTestOHLC
import requests
symbol = 'USDJPY'
#symbol = 'EURUSD'
timeframe = 'M1';
dataframe = mt5.TIMEFRAME_M1

login = 25006371
password = 'g(gpG4/hO%Z@'
server = 'demo.mt5tickmill.com'

# Create your views here.
def index(request):
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    mt5.login(login,password,server)

    account_info = mt5.account_info()
    # print(account_info)

    currentview = CurrentView.objects.first()
    tf = TimeFrame.objects.get(id = currentview.timeframe_id)
    timeframe = tf.name
    dataframe = getattr(mt5, f'TIMEFRAME_{timeframe}')
    _symbol = Symbol.objects.get(id = currentview.symbol_id)
    symbol = _symbol.name
    
    symbol_price = mt5.symbol_info_tick(symbol)._asdict()
    
    ohlc_data = pd.DataFrame(mt5.copy_rates_from_pos(symbol, dataframe, 0, 500))
    ohlc_data['time']=pd.to_datetime(ohlc_data['time'], unit='s')
    ohlcs = []
    for i, data in ohlc_data.iterrows():
        ohlc = {
            'time':data['time'].strftime('%Y-%m-%d %H:%M:%S'),
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume']
        }
        ohlcs.append(ohlc)

    data = {
        'symbol':symbol,
        'series':ohlcs, 
        'price': 
        {
            'ask':symbol_price['ask'],
            'bid':symbol_price['bid'],
            'timeframe':timeframe
        }
    }

    data = dumps(data)
    return render(request,'index.html',{
        'resData': data,
        'symbols':Symbol.objects.filter(status="1"),
        'timeframes':TimeFrame.objects.all(),
        'currentview':currentview
    })

def getohlc(request):  
    currentview = CurrentView.objects.first()
    tf = TimeFrame.objects.get(id = currentview.timeframe_id)
    timeframe = tf.name
    dataframe = getattr(mt5, f'TIMEFRAME_{timeframe}')
    _symbol = Symbol.objects.get(id = currentview.symbol_id)
    symbol = _symbol.name

    symbol_price = mt5.symbol_info_tick(symbol)._asdict()
    ohlc_data = pd.DataFrame(mt5.copy_rates_from_pos(symbol, dataframe, 0, 600))
    ohlc_data['time']=pd.to_datetime(ohlc_data['time'], unit='s')
    ohlcs = []
    for i, data in ohlc_data.iterrows():
        ohlc = {
            'time':data['time'],
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume']
        }
        ohlcs.append(ohlc)

    data = {
        'symbol':symbol,
        'series':ohlcs, 
        'price': 
        {
            'ask':symbol_price['ask'],
            'bid':symbol_price['bid'],
            'timeframe':timeframe
        }
    }
    
    return JsonResponse(data)

def getSymbolData(request):
    currentview = CurrentView.objects.first()
    currentview.symbol_id = request.POST['selectedSymbol']
    currentview.timeframe_id = request.POST['selectedTimeframe']
    currentview.save()

    currentview = CurrentView.objects.first()
    tf = TimeFrame.objects.get(id = currentview.timeframe_id)
    timeframe = tf.name
    dataframe = getattr(mt5, f'TIMEFRAME_{timeframe}')
    _symbol = Symbol.objects.get(id = currentview.symbol_id)
    symbol = _symbol.name

    symbol_price = mt5.symbol_info_tick(symbol)._asdict()
    
    ohlc_data = pd.DataFrame(mt5.copy_rates_from_pos(symbol, dataframe, 0, 500))
    ohlc_data['time']=pd.to_datetime(ohlc_data['time'], unit='s')
    ohlcs = []
    for i, data in ohlc_data.iterrows():
        ohlc = {
            'time':data['time'].strftime('%Y-%m-%d %H:%M:%S'),
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume']
        }
        ohlcs.append(ohlc)

    data = {
        'symbol':symbol,
        'series':ohlcs, 
        'price': 
        {
            'ask':symbol_price['ask'],
            'bid':symbol_price['bid'],
            'timeframe':timeframe
        }
    }

    data = dumps(data)

    return redirect('/',{
        'resData': data,
        'symbols':Symbol.objects.filter(status="1"),
        'timeframes':TimeFrame.objects.all()
    })
def lineNotification(request):
    message = 'ทดสอบ'
    payload = {'message':message}
    return _lineNotify(payload)


def _lineNotify(payload,file=None):
    url = 'https://notify-api.line.me/api/notify'
    token = 'p59HvOJlVFphWeUtCUmWTfyI5vLbWEUJoHiJXLgdELM'
    headers = {'Authorization':'Bearer '+token}
    return requests.post(url, headers=headers , data = payload, files=file)    

def backtest(request):
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    # mt5.login(login,password,server)

    # account_info = mt5.account_info()
    # print(account_info)

    backtest = BackTest.objects.first()
    tf = TimeFrame.objects.get(id = backtest.timeframe_id)

    backtestdataframe = getattr(mt5, f'TIMEFRAME_{tf.name}')
    firstbacktestsymbol = BackTestSymbol.objects.first()
    _symbol = Symbol.objects.get(id = firstbacktestsymbol.symbol_id)
    backtestsymbol = _symbol.name

    backtestsymbols = BackTestSymbol.objects.filter(backtest_id = backtest.id)
    backtestintervals = BackTestInterval.objects.all()
    
    ohlc_data = pd.DataFrame(mt5.copy_rates_from_pos(backtestsymbol, backtestdataframe, 0, 200))
    ohlc_data['time']=pd.to_datetime(ohlc_data['time'], unit='s')
    ohlcs = []
    for i, data in ohlc_data.iterrows():
        ohlc = {
            'time':data['time'].strftime('%Y-%m-%d %H:%M:%S'),
            'open':data['open'] ,
            'high':data['high'],
            'low':data['low'] ,
            'close':data['close'], 
            'tick':data['tick_volume']
        }
        ohlcs.append(ohlc)

    data = {
        'symbol':_symbol.name,
        'series':ohlcs, 
        'timeframe':tf.name
    }

    data = dumps(data)
    return render(request,'backtest.html',{
        'resData': data,
        'symbols':Symbol.objects.filter(status="1"),
        'timeframes':TimeFrame.objects.all(),
        'backtestsizes':BackTestSize.objects.all(),
        'backtest':backtest,
        'backtestsymbols' : backtestsymbols,
        'backtestintervals':backtestintervals
    })

def createbacktest(request):
    backtestsymbols = request.POST.getlist('backtestsymbols[]')
    backtest = BackTest.objects.first()
    backtest.backtestsize_id = request.POST.get('size')
    backtest.timeframe_id  = request.POST.get('timeframe')
    backtest.interval_id  = request.POST.get('interval')
    backtest.save()

    tf = TimeFrame.objects.get(id = request.POST.get('timeframe'))
    backtestdataframe = getattr(mt5, f'TIMEFRAME_{tf.name}')

    BackTestOHLC.objects.all().delete()
    BackTestSymbol.objects.filter(backtest_id = backtest.id).delete()
    for i in backtestsymbols:
        new = BackTestSymbol(backtest_id= backtest.id, symbol_id=i)
        new.save()

        backtest_symbol = Symbol.objects.filter(id=i).first()
        ohlc_data = pd.DataFrame(mt5.copy_rates_from_pos(backtest_symbol.name, backtestdataframe, 0, 2000))
        ohlc_data['time']=pd.to_datetime(ohlc_data['time'], unit='s')

        bulk_list = list()
        for j, data in ohlc_data.iterrows():
            bulk_list.append(
                BackTestOHLC(symbol_id=i,date=data['time'], open=data['open'], high=data['high'], low=data['low'], close=data['close'], tick=data['tick_volume']))
        BackTestOHLC.objects.bulk_create(bulk_list)   

    data = {
        'backtestsymbols': '',
    }

    return JsonResponse(data)

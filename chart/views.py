from django.shortcuts import render
from datetime import datetime
import pandas as pd
import MetaTrader5 as mt5
from django.http import JsonResponse
from json import dumps
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
    return render(request,'index.html',{'resData': data})

def getohlc(request):  
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
    timeframe = 'M5';
    dataframe = mt5.TIMEFRAME_M5
    tf = request.GET['selectedTimeframe']
    if tf == 'M5':
        timeframe = 'M5';
        dataframe = mt5.TIMEFRAME_M5
    if tf == 'M15':
        timeframe = 'M15';
        dataframe = mt5.TIMEFRAME_M15    
    if tf == 'M30':
        timeframe = 'M30';
        dataframe = mt5.TIMEFRAME_M30        
    if tf == 'H1':
        timeframe = 'H1';
        dataframe = mt5.TIMEFRAME_H1
    if tf == 'H4':
        timeframe = 'H1';
        dataframe = mt5.TIMEFRAME_H4


    symbol = request.GET['selectedSymbol']
    
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
    return render(request,'index.html',{'resData': data})

def lineNotification(request):
    message = 'ทดสอบ'
    payload = {'message':message}
    return _lineNotify(payload)


def _lineNotify(payload,file=None):
    url = 'https://notify-api.line.me/api/notify'
    token = 'p59HvOJlVFphWeUtCUmWTfyI5vLbWEUJoHiJXLgdELM'
    headers = {'Authorization':'Bearer '+token}
    return requests.post(url, headers=headers , data = payload, files=file)    






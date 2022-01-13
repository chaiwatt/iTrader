from django.shortcuts import render,redirect
from datetime import datetime
import pandas as pd
import MetaTrader5 as mt5
from django.http import JsonResponse,HttpResponse
from json import dumps
from django.db.models import Q
from .models import CurrentView,Symbol,TimeFrame,BackTest,BackTestSize,BackTestInterval,BackTestOHLC,Setting,MyAccount,Broker
# import requests
symbol = 'USDJPY'
from django.utils import timezone
from django.core import serializers

#symbol = 'EURUSD'
timeframe = 'M1';
dataframe = mt5.TIMEFRAME_M1

# login = 25006371
# password = 'g(gpG4/hO%Z@'
# server = 'demo.mt5tickmill.com'

# Create your views here.
def index(request):
    setting = Setting.objects.first()
    
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()

    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    mt5.login(myaccount.login,myaccount.password,myaccount.server)

    accountinfo = mt5.account_info()
    
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
            'tick':data['tick_volume'],
            'id':i
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
        'symbols':Symbol.objects.filter(status="1",broker_id=myaccount.broker_id),
        'timeframes':TimeFrame.objects.all(),
        'currentview':currentview,
        'broker':Broker.objects.filter(id = myaccount.broker_id).first(),
        'accountinfo' : accountinfo
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
            'tick':data['tick_volume'],
            'id':i
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
    setting = Setting.objects.first()
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()
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
            'tick':data['tick_volume'],
            'id':i
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
        'symbols':Symbol.objects.filter(status="1",broker_id=myaccount.broker_id),
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

    setting = Setting.objects.first()
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()
    # mt5.login(login,password,server)

    accountinfo = mt5.account_info()
    # print(account_info)

    backtest = BackTest.objects.last()
    # print(backtest.code)
    # tf = TimeFrame.objects.get(id = backtest.timeframe_id)

    # backtestdataframe = getattr(mt5, f'TIMEFRAME_{tf.name}')
    # firstbacktestsymbol = BackTestSymbol.objects.first()
    # _symbol = Symbol.objects.get(id = firstbacktestsymbol.symbol_id)
    # backtestsymbol = _symbol.name

    # backtestsymbols = None
    # if backtest != None:
    #      backtestsymbols = BackTestSymbol.objects.filter(backtest_id = backtest.id)

    backtestintervals = BackTestInterval.objects.all()
    
    # ohlc_data = pd.DataFrame(mt5.copy_rates_from_pos(backtestsymbol, backtestdataframe, 0, 200))
    # ohlc_data['time']=pd.to_datetime(ohlc_data['time'], unit='s')
    # ohlcs = []
    # for i, data in ohlc_data.iterrows():
    #     ohlc = {
    #         'time':data['time'].strftime('%Y-%m-%d %H:%M:%S'),
    #         'open':data['open'] ,
    #         'high':data['high'],
    #         'low':data['low'] ,
    #         'close':data['close'], 
    #         'tick':data['tick_volume']
    #     }
    #     ohlcs.append(ohlc)

    # data = {
    #     'symbol':_symbol.name,
    #     'series':ohlcs, 
    #     'timeframe':tf.name
    # }

    # data = dumps(data)
    return render(request,'backtest.html',{
        # 'resData': data,
        'symbols':Symbol.objects.filter(status="1",broker_id=myaccount.broker_id),
        'timeframes':TimeFrame.objects.all(),
        'backtestsizes':BackTestSize.objects.all(),
        'backtest':backtest,
        # 'backtestsymbols' : backtestsymbols,
        'backtestintervals':backtestintervals,
        'broker':Broker.objects.filter(id = myaccount.broker_id).first(),
        'accountinfo' : accountinfo,
        'backtestjobs' : BackTest.objects.all().order_by("-id")
    })

def createbacktest(request):

    btsize = BackTestSize.objects.filter(id = int(request.POST.get('size'))).first().size + 250

    backtestsymbol = request.POST.get('backtestsymbol')

    # print(backtestsymbol)

    newBackTest = BackTest(symbol_id= backtestsymbol,code= datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),backtestsize_id= request.POST.get('size'),timeframe_id= request.POST.get('timeframe'), interval_id=request.POST.get('interval'))
    newBackTest.save()

    backtestid = newBackTest.id

    tf = TimeFrame.objects.get(id = request.POST.get('timeframe'))
    backtestdataframe = getattr(mt5, f'TIMEFRAME_{tf.name}')

    # BackTestOHLC.objects.all().delete()
    # BackTestSymbol.objects.filter(backtest_id = backtest.id).delete()
    # for i in backtestsymbols:
    # new = BackTestSymbol(backtest_id= newBackTest.id, symbol_id=i)
    # new.save()

    backtest_symbol = Symbol.objects.filter(id=backtestsymbol).first()
    ohlc_data = pd.DataFrame(mt5.copy_rates_from_pos(backtest_symbol.name, backtestdataframe, 0, btsize))
    ohlc_data['time']=pd.to_datetime(ohlc_data['time'], unit='s')

    bulk_list = list()
    for j, data in ohlc_data.iterrows():
        bulk_list.append(
            BackTestOHLC(backtest_id=newBackTest.id,symbol_id=backtestsymbol,date=data['time'], open=data['open'], high=data['high'], low=data['low'], close=data['close'], tick=data['tick_volume']))
    BackTestOHLC.objects.bulk_create(bulk_list)   

    data = {
        'backtest': serializers.serialize('json', BackTest.objects.filter(id = backtestid)),
        'backtestjobs' : serializers.serialize('json', BackTest.objects.all().order_by("-id")), 
    }

    return JsonResponse(data)

def deleteallbacktest(request):
    BackTest.objects.all().delete()
    data = {
        'backtestjobs' :  serializers.serialize('json', BackTest.objects.all().order_by("-id")), 
    }
    return JsonResponse(data)

def deletebacktest(request):
    BackTest.objects.filter(id = request.POST.get('id')).delete()
    data = {
        'backtestjobs' :  serializers.serialize('json', BackTest.objects.all().order_by("-id")), 
    }
    return JsonResponse(data)

def getbacktestjob(request):
    setting = Setting.objects.first()
    
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()
    id = request.POST.get('id')
    data = {
        'backtest': serializers.serialize('json', BackTest.objects.filter(id = id)),
        'symbols': serializers.serialize('json', Symbol.objects.filter(status="1",broker_id=myaccount.broker_id)),
        'timeframes': serializers.serialize('json', TimeFrame.objects.all()),
        'intervals': serializers.serialize('json', BackTestInterval.objects.all()),
        'backtestsizes': serializers.serialize('json', BackTestSize.objects.all()),
        'ohlcs': serializers.serialize('json', BackTestOHLC.objects.filter(backtest_id = id)),
    }
    return JsonResponse(data)    

def jogtest(request):
    id = request.POST.get('id')
    data = {
        'backtest': serializers.serialize('json', BackTest.objects.filter(id = id)),
        
    }
    return JsonResponse(data)

def symbolsetting(request):
    return render(request,'symbol.html') 

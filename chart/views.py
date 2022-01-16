from django.shortcuts import render,redirect
from datetime import datetime
import pandas as pd
import MetaTrader5 as mt5
from django.http import HttpRequest, JsonResponse,HttpResponse
from json import dumps
from django.db.models import Q
from .models import CurrentView,Symbol,TimeFrame,BackTest,BackTestSize,BackTestInterval,BackTestOHLC,Setting,MyAccount,Broker,TestSpec,Spec
import requests
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
    
    # symbol_info=mt5.symbol_info(symbol)
    # print (symbol_info)

    # lasttick=mt5.symbol_info_tick(symbol)
    # print(lasttick)
    
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
        'accountinfo' : accountinfo,
        'buytestspec' : serializers.serialize('json', TestSpec.objects.filter(id = 1)),  
        'entryspecobjectss' : Spec.objects.filter(spec_type = 1,status = 1), 
        'entryspecs' : serializers.serialize('json', Spec.objects.filter(spec_type = 1,status = 1)), 
        'exitspecs' : serializers.serialize('json', Spec.objects.filter(spec_type = 2,status = 1)), 
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
    print('hello')
    # message = 'ทดสอบ'
    payload = {
        'message':request.POST['message']
    }
    url = 'https://notify-api.line.me/api/notify'
    token = 'p59HvOJlVFphWeUtCUmWTfyI5vLbWEUJoHiJXLgdELM'
    headers = {'Authorization':'Bearer '+token}
    result = requests.post(url, headers=headers , data = payload, files=None)    
    data = {
        'data':'nothing',
    }
    return JsonResponse(data)


# def _lineNotify(payload,file=None):
#     url = 'https://notify-api.line.me/api/notify'
#     token = 'p59HvOJlVFphWeUtCUmWTfyI5vLbWEUJoHiJXLgdELM'
#     headers = {'Authorization':'Bearer '+token}
#     result = requests.post(url, headers=headers , data = payload, files=file)    
#     return HttpRequest(None)

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
   

    backtestintervals = BackTestInterval.objects.all()
    

    return render(request,'backtest.html',{
        'symbols':Symbol.objects.filter(status="1",broker_id=myaccount.broker_id),
        'timeframes':TimeFrame.objects.all(),
        'backtestsizes':BackTestSize.objects.all(),
        'backtest':backtest,
        'specs' : serializers.serialize('json', Spec.objects.all()), 
        'backtestintervals':backtestintervals,
        'broker':Broker.objects.filter(id = myaccount.broker_id).first(),
        'accountinfo' : accountinfo,
        'backtestjobs' : BackTest.objects.all().order_by("-id"),
        'buytestspec' : serializers.serialize('json', TestSpec.objects.filter(id = 1)),  
        'entryspecobjectss' : Spec.objects.filter(spec_type = 1,status = 1), 
        'entryspecs' : serializers.serialize('json', Spec.objects.filter(spec_type = 1,status = 1)), 
        'exitspecs' : serializers.serialize('json', Spec.objects.filter(spec_type = 2,status = 1)), 
    })

def createbacktest(request):

    btsize = BackTestSize.objects.filter(id = int(request.POST.get('size'))).first().size + 250

    backtestsymbol = request.POST.get('backtestsymbol')

    # print(backtestsymbol)

    tf = TimeFrame.objects.get(id = request.POST.get('timeframe'))
    backtestdataframe = getattr(mt5, f'TIMEFRAME_{tf.name}')

    symbol = Symbol.objects.filter(id = backtestsymbol).first()

    newBackTest = BackTest(symbol_id= backtestsymbol,timeframename= tf.name,symbolname= symbol.name,code= datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),backtestsize_id= request.POST.get('size'),timeframe_id= request.POST.get('timeframe'), interval_id=request.POST.get('interval'))
    newBackTest.save()

    backtestid = newBackTest.id

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
    setting = Setting.objects.first()
    
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()
    return render(request,'symbol.html',{
        'symbols':Symbol.objects.filter(broker_id=myaccount.broker_id),
    }) 

def changesymbolstatus(request):
    id = request.POST.get('id')
    symbol = Symbol.objects.filter(id = id).first()
    symbol.status = request.POST['status']
    symbol.save()
    data = {
        'backtest': serializers.serialize('json', Symbol.objects.filter(id = id)),
    }
    return JsonResponse(data)

def spec(request):
    setting = Setting.objects.first()
    
    myaccount = MyAccount.objects.filter(id = setting.myaccount_id).first()

    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    mt5.login(myaccount.login,myaccount.password,myaccount.server)

    accountinfo = mt5.account_info()
    
    # print(accountinfo)



    return render(request,'spec.html',{
        'accountinfo' : accountinfo,
        'broker':Broker.objects.filter(id = myaccount.broker_id).first(),
        'buytestspec':TestSpec.objects.filter(id = 1).first(),
        'entryspecobjectss' : Spec.objects.filter(spec_type = 1), 
        'entryspecs' : serializers.serialize('json', Spec.objects.filter(spec_type = 1)), 
        'exitspecs' : serializers.serialize('json', Spec.objects.filter(spec_type = 2)), 
    })  

def savebuytestspec(request):
    # print(request.POST.get('ma8_percent_diff_ma13'))
    buyTestSpec = TestSpec.objects.filter(id = 1).first()
    buyTestSpec.aligator_trend = request.POST['aligator_trend']
    buyTestSpec.ma5_slope = request.POST['ma5_slope']

    buyTestSpec.ma5_std = request.POST['ma5_std']
    buyTestSpec.ma8_slope = request.POST['ma8_slope']
    buyTestSpec.ma8_std = request.POST['ma8_std']
    buyTestSpec.ma13_slope = request.POST['ma13_slope']
    buyTestSpec.ma13_std = request.POST['ma13_std']
    buyTestSpec.ma100_slope = request.POST['ma100_slope']
    buyTestSpec.ma100_arrow_below = request.POST['ma100_arrow_below']
    buyTestSpec.macd_cross = request.POST['macd_cross']
    buyTestSpec.macd_trend = request.POST['macd_trend']
    buyTestSpec.rsi = request.POST['rsi']
    buyTestSpec.ma8_percent_diff_ma5 = request.POST['ma8_percent_diff_ma5']
    buyTestSpec.ma8_percent_diff_ma13 = request.POST['ma8_percent_diff_ma13']
    buyTestSpec.ssma3line_uptrend = request.POST['ssma3line_uptrend']
    buyTestSpec.save()
    data = {
        'backtest': serializers.serialize('json', TestSpec.objects.filter(id = 1)),
    }
    return JsonResponse(data)     

def changespecusage(request):
    id = request.POST.get('id')
    spec = Spec.objects.filter(id = id).first()
    spec.status = request.POST['status']
    spec.save()
    data = {
        'specs': serializers.serialize('json', Spec.objects.filter(spec_type = 1)),
    }
    return JsonResponse(data)

def changespecentrypointvalue(request):
    id = request.POST.get('id')
    spec = Spec.objects.filter(id = id).first()
    spec.entry_value = request.POST['value']
    spec.save()
    data = {
        'specs': serializers.serialize('json', Spec.objects.filter(spec_type = 1)),
    }
    return JsonResponse(data)
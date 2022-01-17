from django.shortcuts import render,redirect
from datetime import datetime
import pandas as pd
import MetaTrader5 as mt5
from django.http import HttpRequest, JsonResponse,HttpResponse
from json import dumps
from django.db.models import Q
from .models import CurrentView,Symbol,TimeFrame,BackTest,BackTestSize,BackTestInterval,BackTestOHLC,Setting,MyAccount,Broker,Spec
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
        'exitspecobjects' : Spec.objects.filter(spec_type = 2,status = 1,symbol_id = currentview.symbol_id),   
        'entryspecobjectss' : Spec.objects.filter(spec_type = 1,status = 1,symbol_id = currentview.symbol_id), 
        'entryspecs' : serializers.serialize('json', Spec.objects.filter(spec_type = 1,status = 1,symbol_id = currentview.symbol_id)), 
        'exitspecs' : serializers.serialize('json', Spec.objects.filter(spec_type = 2,status = 1,symbol_id = currentview.symbol_id)), 
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
        'exitspecobjects' : Spec.objects.filter(spec_type = 2,status = 1), 
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
    symbolid = request.POST.get('symbol_id')
    data = {
        'backtest': serializers.serialize('json', BackTest.objects.filter(id = id)),
        'symbols': serializers.serialize('json', Symbol.objects.filter(status="1",broker_id=myaccount.broker_id)),
        'timeframes': serializers.serialize('json', TimeFrame.objects.all()),
        'intervals': serializers.serialize('json', BackTestInterval.objects.all()),
        'backtestsizes': serializers.serialize('json', BackTestSize.objects.all()),
        'ohlcs': serializers.serialize('json', BackTestOHLC.objects.filter(backtest_id = id)),
        'entryspecs': serializers.serialize('json', Spec.objects.filter(symbol_id = symbolid, status =1, spec_type =1)),
        'exitspecs': serializers.serialize('json', Spec.objects.filter(symbol_id = symbolid, status =1, spec_type =2)),
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

    # ids = Spec.objects.all().values_list('symbol_id', flat=True).distinct('symbol_id')
    ids = Spec.objects.all().values('symbol_id').distinct()
    print(ids)
    print(Symbol.objects.filter(id__in = ids))


    return render(request,'spec.html',{
        'accountinfo' : accountinfo,
        'broker':Broker.objects.filter(id = myaccount.broker_id).first(),
        'symbols':Symbol.objects.filter(id__in = ids,status=1),
        'entryspecobjectss' : Spec.objects.filter(spec_type = 1), 
        'exitspecobjects' : Spec.objects.filter(spec_type = 2), 
        'entryspecs' : serializers.serialize('json', Spec.objects.filter(spec_type = 1)), 
        'exitspecs' : serializers.serialize('json', Spec.objects.filter(spec_type = 2)), 
    })  


def changespecusage(request):
    id = request.POST.get('id')
    symbolid = request.POST.get('symbol')
    spec = Spec.objects.filter(id = id,symbol_id=symbolid).first()
    spec.status = request.POST['status']
    spec.save()
    data = {
        'specs': serializers.serialize('json', Spec.objects.filter(spec_type = 1, status=1)),
    }
    return JsonResponse(data)

def changespecentrypointvalue(request):
    id = request.POST.get('id')
    symbolid = request.POST.get('symbol')
    val = request.POST['value'];
    print(val)
    spec = Spec.objects.filter(id = id,symbol_id=symbolid).first()
   
    if spec.parameter_type == 'equal':
       if spec.exit_value ==  val:
          spec.exit_value = spec.entry_value

    spec.entry_value = request.POST['value']
    spec.save()

    data = {
        'specs': serializers.serialize('json', Spec.objects.filter(spec_type = 1, status=1)),
    }
    return JsonResponse(data)

def clonespec(request):
    symbolid = request.POST.get('id')
    Spec.objects.filter(~Q(symbol_id=symbolid)).delete()
    basespec = Spec.objects.filter(symbol_id=symbolid)


    symbols = Symbol.objects.filter(~Q(id=symbolid))
    # print(symbols)

    for symbol in symbols.iterator():
        for base in basespec.iterator():
            # print(base.name)
            newspec = Spec(
                    name= base.name,
                    parameter= base.parameter,
                    entry_value= base.entry_value,
                    exit_value= base.exit_value,
                    parameter_type= base.parameter_type,
                    compare_reverse= base.compare_reverse,
                    status= base.status,
                    spec_type= base.spec_type,
                    symbol_id = symbol.id
                )
            newspec.save()

    data = {
        'specs': serializers.serialize('json', Spec.objects.filter(spec_type = 1, symbol_id=symbolid, status=1)),
    }
    return JsonResponse(data)

def getentryspec(request):
    symbolid = request.POST.get('id')
    data = {
        'spec': serializers.serialize('json', Spec.objects.filter(spec_type = 1, symbol_id=symbolid)),
    }
    return JsonResponse(data)


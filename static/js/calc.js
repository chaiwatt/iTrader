    var upColor = '#00da3c';
    var downColor = '#ec0000';

    function createRawData(backtestOhlc){
        var _data = []
        JSON.parse(backtestOhlc).forEach((ohlc,key) => {
            _data.push({
                    time: ohlc.fields.date,
                    open: ohlc.fields.open,
                    close: ohlc.fields.close,
                    low: ohlc.fields.low,
                    high: ohlc.fields.high,
                    tick: ohlc.fields.tick,
                    index: ohlc.pk,
                })
        });
        return _data;
    }
    
    function getData(_arr) {
        var _data = []
        _arr.forEach((item,key) => {
            let _index = item.index;
            if(typeof _index === "undefined"){
                _index = item.id;
            }
            _data.push(Object.seal([
                item.open,
                item.close,
                item.low,
                item.high,
                _index,
                item.time,
            ]))
        });
        return _data;
    }

    function getSampleData(_arr) {
        var _data = []
        _arr.forEach((item,key) => {
            _data.push(Object.seal([item.open,item.close,item.low,item.high,key]))
        });
        return _data;
    }

    function getClosedPrice(_arr) {
        var _closedprice = []
        _arr.forEach((item) => {
            _closedprice.push(item.close)
        });
        return _closedprice;
    }

    function getLowPrice(_arr) {
        var _lowprice = []
        _arr.forEach((item) => {
            _lowprice.push(item.low)
        });
        return _lowprice;
    }

    function getHighPrice(_arr) {
        var _highprice = []
        _arr.forEach((item) => {
            _highprice.push(item.high)
        });
        return _highprice;
    }

    function getDateLabel(_arr) {
        var _dateLabel = []
        _arr.forEach((item) => {
            _dateLabel.push(item.time)
        });
        return _dateLabel;
    }

    function getAvgClosedPrice(mArray,mRange){
        return mArray.slice(0, mRange).reduce((a,c) => a + c, 0) / mRange;
    }

    function EMACalc(mArray,mRange) {
        var k = 2/(mRange + 1);
        var avgClosed = getAvgClosedPrice(mArray,mRange)
        emaArray = [avgClosed];
        
        var _emaArray = [];
        for (var i = mRange; i < mArray.length+1; i++) {
            emaArray.push(mArray[i] * k + emaArray[i -mRange] * (1 - k));
            _emaArray.push(emaArray[i-mRange]);
        }
        return _emaArray;
    }

    function SSMA_BARESMOTH(arrSSMA,mRange) {
        _ssmaSmoth = [];
        for (var i = 0; i < arrSSMA.length-mRange+1; i++) {
            var ssmaSmoth = arrSSMA.slice(i, mRange+i).reduce((a,c) => a + c, 0) / mRange;
            _ssmaSmoth.push(ssmaSmoth);
        }
        return _ssmaSmoth;
    }

    function calculateMA(dayCount, data) {
        var result = [];
        for (var i = 0, len = data.length; i < len; i++) {
            if (i < dayCount) {
                result.push('-');
                continue;
            }
            var sum = 0;
            for (var j = 0; j < dayCount; j++) {
                sum += data[i - j][1];
            }
            result.push((sum / dayCount));
        }
        return result;
    }

    function EMACalc(mArray,mRange) {
        var k = 2/(mRange + 1);
        var avgClosed = getAvgClosedPrice(mArray,mRange)
        emaArray = [avgClosed];
        
        var _emaArray = [];
        for (var i = mRange; i < mArray.length+1; i++) {
            emaArray.push(mArray[i] * k + emaArray[i -mRange] * (1 - k));
            _emaArray.push(emaArray[i-mRange]);
        }
        return _emaArray;
    }

    function MACDCalc(mArray1,mArray2,mRange1,mRange2) {
        var diffRange = mRange1 - mRange2;
        var _macdArray = [];
        for (var i = 0; i < mArray1.length; i++) {
            var _macd  = mArray2[i+diffRange] - mArray1[i];
            _macdArray.push(_macd);
        }
        return _macdArray;
    }

    function HistogramCalc(mArray1,mArray2,mRange) {
        var diffRange = mRange - 1;
        var _histogramArray = [];
        for (var i = 0; i < mArray1.length; i++) {
            var _histogram = mArray2[i+diffRange] - mArray1[i];
            _histogramArray.push(_histogram);
        }
        return _histogramArray;
    }

    function SSMA_Calc(arr,n){
        var ssma = [];
        ssma.push(avarageSum(arr,n));

        for (var i = 1 ; i < arr.length ; i++){
            ssma.push((ssma[i-1]*(n-1) + arr[i])/n);
        }
        return ssma;

        function avarageSum(arr,n){
            var temp = arr.slice(0, n);
            return temp.reduce(function(a,b){return a+b;})/temp.length;
        }
    }

    function getSignChange(arr,macdarr){
        let positive = arr[0] >= 0; 
        return arr.map((item, index) => {
            if ((positive && item < 0 || !positive && item >= 0)) {
                positive = arr[index] >= 0
                if(arr[index-1]!==null && item !== null){
                    var isUpTrendUpperMacd = '';
                    var macdatpoint = macdarr[index];
                    if(item > 0){
                        if(macdatpoint < 0){
                            isUpTrendUpperMacd = 'under';
                        }else{
                            isUpTrendUpperMacd = 'above';
                        }
                    }
                    return [index-1, arr[index-1], item,isUpTrendUpperMacd]
                }
            }
        }).filter(x => x != null);
    }

    function getMacdCross(macd,signal){
        let isUp = true;
        let crossAbove = true;  
        let crossIndex = 0; 
        if(macd[macd.length-1] > signal[signal.length-1]){ 
            for(var i = macd.length-1 ; i > 0 ; i--){
                if(macd[i] < signal[i]){
                    if(macd[i] < 0){       
                        crossAbove = false
                    }
                    crossIndex = i;
                    break;
                }
            }
        }else{
            isUp = false
            for(var i = macd.length-1 ; i > 0 ; i--){
                if(macd[i] > signal[i]){
                    if(macd[i] < 0){
                        crossAbove = false
                    }
                    crossIndex = i;
                    break;
                }
            }
        }
        return [isUp,crossAbove,crossIndex+1,macd[macd.length-1]]
    }

    function genRegressionLine(_data,nRange){
        var yVal = [];
        for(var i = _data.length-nRange ; i < _data.length ; i++ ){
            yVal.push(_data[i]);
        }
        const xVal = Array(nRange ).fill().map((_, idx) => 1 + idx)
      
        const mX = xVal.reduce((a,v,i)=>(a*i+v)/(i+1));
        const mY = yVal.reduce((a,v,i)=>(a*i+v)/(i+1));

        let xValMinusMx = xVal.map(function(val){
            return  (val - mX)
        })

        let xValMinusMxSquare = xValMinusMx.map(function(val){
            return  val*val
        })

        let yValMinusMy = yVal.map(function(val){
            return  (val - mY)
        })
      
        let diffMxTimediffMy = yValMinusMy.map(function(val,index){
            return val * xValMinusMx[index]
        })

        const sumSquareError = xValMinusMxSquare.reduce((a, b) => a + b, 0)

        const sumdiffMxTimediffMy = diffMxTimediffMy.reduce((a, b) => a + b, 0)
        
        let slope = sumdiffMxTimediffMy/sumSquareError

        let constantC = mY - mX*slope

        return [slope,constantC]
    }

    function getCoord(arr,startX,endX,nRage){
        let startY = 1 * arr[0] + arr[1]
        let endY = nRage * arr[0] + arr[1]
        return [[startX,startY],[endX,endY]]
    }

    function isUpTrend(slope,_data,sma100,nRange,slopeSpec){
        let tmp = [
                {
                name: {
                    slope: 'Slope: ' + slope
                },
                value: sma100[_data.length-1],
                xAxis: _data.length-1,
                yAxis: sma100[_data.length-1],
                color: "#000",
            }
        ]
        var allSMA100Low = true;
        for(var i = _data.length-nRange ; i < _data.length ; i++ ){
            if(sma100[i] > _data[i][2]){
                allSMA100Low = false
                return [tmp, false]
            }        
        }
        if(allSMA100Low == true && slope > slopeSpec){
            return [tmp, true]
        }else{
            return [tmp, false]
        }
    }

    function sma100ArrowBelow(_data,sma100,nRange){
        for(var i = _data.length-nRange ; i < _data.length ; i++ ){
            if(sma100[i] > _data[i][2]){
                return false
            }        
        }
        return true;
    }

    function sma100PresentBelow(_data,sma100){
        c = _data.length-1
        if(sma100[c] > _data[c][2]){
            return false
        }   

        return true;
    }

    function sma100ArrowAbove(_data,sma100,nRange){   
        for(var i = _data.length-nRange ; i < _data.length ; i++ ){
            if(sma100[i] < _data[i][3]){
                return false
            }        
        }
        return true;
    }

    function sma100PresentAbove(_data,sma100){   
        c = _data.length-1
        if(sma100[c] < _data[c][3]){
            return false
        }   

        return true;
    }

    function getMomenttumBar(_data){ 
        let present = _data[_data.length-1]
        let previous1 = _data[_data.length-2]
        let previous2 = _data[_data.length-3]
        let previous3 = _data[_data.length-4]  

        let diffHiLow_present = present[3] - present[2];
        let diffHiLow_previous1 = previous1[3]- previous1[2];
        let diffHiLow_previous2 = previous2[3] - previous2[2];
        let diffHiLow_previous3 = previous3[3] - previous3[2];

        if(diffHiLow_present > 2.5*(diffHiLow_previous1) && diffHiLow_present > 2.5*(diffHiLow_previous2) && diffHiLow_present > 2.5*(diffHiLow_previous3)){
            if(present[2] < previous1[2] && present[2] < previous2[2]  && present[2] < previous3[2] ){
                return {
                    foundBar : true,
                    order : 'sell',
                }
            } else{
                return {
                    foundBar : true,
                    order : 'buy',
                }
            }
        }
        return {
            foundBar : false,
            order : 'sell',
        }
        // c = _data.length-1
        // if(sma100[c] < _data[c][3]){
        //     return false
        // }   

        // return true;
    }

    function getSsma3LineOrder(ssma5,ssma8,ssma13){
        // isSsmaSequencing = isSssmaSequence(Smoth_SSMA5Arr,Smoth_SSMA8Arr,Smoth_SSMA13Arr)
        let isUpTrend = false;
        let isDownTrend = false;
        if((ssma5[ssma5.length-1] > ssma8[ssma8.length-1]) && (ssma8[ssma8.length-1] > ssma13[ssma13.length-1])){
            isUpTrend = true
        }

        if((ssma5[ssma5.length-1] < ssma8[ssma8.length-1]) && (ssma8[ssma8.length-1] < ssma13[ssma13.length-1])){
            isDownTrend = true
        }
        return {'aligator_order_uptrend': isUpTrend, 'aligator_order_downtrend': isDownTrend}
    }

    function StandardDeviationCalc(_array,nRange) {
        let array = _array.slice((_array.length - nRange), _array.length)
        const mean = array.reduce((a, b) => a + b) / nRange
        return Math.sqrt(array.map(x => Math.pow(x - mean, 2)).reduce((a, b) => a + b) / nRange)
    }

    function RS(mArray,mRange) {
        var _closePriceChanged = [];
        var _closePriceChangedGain = [];
        var _closePriceChangedLost = [];
        var _avgGain = [];
        var _avgLost = [];
        
        var _RS = [];
        for (var i = 1; i < mArray.length; i++) {
            var closePriceChanged  = mArray[i] - mArray[i-1];
            _closePriceChanged.push(closePriceChanged);
            if(closePriceChanged > 0){
                _closePriceChangedGain.push(closePriceChanged);
                _closePriceChangedLost.push(0);
            }else{
                _closePriceChangedGain.push(0);
                _closePriceChangedLost.push(closePriceChanged*-1)
            }
        }

        var avgGain = _closePriceChangedGain.slice(0, mRange).reduce((a,c) => a + c, 0) / mRange;
        var avgLost = _closePriceChangedLost.slice(0, mRange).reduce((a,c) => a + c, 0) / mRange;

        _avgGain = [avgGain];
        _avgLost = [avgLost];


        for (var i = mRange; i < _closePriceChangedGain.length; i++) {
            _avgGain.push((_avgGain[i-mRange]*(mRange-1) + _closePriceChangedGain[i])/mRange );
        }

        for (var i = mRange; i < _closePriceChangedLost.length; i++) {
            _avgLost.push((_avgLost[i-mRange]*(mRange-1) + _closePriceChangedLost[i])/mRange );
        }
        for (var i = 0; i < _avgGain.length; i++) {
            var rs = _avgGain[i] / _avgLost[i];
            if(_avgLost[i] == 0){
                _RS.push(100);
            }else{
                _RS.push(100-(100/(1+rs)));
            }
        }
        return _RS;
    }


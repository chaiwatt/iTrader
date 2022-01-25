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
                item.tick,
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

    function getMomenttumBar(_data,presentLevel,gain){ 
        let present = _data[_data.length-1]
        let previous1 = _data[_data.length-2]
        let previous2 = _data[_data.length-3]
        let previous3 = _data[_data.length-4]  

    //     if(isCorrectWickTail(previous1,80) == false || isCorrectWickTail(previous2,80) == false || isCorrectWickTail(previous3,80) == false){
    //         return {
    //             id : present[4],
    //             foundBar : false,
    //             type : '',
    //         }
    //    }

        let diffHiLow_present = present[3] - present[2];
        let diffHiLow_previous1 = previous1[3]- previous1[2];
        let diffHiLow_previous2 = previous2[3] - previous2[2];
        let diffHiLow_previous3 = previous3[3] - previous3[2];

        if(diffHiLow_present > gain*(diffHiLow_previous1) && diffHiLow_present > gain*(diffHiLow_previous2) && diffHiLow_present > gain*(diffHiLow_previous3)){
            if(present[2] < previous1[2] && present[2] < previous2[2]  && present[2] < previous3[2] && presentLevel.sma100_present_above == true){
                return {
                    id : present[4],
                    foundBar : true,
                    type : 1,
                }
            } else if(present[2] > previous1[2] && present[2] > previous2[2]  && present[2] > previous3[2] && presentLevel.sma100_present_below == true){
                return {
                    id : present[4],
                    foundBar : true,
                    type : 2,
                }
            }else{
                return {
                    id : present[4],
                    foundBar : false,
                    type : '',
                }
            }
        }
        return {
            id : present[4],
            foundBar : false,
            type : '',
        }
        // c = _data.length-1
        // if(sma100[c] < _data[c][3]){
        //     return false
        // }   

        // return true;
    }

    function getTrendPattern(_data,presentLevel){
        let present = _data[_data.length-1]
        let previous1 = _data[_data.length-2]
        let previous2 = _data[_data.length-3]
        let previous3 = _data[_data.length-4]  

        if(isCorrectWickTail(previous1,30) == false || isCorrectWickTail(previous2,30) == false || isCorrectWickTail(previous3,30) == false){
            return {
                id : present[4],
                foundBar : false,
                type : '',
            }
       }

        if(presentLevel.sma100_present_below == true){ //check up trend
            if(previous1[0] > previous2[0] && previous2[0] > previous3[0] && previous1[2] > previous2[2] && previous2[2] > previous3[2] ){
                // console.log('pattern up trend')
                return {
                    id : present[4],
                    foundBar : true,
                    type : 2,
                }
            }else{
                return {
                    id : present[4],
                    foundBar : false,
                    type : '',
                }
            }
        }else if(presentLevel.sma100_present_above == true){ //check down trend
            if(previous1[0] < previous2[0] && previous2[0] < previous3[0] && previous1[2] < previous2[2] && previous2[2] < previous3[2] ){
                // console.log('pattern down trend')
                return {
                    id : present[4],
                    foundBar : true,
                    type : 1,
                }
            }else{
                return {
                    id : present[4],
                    foundBar : false,
                    type : '',
                }
            }
        }else{
            return {
                id : present[4],
                foundBar : false,
                type : '',
            }
        }

    }

    // function getMomenttum2Bar(_data,gain){ 
    //     let present = _data[_data.length-1]
    //     let previous1 = _data[_data.length-2]
    //     let previous2 = _data[_data.length-3]

    //    if(isCorrectWickTail(previous1,80) == false || isCorrectWickTail(previous2,80) == false ){
    //         return {
    //             id : _data.length-1,
    //             foundBar : false,
    //             type : '',
    //         }
    //    }

    //     let diffHiLow_present = present[3] - present[2];
    //     let diffHiLow_previous1 = previous1[3]- previous1[2];
    //     let diffHiLow_previous2 = previous2[3] - previous2[2];

    //     if(diffHiLow_present > gain*(diffHiLow_previous1) && diffHiLow_present > gain*(diffHiLow_previous2) ){
    //         if(present[2] < previous1[2] && present[2] < previous2[2] ){
    //             return {
    //                 id : present[4],
    //                 foundBar : true,
    //                 type : 1,
    //             }
    //         } else{
    //             return {
    //                 id : present[4],
    //                 foundBar : true,
    //                 type : 2,
    //             }
    //         }
    //     }
    //     return {
    //         id : _data.length-1,
    //         foundBar : false,
    //         type : '',
    //     }
    //     // c = _data.length-1
    //     // if(sma100[c] < _data[c][3]){
    //     //     return false
    //     // }   

    //     // return true;
    // }

    function isContinuityDownTrendrend(_data,sma100){
        let downtren0 = sma100[sma100.length-1] - _data[_data.length-1][3]
        let downtren1 = sma100[sma100.length-2] - _data[_data.length-2][3]
        let downtren2 = sma100[sma100.length-3] - _data[_data.length-3][3]  

        if(downtren0 > downtren1 && downtren1 > downtren2){
            // console.log(downtren0+ ' ' + downtren1+ ' ' + downtren2)
            return true
        }else {
            return false
        }
    }

    function twoBarsUp(_data,barSize){
        let presentbarsize = _data[_data.length-1][1] - _data[_data.length-1][0] 
        let previous1 = _data[_data.length-2][1] -_data[_data.length-2][0]
        let previous2 = _data[_data.length-3][1] - _data[_data.length-3][0]

        if(Math.abs(presentbarsize) > barSize && Math.abs(previous1) > barSize && Math.abs(previous2) > barSize && presentbarsize > 0 && previous1 > 0 && previous2 > 0){
            if(_data[_data.length-1][3] > _data[_data.length-2][3] && _data[_data.length-2][3] > _data[_data.length-3][3] &&  _data[_data.length-1][2] > _data[_data.length-2][2] && _data[_data.length-2][2] > _data[_data.length-3][2]){
                console.log('found two bar up')
                // console.log(`${presentbarsize} ${previous1} ${previous2}`)
                return true
            }else{
                return false 
            }
        }else{
            return false
        }
    }

    function bullishBars(_data,barsize,gain,numbars){
        for (let i = 1 ; i <= numbars; i++){
            let open = _data[_data.length-i][0]
            let close = _data[_data.length-i][1]
            let body = close - open
            if(body < 0 || Math.abs(body) < barsize*gain){
                return false
            }
        }
        return true
    }

    function bullishLadder(_data,numbars){
        for (let i = 1 ; i < numbars; i++){
            let preopen = _data[_data.length-i][0]
            let postopen = _data[_data.length-i-1][0]

            let preclose = _data[_data.length-i][1]
            let postclose = _data[_data.length-i-1][1]
       
            if(preopen < postopen){
                return false
            }
            if(preclose < postclose){
                return false
            }
        }
        return true
    }

    function bearishTrend(_data,barsize,gain,numbars){
        for (let i = 1 ; i <= numbars; i++){
            let open = _data[_data.length-i][0]
            let close = _data[_data.length-i][1]
            let body = open - close 
            if(body < 0 || Math.abs(body) < barsize*gain){
                return false
            }
        }
        return true
    }

    function bearishLadder(_data,numbars){
        for (let i = 1 ; i < numbars; i++){
            let preopen = _data[_data.length-i][0]
            let postopen = _data[_data.length-i-1][0]

            let preclose = _data[_data.length-i][1]
            let postclose = _data[_data.length-i-1][1]
       
            if(preopen > postopen){
                return false
            }
            if(preclose > postclose){
                return false
            }
        }
        return true
    }

    function twoBarsDown(_data,barSize){
        let presentbarsize = _data[_data.length-1][0] - _data[_data.length-1][1]
        let previous1 = _data[_data.length-2][0] - _data[_data.length-2][1]
        let previous2 = _data[_data.length-3][0] - _data[_data.length-3][1]

        if(Math.abs(presentbarsize) > barSize && Math.abs(previous1) > barSize && Math.abs(previous2) > barSize && presentbarsize > 0 && previous1 > 0 && previous2 > 0){
            if(_data[_data.length-1][3] < _data[_data.length-2][3] && _data[_data.length-2][3] < _data[_data.length-3][3] &&  _data[_data.length-1][2] < _data[_data.length-2][2] && _data[_data.length-2][2] < _data[_data.length-3][2]){
                console.log('found two bar down')
                // console.log(`${presentbarsize} ${previous1} ${previous2}`)
                return true
            }else{
                return false 
            }
        }else{
            return false
        }

    }

    function momentumBarUp(_data,_barSize,barSizeRatio,gain){
        let barSize = _barSize*barSizeRatio
        // console.log('barSize' + barSize)
        let presentbarsize = _data[_data.length-1][0] - _data[_data.length-1][1]
        let previous1 = _data[_data.length-2][0] - _data[_data.length-2][1]
        let previous2 = _data[_data.length-3][0] - _data[_data.length-3][1]
        let positive = _data[_data.length-1][1] - _data[_data.length-2][1] 

        if(Math.abs(previous1) > barSize && Math.abs(previous2) > barSize && Math.abs(presentbarsize) > gain*Math.abs(previous1) && Math.abs(presentbarsize) > gain*Math.abs(previous2) && positive > 0 ){
            // let wick = params.data[4] - params.data[2]
            // console.log('found bullish engulfing')
            let diffbody_previouswick_1 = 0
            let diffbodytail_1 = 0
            let diffbody_previouswick_2 = 0
            let diffbodytail_2 = 0
            if(previous1 < 0){
                let previouswick_1 = _data[_data.length-2][3] -  _data[_data.length-2][1]
                diffbody_previouswick_1 = 100-((Math.abs(previous1) - Math.abs(previouswick_1))*100/Math.abs(previous1))
                let previoustail_1 = _data[_data.length-2][2] -  _data[_data.length-2][0]
                diffbodytail_1 = 100-((Math.abs(previous1) - Math.abs(previoustail_1))*100/Math.abs(previous1))
                // console.log('แท่ง1')
                // console.log(previous1 + ' ' +previouswick_1 + ' ' + diffbody_previouswick_1 + ' ' + diffbodytail_1 )
                
            }else{
                let previouswick_1 = _data[_data.length-2][3] -  _data[_data.length-2][0]
                diffbody_previouswick_1 = 100-((Math.abs(previous1) - Math.abs(previouswick_1))*100/Math.abs(previous1))
                let previoustail_1 = _data[_data.length-2][2] -  _data[_data.length-2][1]
                diffbodytail_1 = 100-((Math.abs(previous1) - Math.abs(previoustail_1))*100/Math.abs(previous1))
                // console.log('แท่ง1')
                // console.log(previous1 + ' ' +previouswick_1 + ' ' + diffbody_previouswick_1 + ' ' + diffbodytail_1 )
               
            }

            if(previous2 < 0){
                let previouswick_2 = _data[_data.length-3][3] -  _data[_data.length-3][1]
                diffbody_previouswick_2 = 100-((Math.abs(previous2) - Math.abs(previouswick_2))*100/Math.abs(previous2))
    
                let previoustail_2 = _data[_data.length-3][2] -  _data[_data.length-3][0]
                diffbodytail_2 = 100-((Math.abs(previous2) - Math.abs(previoustail_2))*100/Math.abs(previous2))
                // console.log('แท่ง2')
                // console.log(previous2 + ' ' +previouswick_2 + ' ' + diffbody_previouswick_2 + ' ' + diffbodytail_2 )
             
            }else{
                let previouswick_2 = _data[_data.length-3][3] -  _data[_data.length-3][0]
                diffbody_previouswick_2 = 100-((Math.abs(previous2) - Math.abs(previouswick_2))*100/Math.abs(previous2))
    
                let previoustail_2 = _data[_data.length-3][2] -  _data[_data.length-3][1]
                diffbodytail_2 = 100-((Math.abs(previous2) - Math.abs(previoustail_2))*100/Math.abs(previous2))
                // console.log('แท่ง2')
                // console.log(previous2 + ' ' +previouswick_2 + ' ' + diffbody_previouswick_2 + ' ' + diffbodytail_2 ) 
            }
            
            if(diffbody_previouswick_1 < 150 && diffbodytail_1 < 150 && diffbody_previouswick_2 < 150 && diffbodytail_2 < 150){
                console.log('found bullish engulfing 555')
                return true
            }else{
                return false
            }
            
        }else{
            // console.log('not good')
            return false
        }

    }

    function momentumBarDown(_data,_barSize,barSizeRatio,gain){
        let barSize = _barSize*barSizeRatio
        // console.log('barSize' + barSize)
        let presentbarsize = _data[_data.length-1][0] - _data[_data.length-1][1]
        let previous1 = _data[_data.length-2][0] - _data[_data.length-2][1]
        let previous2 = _data[_data.length-3][0] - _data[_data.length-3][1]
        let negative = _data[_data.length-1][1] - _data[_data.length-2][1] 

        if(Math.abs(previous1) > barSize && Math.abs(previous2) > barSize && Math.abs(presentbarsize) > gain*Math.abs(previous1) && Math.abs(presentbarsize) > gain*Math.abs(previous2) && negative < 0){
            console.log('bearish engulfing')
            return true
        }else{
            // console.log('not good')
            return false
        }
    }


    function isContinuityDownTrend(_data,sma100,trend){
        let uptren0 = _data[_data.length-1][2] -  sma100[sma100.length-1] 
        let uptren1 = _data[_data.length-2][2] - sma100[sma100.length-2]
        let uptren2 = _data[_data.length-3][2]  - sma100[sma100.length-3]   

        if(uptren0 > uptren1 && uptren1 > uptren2){
            return true
        }else {
            return false
        }
    }

    function isCorrectWickTail(data,percent){
        presentarr = data.filter((ohlc,idx) => idx < 4)
        let sorted = sortArr(presentarr);
        let body = sorted[2]-sorted[1]
        let wick = sorted[3]-sorted[2]
        let tail = sorted[1]-sorted[0]

        // console.log(data)
        
        
        let diffbodywick = 100-((body - wick)*100/body)
        let diffbodytail = 100-((body - tail)*100/body)

        // console.log(diffbodywick + ' yyy ' + diffbodytail)

        if (diffbodywick <= percent && diffbodytail <= percent) {
            
            return true;
        }
        return false;
    }

    function sortArr(numArray){
        numArray.sort(function(a, b) {
        return a - b;
        });
        return numArray;
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


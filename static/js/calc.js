    var upColor = '#00da3c';
    var downColor = '#ec0000';
    
    function getData(rawData) {
        var _data = []
        rawData.forEach((item) => {
            _data.push(Object.seal([item.open,item.close,item.low,item.high]))
        });
        return _data;
    }
    function getClosedPrice(rawData) {
        var _closedprice = []
        rawData.forEach((item) => {
            _closedprice.push(item.close)
        });
        return _closedprice;
    }

    function getLowPrice(rawData) {
        var _lowprice = []
        rawData.forEach((item) => {
            _lowprice.push(item.low)
        });
        return _lowprice;
    }

    function getHighPrice(rawData) {
        var _highprice = []
        rawData.forEach((item) => {
            _highprice.push(item.high)
        });
        return _highprice;
    }

    function getDateLabel(rawData) {
        var _dateLabel = []
        rawData.forEach((item) => {
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


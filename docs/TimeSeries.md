### TimeSeries

#### [iOpen](https://www.mql5.com/pt/docs/series/iopen)

------------


*Returns the value of the opening price of the bar (indicated by the shift parameter) of the corresponding chart.*

iOpen(Symbol, Period, Shift)
 


Example:
```python
mql5.iOpen("BTCUSD", "M1", 0)
```

#### [iHigh](https://www.mql5.com/pt/docs/series/ihigh)

------------


*Returns the value of the opening price of the bar (indicated by the shift parameter) of the corresponding chart.*

iHigh(Symbol, Period, Shift)
 


Example:
```python
mql5.iHigh("BTCUSD", "M1", 0)
```


#### [iLow](https://www.mql5.com/pt/docs/series/ilow)

------------


*Returns the value of the opening price of the bar (indicated by the shift parameter) of the corresponding chart.*

iLow(Symbol, Period, Shift)
 


Example:
```python
mql5.iLow("BTCUSD", "M1", 0)
```


#### [iClose](https://www.mql5.com/pt/docs/series/iclose )

------------


*Returns the closing price value of the bar (indicated by the shift parameter) of the corresponding chart*

iClose(Symbol, Period, Shift)
 

Example:
```python
mql5.iClose("BTCUSD", "M1", 0)
```


#### [iTime](https://www.mql5.com/pt/docs/series/itime)

------------


*Returns the closing price value of the bar (indicated by the shift parameter) of the corresponding chart*

iTime(Symbol, Period, Shift)
 

Example:
```python
mql5.iTime("BTCUSD", "M1", 0)
```

#### [iVolume](https://www.mql5.com/pt/docs/series/irealvolume)

------------

*Returns the closing price value of the bar (indicated by the shift parameter) of the corresponding chart*

iVolume(Symbol, Period, Shift)

Example:
```python
mql5.iVolume("BTCUSD", "M1", 0)
```

#### [CopyTicks](https://www.mql5.com/pt/docs/series/copyticks)

------------


CopyTicks(Symbol, Start_Time_MSC, Count)

Example:
```python
mql5.CopyTicks("BTCUSD", 0, 10) # Returns the last 10 ticks(TimesAndTrades)
```

#### [CopyTicksRange](https://www.mql5.com/pt/docs/series/copyticksrange)

------------
**Returns the **

CopyTicksRange(Symbol, Start_Time_MSC, Stop_Time_MSC)

Example:
```python
mql5.CopyTicksRange("BTCUSD", 1563791171058,1563791171221)
```

#### [CopyRates](https://www.mql5.com/pt/docs/series/copyrates)

------------
*Gets historical data from the **[MQLRates](https://www.mql5.com/en/docs/constants/structures/mqlrates)** structure for a specified symbol-period in the specified quantity. The sorting of the copied data elements is from the present to the past, i.e. the start position 0 means the current bar.*


**CopyRates(Symbol, Period, Start_Pos, Count)** - Returns an array of type MQLRates(Candles), with the start candle number and quantity specified.
**CopyRatesTC(Symbol, Period, Start_Time, Count)** - Returns an array of type MQLRates(Candles), with the start candle date and time and quantity specified.
**CopyRatesTT(Symbol, Period, Start_Time, Stop_Time)** - Returns an array of type MQLRates(Candles), with a specified date and time range.
Example:
```python
mql5.CopyRates("BTCUSD", "D1", 0, 10)
```
```python
mql5.CopyRatesTC("BTCUSD", "M15", "2019.07.18 10:00:00", 10)
```
```python
mql5.CopyRatesTT("BTCUSD", "M1", "2019.07.18 10:00:00", "2019.07.18 10:10:00")
```

#### [CopyOpen](https://www.mql5.com/pt/docs/series/copyopen)

------------
*The function gets an array of type **Double**, of historical data of bar opening prices for the selected asset-period pair in the specified quantity. It should be noted that the ordering of the elements is from the present to the past, i.e. the starting position 0 means the current bar.*

**CopyOpen(Symbol, Period, Start_Pos, Count)** - Returns a double array with the opening prices of the candles, with the start candle number and quantity specified.
**CopyOpenTC(Symbol, Period, Start_Time, Count)** - Returns a double array with the opening prices of the candles, with the date and time of the start candle and quantity specified.
**CopyOpenTT(Symbol, Period, Start_Time, Stop_Time)** - Returns a double array with the opening prices of the candles, with a specified date and time range.
Example:
```python
mql5.CopyOpen("BTCUSD", "D1", 0, 10)
```
```python
mql5.CopyOpenTC("BTCUSD", "M15", "2019.07.18 10:00:00", 10)
```
```python
mql5.CopyOpenTT("BTCUSD", "M1", "2019.07.18 10:00:00", "2019.07.18 10:10:00")
```
#### [CopyHigh](https://www.mql5.com/pt/docs/series/copyhigh)

------------
*The function gets an array of type **Double**, of historical data of the highest bar prices for the selected asset-period pair in the specified quantity. It should be noted that the ordering of the elements is from the present to the past, i.e. the starting position 0 means the current bar.*

**CopyHigh(Symbol, Period, Start_Pos, Count)** - Returns a double array with the maximum prices of the candles, with the start candle number and quantity specified.
**CopyHighTC(Symbol, Period, Start_Time, Count)** - Returns a double array with the maximum prices of the candles, with the date and time of the start candle and the specified quantity.
**CopyHighTT(Symbol, Period, Start_Time, Stop_Time)** - Returns a double array with the maximum prices of the candles, with a specified date and time range.
Example:
```python
mql5.CopyHigh("BTCUSD", "D1", 0, 10)
```
```python
mql5.CopyHighTC("BTCUSD", "M15", "2019.07.18 10:00:00", 10)
```
```python
mql5.CopyHighTT("BTCUSD", "M1", "2019.07.18 10:00:00", "2019.07.18 10:10:00")
```

#### [CopyLow](https://www.mql5.com/pt/docs/series/copylow)

------------
*The function gets an array of type **Double**, of historical data of minimum bar prices for the selected asset-period pair in the specified quantity. It should be noted that the ordering of the elements is from the present to the past, i.e. the starting position 0 means the current bar.*

**CopyLow(Symbol, Period, Start_Pos, Count)** - Returns a double array with the minimum prices of the candles, with the start candle number and quantity specified.
**CopyLowTC(Symbol, Period, Start_Time, Count)** - Returns a double array with the minimum prices of the candles, with the date and time of the start candle and quantity specified.
**CopyLowTT(Symbol, Period, Start_Time, Stop_Time)** - Returns a double array with the minimum prices of the candles, with a specified date and time range.
Example:
```python
mql5.CopyLow("BTCUSD", "D1", 0, 10)
```
```python
mql5.CopyLowTC("BTCUSD", "M15", "2019.07.18 10:00:00", 10)
```
```python
mql5.CopyLowTT("BTCUSD", "M1", "2019.07.18 10:00:00", "2019.07.18 10:10:00")
```

#### [CopyClose](https://www.mql5.com/pt/docs/series/copyclose)

------------
*The function gets an array of type **Double** of historical data of bar closing prices for the selected asset-period pair in the specified quantity. It should be noted that the ordering of the elements is from the present to the past, i.e. the starting position 0 means the current bar.*

**CopyClose(Symbol, Period, Start_Pos, Count)**- Returns a double array with the closing prices of the candles, with the start candle number and quantity specified.
**CopyCloseTC(Symbol, Period, Start_Time, Count)**- Returns a double array with the closing prices of the candles, with the date and time of the start candle and quantity specified.
**CopyCloseTT(Symbol, Period, Start_Time, Stop_Time)** - Returns a double array with the closing prices of the candles, with a specified date and time range.
Example:
```python
mql5.CopyClose("BTCUSD", "D1", 0, 10)
```
```python
mql5.CopyCloseTC("BTCUSD", "M15", "2019.07.18 10:00:00", 10)
```
```python
mql5.CopyCloseTT("BTCUSD", "M1", "2019.07.18 10:00:00", "2019.07.18 10:10:00")
```

#### [CopyVolume](https://www.mql5.com/pt/docs/series/copyrealvolume)

------------
*The function gets an array of type **int** of historical data on trading volumes for the selected asset-period pair in the specified quantity. It should be noted that the ordering of the elements is from the present to the past, i.e. the starting position 0 means the current bar.*

**CopyVolume(Symbol, Period, Start_Pos, Count)** - Returns an array of type ulong with the volumes of the candles, with the start candle number and quantity specified.
**CopyVolumeTC(Symbol, Period, Start_Time, Count)** - Returns an array of type ulong with the volumes of the candles, with the date and time of the start candle and the specified quantity.
**CopyVolumeTT(Symbol, Period, Start_Time, Stop_Time)**- Returns an array of type ulong with the volumes of the candles, with a specified date and time range.
Example:
```python
mql5.CopyVolume("BTCUSD", "D1", 0, 10)
```
```python
mql5.CopyVolumeTC("BTCUSD", "M15", "2019.07.18 10:00:00", 10)
```
```python
mql5.CopyVolumeTT("BTCUSD", "M1", "2019.07.18 10:00:00", "2019.07.18 10:10:00")
```


#### [Type MQLRates](https://www.mql5.com/pt/docs/constants/structures/mqlrates)
------------
*The MQLRates Type is a dictionary that has the following model:*
```python
 {
 	'TIME': date, # Start time of period
	'OPEN': float, # Opening price
	'HIGH': float, # The highest price of the period
	'LOW': float, # The lowest price of the period
	'CLOSE': float, # Closing price
	'TICK_VOLUME': int, # Tick Volume
	'SPREAD': int, # Spread
	'REAL_VOLUME': int # Trading volume
}
```

#### [MQLTick Type](https://www.mql5.com/pt/docs/constants/structures/mqltick)
------------
*The MQLTick Type is a dictionary that has the following model:*
```python
{
	'TIME': date, # Time of last price update
	'BID': float(i[1]), # Current ask price
	'ASK': float(i[2]), # Current bid price
	'LAST': float(i[3]), # Last trade price (last price)
	'VOLUME': float(i[4]), # Volume for the current last price
	'TIME_MSC': int(i[5]), # Time of "Last" price update in milliseconds
	'FLAGS': int(i[6]), # Tick flags
	'VOLUME_REAL': float(i[7]) # Volume for current Last price with higher precision
}
```

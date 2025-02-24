//+------------------------------------------------------------------+
//|                                            stream-handlers.mqh   |
//+------------------------------------------------------------------+
#property copyright "QuantsPub"
#property version "0.1"

#include <MT5Ext\utils.mqh>

void GetLatestTick(const string &symbol) {
    MqlTick lastTick;
    if (SymbolInfoTick(symbol, lastTick)) {
        string parameters[] = {
            IntegerToString(lastTick.time),
            DoubleToString(lastTick.bid, 5),
            DoubleToString(lastTick.ask, 5),
            DoubleToString(lastTick.last, 5),
            IntegerToString(lastTick.volume)
        };
        string tickString = MakeMessage("F020", "6", parameters);
        BroadcastStreamData(tickString);
    }
}

void GetLatestBar(const string &symbol, datetime &lastBarTime) {
    // Detect new bar
    datetime currentBarTime = iTime(symbol, PERIOD_CURRENT, 0);
    if (currentBarTime > lastBarTime) {
        lastBarTime = currentBarTime;
        double open = iOpen(symbol, PERIOD_CURRENT, 0);
        double high = iHigh(symbol, PERIOD_CURRENT, 0);
        double low = iLow(symbol, PERIOD_CURRENT, 0);
        double close = iClose(symbol, PERIOD_CURRENT, 0);
        long volume = iVolume(symbol, PERIOD_CURRENT, 0);
        
        string parameters[] = {
            IntegerToString(currentBarTime),
            DoubleToString(open, 5),
            DoubleToString(high, 5),
            DoubleToString(low, 5),
            DoubleToString(close, 5),
            IntegerToString(volume)
        };
        string barString = MakeMessage("F021", "6", parameters);
        BroadcastStreamData(barString);
    }
}

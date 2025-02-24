//+------------------------------------------------------------------+
//|                                            MT5Ext.mqh            |
//+------------------------------------------------------------------+
#property copyright "QuantsPub"
#property version "0.1"

#include <MT5Ext\utils.mqh>

// 
// Various helper functions
// 
string GetBrokerServerTime()
{
    string parameters[] = { IntegerToString(TimeCurrent()) };
    return MakeMessage("F005", "1", parameters);
}

string GetCheckConnection()
{
    string parameters[] = { "OK" };
    return MakeMessage("F000", "1", parameters);
}

string GetStaticAccountInfo()
{
    string parameters[] = {
        AccountInfoString(ACCOUNT_NAME),
        IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN)),
        AccountInfoString(ACCOUNT_CURRENCY),
        IntegerToString(AccountInfoInteger(ACCOUNT_TRADE_MODE)),
        IntegerToString(AccountInfoInteger(ACCOUNT_LEVERAGE)),
        BoolToString((bool)AccountInfoInteger(ACCOUNT_TRADE_ALLOWED)),
        IntegerToString(AccountInfoInteger(ACCOUNT_LIMIT_ORDERS)),
        DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN_SO_CALL)),
        DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN_SO_SO)),
        AccountInfoString(ACCOUNT_COMPANY)
    };
    return MakeMessage("F001", "10", parameters);
}

string GetDynamicAccountInfo()
{
    string parameters[] = {
        DoubleToString(AccountInfoDouble(ACCOUNT_BALANCE), 2),
        DoubleToString(AccountInfoDouble(ACCOUNT_EQUITY), 2),
        DoubleToString(AccountInfoDouble(ACCOUNT_PROFIT), 2),
        DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN), 2),
        DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN_LEVEL), 2),
        DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN_FREE), 2)
    };
    return MakeMessage("F002", "6", parameters);
}

string GetInstrumentInfo(string symbol)
{
    string parameters[] = {
        symbol,
        DoubleToString(SymbolInfoDouble(symbol, SYMBOL_BID), 5),
        DoubleToString(SymbolInfoDouble(symbol, SYMBOL_ASK), 5)
    };
    return MakeMessage("F003", "3", parameters);
}

string GetBrokerInstrumentNames()
{
    string parameters[] = { TerminalInfoString(TERMINAL_NAME) };
    return MakeMessage("F007", "1", parameters);
}

string CheckMarketWatch(string symbol)
{
    bool isWatched = SymbolSelect(symbol, true);
    string parameters[] = { isWatched ? "YES" : "NO" };
    return MakeMessage("F004", "1", parameters);
}

string CheckTradingAllowed(string symbol)
{
    bool tradingAllowed = SymbolInfoInteger(symbol, SYMBOL_TRADE_MODE) != SYMBOL_TRADE_MODE_DISABLED;
    string parameters[] = { tradingAllowed ? "YES" : "NO" };
    return MakeMessage("F008", "1", parameters);
}

string CheckTerminalServerConnection()
{
    string parameters[] = { TerminalInfoInteger(TERMINAL_CONNECTED) ? "CONNECTED" : "DISCONNECTED" };
    return MakeMessage("F011", "1", parameters);
}

string CheckTerminalType()
{
    string parameters[] = { TerminalInfoString(TERMINAL_NAME) };
    return MakeMessage("F012", "1", parameters);
}

string GetLastTickInfo(string symbol)
{
    string errorParameters[] = { "ERROR" };

    // Make the symbol uppercase and standardized
    if (!StringToUpper(symbol)) {
        return MakeMessage("F020", "1", errorParameters);
    }
    SymbolSelect(symbol, true);

    MqlTick lastTick;
    if (SymbolInfoTick(symbol, lastTick))
    {
        string parameters[] = {
            IntegerToString(lastTick.time),
            DoubleToString(lastTick.bid, 5),
            DoubleToString(lastTick.ask, 5),
            DoubleToString(lastTick.last, 5),
            IntegerToString(lastTick.volume),
            IntegerToString(SymbolInfoInteger(symbol, SYMBOL_SPREAD)),
            IntegerToString(lastTick.time_msc),
        };
        return MakeMessage("F020", "6", parameters);
    }
    return MakeMessage("F020", "1", errorParameters);
}

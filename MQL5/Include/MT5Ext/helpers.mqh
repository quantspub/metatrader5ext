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
    string serverTimeString = "F005^1^" + IntegerToString(TimeCurrent());
    return serverTimeString;
}

string GetCheckConnection()
{
    return "F000^1^OK";
}

string GetStaticAccountInfo()
{
    string accountInfo = "F001^10^" + AccountInfoString(ACCOUNT_NAME) + "^" +
                         IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN)) + "^" +
                         AccountInfoString(ACCOUNT_CURRENCY) + "^" +
                         IntegerToString(AccountInfoInteger(ACCOUNT_TRADE_MODE)) + "^" +
                         IntegerToString(AccountInfoInteger(ACCOUNT_LEVERAGE)) + "^" +
                         BoolToString((bool)AccountInfoInteger(ACCOUNT_TRADE_ALLOWED)) + "^" +
                         IntegerToString(AccountInfoInteger(ACCOUNT_LIMIT_ORDERS)) + "^" +
                         DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN_SO_CALL)) + "^" +
                         DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN_SO_SO)) + "^" +
                         AccountInfoString(ACCOUNT_COMPANY) + "^";
    return accountInfo;
}

string GetDynamicAccountInfo()
{
    string accountData = "F002^6^" + DoubleToString(AccountInfoDouble(ACCOUNT_BALANCE), 2) + "^" +
                         DoubleToString(AccountInfoDouble(ACCOUNT_EQUITY), 2) + "^" +
                         DoubleToString(AccountInfoDouble(ACCOUNT_PROFIT), 2) + "^" +
                         DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN), 2) + "^" +
                         DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN_LEVEL), 2) + "^" +
                         DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN_FREE), 2) + "^";
    return accountData;
}

string GetInstrumentInfo(string symbol)
{
    string instrumentInfo = "F003^3^" + symbol + "^" +
                            DoubleToString(SymbolInfoDouble(symbol, SYMBOL_BID), 5) + "^" +
                            DoubleToString(SymbolInfoDouble(symbol, SYMBOL_ASK), 5) + "^";
    return instrumentInfo;
}

string GetBrokerInstrumentNames()
{
    string instruments = "F007^1^" + TerminalInfoString(TERMINAL_NAME);
    return instruments;
}

string CheckMarketWatch(string symbol)
{
    bool isWatched = SymbolSelect(symbol, true);
    return "F004^1^" + (isWatched ? "YES" : "NO");
}

string CheckTradingAllowed(string symbol)
{
    bool tradingAllowed = SymbolInfoInteger(symbol, SYMBOL_TRADE_MODE) != SYMBOL_TRADE_MODE_DISABLED;
    return "F008^1^" + (tradingAllowed ? "YES" : "NO");
}

string CheckTerminalServerConnection()
{
    return "F011^1^" + (TerminalInfoInteger(TERMINAL_CONNECTED) ? "CONNECTED" : "DISCONNECTED");
}

string CheckTerminalType()
{
    return "F012^1^" + TerminalInfoString(TERMINAL_NAME);
}

string GetLastTickInfo()
{
    MqlTick lastTick;
    if (SymbolInfoTick(_Symbol, lastTick))
    {
        string tickInfo = "F020^6^" + IntegerToString(lastTick.time) + "^" +
                          DoubleToString(lastTick.bid, 5) + "^" +
                          DoubleToString(lastTick.ask, 5) + "^" +
                          DoubleToString(lastTick.last, 5) + "^" +
                          IntegerToString(lastTick.volume) + "^";
        return tickInfo;
    }
    return "F020^1^ERROR";
}

// Helper function to convert bool to string
string BoolToString(bool value)
{
    return value ? "true" : "false";
}


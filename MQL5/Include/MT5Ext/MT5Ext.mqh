//+------------------------------------------------------------------+
//|                                            MT5Ext.mqh            |
//+------------------------------------------------------------------+
#property copyright "QuantsPub"
#property version "0.1"

#include <MT5Ext\socket-library-mt4-mt5.mqh>

ServerSocket restServer;
ServerSocket streamingServer;
ClientSocket streamingClients[];  // Store connected clients for streaming


// TODO: use utf instead of ASCII 

// Create a new server socket for REST and streaming servers
void StartServers(ushort restPort, ushort streamPort, bool ForLocalhostOnly = true)
{
    restServer = new ServerSocket(restPort, ForLocalhostOnly);
    if (!restServer.Created())
    {
        Print("Failed to create REST server socket on port ", restPort);
    }
    else
    {
        Print("MQL5 REST server started on port ", restPort);
    }

    streamingServer = new ServerSocket(streamPort, true);
    if (!streamingServer.Created())
    {
        Print("Failed to create streaming server socket on port ", streamPort);
    }
    else
    {
        Print("MQL5 streaming server started on port ", streamPort);
    }
}

// close and delete the server sockets
void CloseServers()
{
    if (restServer != NULL)
    {
        restServer.Close();
        delete restServer;
    }

    if (streamingServer != NULL)
    {
        streamingServer.Close();
        delete streamingServer;
    }
}

// Function to encode strings using a predefined alphabet-number mapping
uchar[] EncodeString(string input)
{
    uchar encoded[];
    for (int i = 0; i < StringLen(input); i++)
    {
        uchar ch = (uchar)StringGetCharacter(input, i);
        ArrayResize(encoded, ArraySize(encoded) + 1);
        encoded[ArraySize(encoded) - 1] = ch + 42;  // Simple shift encoding
    }
    return encoded;
}


// Various helper functions
uchar[] GetBrokerServerTime()
{
    string serverTimeString = "F005^1^" + IntegerToString(TimeCurrent());
    return EncodeString(serverTimeString);
}

uchar[] GetCheckConnection()
{
    return EncodeString("F000^1^OK");
}

uchar[] GetStaticAccountInfo()
{
    string accountInfo = "F001^10^" + AccountInfoString(ACCOUNT_NAME) + "^" +
                         IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN)) + "^" +
                         AccountInfoString(ACCOUNT_CURRENCY) + "^" +
                         IntegerToString(AccountInfoInteger(ACCOUNT_TRADE_MODE)) + "^" +
                         IntegerToString(AccountInfoInteger(ACCOUNT_LEVERAGE)) + "^" +
                         BoolToString(AccountInfoInteger(ACCOUNT_TRADE_ALLOWED)) + "^" +
                         IntegerToString(AccountInfoInteger(ACCOUNT_LIMIT_ORDERS)) + "^" +
                         IntegerToString(AccountInfoInteger(ACCOUNT_MARGIN_SO_CALL)) + "^" +
                         IntegerToString(AccountInfoInteger(ACCOUNT_MARGIN_SO_SO)) + "^" +
                         AccountInfoString(ACCOUNT_COMPANY) + "^";
    return EncodeString(accountInfo);
}

uchar[] GetDynamicAccountInfo()
{
    string accountData = "F002^6^" + DoubleToString(AccountInfoDouble(ACCOUNT_BALANCE), 2) + "^" +
                         DoubleToString(AccountInfoDouble(ACCOUNT_EQUITY), 2) + "^" +
                         DoubleToString(AccountInfoDouble(ACCOUNT_PROFIT), 2) + "^" +
                         DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN), 2) + "^" +
                         DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN_LEVEL), 2) + "^" +
                         DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN_FREE), 2) + "^";
    return EncodeString(accountData);
}

uchar[] GetInstrumentInfo(string symbol)
{
    string instrumentInfo = "F003^3^" + symbol + "^" +
                            DoubleToString(SymbolInfoDouble(symbol, SYMBOL_BID), 5) + "^" +
                            DoubleToString(SymbolInfoDouble(symbol, SYMBOL_ASK), 5) + "^";
    return EncodeString(instrumentInfo);
}

uchar[] GetBrokerInstrumentNames()
{
    string instruments = "F007^1^" + TerminalInfoString(TERMINAL_NAME);
    return EncodeString(instruments);
}

uchar[] CheckMarketWatch(string symbol)
{
    bool isWatched = SymbolSelect(symbol, true);
    return EncodeString("F004^1^" + (isWatched ? "YES" : "NO"));
}

uchar[] CheckTradingAllowed(string symbol)
{
    bool tradingAllowed = SymbolInfoInteger(symbol, SYMBOL_TRADE_MODE) != SYMBOL_TRADE_MODE_DISABLED;
    return EncodeString("F008^1^" + (tradingAllowed ? "YES" : "NO"));
}

uchar[] CheckTerminalServerConnection()
{
    return EncodeString("F011^1^" + (TerminalInfoInteger(TERMINAL_CONNECTED) ? "CONNECTED" : "DISCONNECTED"));
}

uchar[] CheckTerminalType()
{
    return EncodeString("F012^1^" + TerminalInfoString(TERMINAL_NAME));
}

uchar[] GetLastTickInfo()
{
    MqlTick lastTick;
    if (SymbolInfoTick(_Symbol, lastTick))
    {
        string tickInfo = "F020^6^" + IntegerToString(lastTick.time) + "^" +
                          DoubleToString(lastTick.bid, 5) + "^" +
                          DoubleToString(lastTick.ask, 5) + "^" +
                          DoubleToString(lastTick.last, 5) + "^" +
                          IntegerToString(lastTick.volume) + "^";
        return EncodeString(tickInfo);
    }
    return EncodeString("F020^1^ERROR");
}

void BroadcastStreamingData(const uchar &data[])
{
    for (int i = 0; i < ArraySize(streamingClients); i++)
    {
        if (streamingClients[i].IsConnected())
        {
            streamingClients[i].Send(data);
        }
    }
}

#include <socket-library-mt4-mt5.mqh>

// Function to compress a string using a basic run-length encoding (RLE) algorithm
uchar[] CompressString(string input)
{
    uchar compressed[];
    int len = StringLen(input);
    int count = 1;
    
    for (int i = 0; i < len; i++)
    {
        uchar ch = (uchar)StringGetCharacter(input, i);
        ArrayResize(compressed, ArraySize(compressed) + 1);
        compressed[ArraySize(compressed) - 1] = ch;
        
        if (i + 1 < len && input[i] == input[i + 1])
        {
            count++;
        }
        else
        {
            ArrayResize(compressed, ArraySize(compressed) + 1);
            compressed[ArraySize(compressed) - 1] = (uchar)count;
            count = 1;
        }
    }
    return compressed;
}

// Function to encode and compress strings
uchar[] EncodeString(string input)
{
    uchar encoded[];
    uchar compressed[] = CompressString(input);
    
    for (int i = 0; i < ArraySize(compressed); i++)
    {
        uchar ch = compressed[i] + 42;  // Simple shift encoding
        ArrayResize(encoded, ArraySize(encoded) + 1);
        encoded[ArraySize(encoded) - 1] = ch;
    }
    return encoded;
}



void ProcessClient(Socket &client)
{
    uchar buffer[1024];
    int received = client.Receive(buffer);

    if (received > 0)
    {
        string request = CharArrayToString(buffer, received);
        uchar response[];

        if (request == "F000^1^")
        {
            response = GetCheckConnection();
        }
        else if (request == "F001^1^")
        {
            response = GetStaticAccountInfo();
        }
        else if (request == "F002^1^")
        {
            response = GetDynamicAccountInfo();
        }
        else if (request == "F003^2^")
        {
            response = GetInstrumentInfo(_Symbol);
        }
        else if (request == "F007^1^")
        {
            response = GetBrokerInstrumentNames();
        }
        else if (request == "F004^2^")
        {
            response = CheckMarketWatch(_Symbol);
        }
        else if (request == "F008^2^")
        {
            response = CheckTradingAllowed(_Symbol);
        }
        else if (request == "F011^1^")
        {
            response = CheckTerminalServerConnection();
        }
        else if (request == "F012^1^")
        {
            response = CheckTerminalType();
        }
        else if (request == "F020^2^")
        {
            response = GetLastTickInfo();
        }
        else if (request == "F005^1^")
        {
            response = GetBrokerServerTime();
        }
        else
        {
            response = EncodeString("F999^1^UNKNOWN_REQUEST");
        }

        if (ONLY_STREAM_MODE)
        {
            BroadcastStreamingData(response);
        }
        else
        {
            client.Send(response);
        }
    }
}

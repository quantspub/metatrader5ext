//+------------------------------------------------------------------+
//|                                            MT5Ext.mqh            |
//+------------------------------------------------------------------+
#property copyright "QuantsPub"
#property version "0.1"

#include <MT5Ext\socket-library-mt4-mt5.mqh>
#include <MT5Ext\utils.mqh>

ServerSocket *restServer;
ServerSocket *streamingServer;
ClientSocket *streamingClients[];  // Store connected clients for streaming

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

// Close and delete the server sockets
void CloseServers()
{
    if (restServer != NULL)
    {
        delete restServer;
    }

    if (streamingServer != NULL)
    {
        delete streamingServer;
    }

    for (int i = 0; i < ArraySize(streamingClients); i++)
    {
        delete streamingClients[i];
    }
}

void AcceptClients(bool onlyStream)
{
    if (restServer != NULL)
    {
        ClientSocket *client = restServer.Accept();
        if (client != NULL && client.IsSocketConnected())
        {
            ProcessClient(*client, onlyStream);
            delete client;
        }
    }

    if (streamingServer != NULL)
    {
        ClientSocket *newClient = streamingServer.Accept();
        if (newClient != NULL && newClient.IsSocketConnected())
        {
            Print("New streaming client connected: ", newClient);
            ArrayResize(streamingClients, ArraySize(streamingClients) + 1);
            streamingClients[ArraySize(streamingClients) - 1] = newClient;
        }
    }
}


void ProcessClient(ClientSocket &client, bool onlyStream)
{
    uchar buffer[1024];
    int received = client.Receive(buffer);

    if (received > 0)
    {
        string request = CharArrayToString(buffer, received);
        string response;

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
            response = "F999^1^UNKNOWN_REQUEST";
        }

        if (onlyStream)
        {
            BroadcastStreamingData(response);
        }
        else
        {
            client.Send(response);
        }
    }
}

void BroadcastStreamingData(const string &data)
{
    for (int i = 0; i < ArraySize(streamingClients); i++)
    {
        if (streamingClients[i].IsSocketConnected())
        {
            streamingClients[i].Send(data);
        }
    }
}

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


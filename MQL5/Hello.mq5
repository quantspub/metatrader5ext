#include <MT5Ext/socket-library-mt4-mt5.mqh>

input int restServerPort = 1111;   // REST server for commands
input int streamingServerPort = 2222; // Streaming server for real-time data and responses
input int timerInterval = 1;    // Timer interval for the REST server
input bool onlyStreamMode = false; // If enabled, responses will be sent via stream server

datetime lastBarTime = 0;

ServerSocket restServer;
ServerSocket streamingServer;
Socket streamingClients[];  // Store connected clients for streaming

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

        if (onlyStreamMode)
        {
            BroadcastStreamingData(response);
        }
        else
        {
            client.Send(response);
        }
    }
}

void OnInit()
{
    restServer = new ServerSocket(restServerPort, true);
    if (!restServer.Created())
    {
        Print("Failed to create REST server socket on port ", restServerPort);
        return;
    }
    Print("MQL5 REST server started on port ", restServerPort);

    streamingServer = new ServerSocket(streamingServerPort, true);
    if (!streamingServer.Created())
    {
        Print("Failed to create streaming server socket on port ", streamingServerPort);
        return;
    }
    Print("MQL5 streaming server started on port ", streamingServerPort);

    lastBarTime = iTime(_Symbol, PERIOD_CURRENT, 0);
    EventSetTimer(timerInterval);
}

void OnDeinit(const int reason)
{
    EventKillTimer();
    
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

void OnTimer()
{
    if (restServer != NULL)
    {
        Socket client = restServer.Accept();
        if (client.IsConnected())
        {
            ProcessClient(client);
            client.Close();
        }
    }

    if (streamingServer != NULL)
    {
        Socket newClient = streamingServer.Accept();
        if (newClient.IsConnected())
        {
            Print("New streaming client connected: ", newClient.RemoteAddress());
            ArrayResize(streamingClients, ArraySize(streamingClients) + 1);
            streamingClients[ArraySize(streamingClients) - 1] = newClient;
        }
    }
}

void OnTick()
{
    MqlTick lastTick;
    if (SymbolInfoTick(_Symbol, lastTick))
    {
        uchar tickData[];
        string tickString = "F020^6^" + IntegerToString(lastTick.time) + "^" +
                            DoubleToString(lastTick.bid, 5) + "^" +
                            DoubleToString(lastTick.ask, 5) + "^" +
                            DoubleToString(lastTick.last, 5) + "^" +
                            IntegerToString(lastTick.volume) + "^";
        tickData = EncodeString(tickString);
        BroadcastStreamingData(tickData);
    }
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

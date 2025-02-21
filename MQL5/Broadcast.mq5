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
    
    // Detect new bar
    datetime currentBarTime = iTime(_Symbol, PERIOD_CURRENT, 0);
    if (currentBarTime > lastBarTime)
    {
        lastBarTime = currentBarTime;
        double open = iOpen(_Symbol, PERIOD_CURRENT, 0);
        double high = iHigh(_Symbol, PERIOD_CURRENT, 0);
        double low = iLow(_Symbol, PERIOD_CURRENT, 0);
        double close = iClose(_Symbol, PERIOD_CURRENT, 0);
        long volume = iVolume(_Symbol, PERIOD_CURRENT, 0);
        
        string barString = "F021^6^" + IntegerToString(currentBarTime) + "^" +
                           DoubleToString(open, 5) + "^" +
                           DoubleToString(high, 5) + "^" +
                           DoubleToString(low, 5) + "^" +
                           DoubleToString(close, 5) + "^" +
                           IntegerToString(volume) + "^";
        uchar barData[] = EncodeString(barString);
        BroadcastStreamingData(barData);
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

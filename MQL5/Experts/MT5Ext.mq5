//+------------------------------------------------------------------+
//|                                            MT5Ext.mq5            |
//+------------------------------------------------------------------+
#property copyright "QuantsPub"
#property version "0.1"

#include <MT5Ext\MT5Ext.mqh>

input ushort REST_SERVER_PORT = 1111;   // REST server for commands
input ushort STREAM_SERVER_PORT = 2222; // Streaming server for real-time data and responses
input int TIMER_INTERVAL = 1;    // Timer interval for the REST server
input bool ONLY_STREAM_MODE = false; // If enabled, responses will be sent via stream server

datetime lastBarTime = 0;

void OnInit()
{
    StartServers(REST_SERVER_PORT, STREAM_SERVER_PORT, true);

    lastBarTime = iTime(_Symbol, PERIOD_CURRENT, 0);
    EventSetTimer(TIMER_INTERVAL);
}

void OnDeinit(const int reason)
{
    EventKillTimer();
    
    CloseServers();
    for (int i = 0; i < ArraySize(streamingClients); i++)
    {
        streamingClients[i].Close();
    }
}

void OnTimer()
{
    if (restServer != NULL)
    {
        ClientSocket *client = restServer.Accept();
        if (client != NULL && client.IsSocketConnected())
        {
            ProcessClient(*client);
            client.Close();
            delete client;
        }
    }

    if (streamingServer != NULL)
    {
        ClientSocket *newClient = streamingServer.Accept();
        if (newClient != NULL && newClient.IsSocketConnected())
        {
            Print("New streaming client connected: ", newClient.RemoteAddress());
            ArrayResize(streamingClients, ArraySize(streamingClients) + 1);
            streamingClients[ArraySize(streamingClients) - 1] = *newClient;
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

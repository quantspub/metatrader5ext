//+------------------------------------------------------------------+
//|                                      MT5Streamer.mq5             |
//+------------------------------------------------------------------+
#property copyright "Mita Platform"
#property version "0.2"

#include <MT5Streamer\Websockets.mqh>

#define DEBUG_PRINT true
#define MSVCRT_DLL

//+------------------------------------------------------------------+
// Global Variables
//+------------------------------------------------------------------+
input string SYMBOLS_LIST = "";         // List of tools
input int MILLISECONDS_PING_TIMER = 10; // Update period, ms
//---
input string SOCKET_OPTIONS = "=== TCP Socket ===";
input string HOST = "http://localhost"; //  hostname or IP address
input ushort PORT = 15557;              // port
input string CALLBACK_URL = "http://localhost/callback";
input string CALLBACK_FORMAT = "JSON";
input string URL_SWAGGER = "http://localhost:6542";
input string AUTH_TOKEN = "test-token";
input bool DEBUG = true;
//---
int COMMAND_WAIT_TIMEOUT = 10;

CWebsockets api;

int OnInit()
{
    api.Init(HOST, PORT, URL_SWAGGER, COMMAND_WAIT_TIMEOUT);
    api.SetCallback(CALLBACK_URL, CALLBACK_FORMAT);
    api.SetAuth(AUTH_TOKEN);

    if (!api.Listen())
    {
        if (DEBUG)
        {
            Print("Server socket FAILED - is the port already in use?");
        }

        return (INIT_FAILED);
    }

    EventSetMillisecondTimer(MILLISECONDS_PING_TIMER);

    if (DEBUG)
    {
        Print("Server Started...");
    }

    return (INIT_SUCCEEDED);
}

void OnDeinit(const int reason)
{

    EventKillTimer();

    api.Deinit();

    Print("Server Closed...");
}

void OnTimer()
{
    if (!TerminalInfoInteger(TERMINAL_CONNECTED))
        return;

    api.Processing();
}

void OnTradeTransaction(const MqlTradeTransaction &trans,
                        const MqlTradeRequest &request,
                        const MqlTradeResult &result)
{

    api.OnTradeTransaction(trans, request, result);
}
//+------------------------------------------------------------------+
//|                                      StreamerSockets.mq5             |
//+------------------------------------------------------------------+
//
//
// Overview workings:
// It uses two ports: server 1 port and server 2 port. A client trying to request data will have to create a server and broadcast the port of that server to it at the init handshake or along with each request.
// Then the response is streamed to the {server:port} broadcasted by the client.
//
// NOTE: It Can handle a maximum of 8 clients simultaneously.

#property copyright "Ramin Rostami"
#property version "0.2"

#include <Arrays\ArrayString.mqh>
#include <Arrays\List.mqh>
#include <MT5Streamer\socket-library-mt4-mt5.mqh>
#include <MT5Streamer\Json.mqh>

#define DEBUG_PRINT true
#define MSVCRT_DLL

//+------------------------------------------------------------------+
// Global Variables
//+------------------------------------------------------------------+
input string SYMBOLS_LIST = "";   // List of tools
input int MILLISECOND_TIMER = 25; // Update period, ms
//---
input string SOCKET_OPTIONS = "=== TCP Socket ===";
input ushort REQ_PORT = 15557;                    // Request port (Server 1 Port - This Server)
input string DEFAULT_CALLBACK_HOST = "127.0.0.1"; // Callback Server 2 hostname or IP address
input ushort DEFAULT_CALLBACK_PORT = 15558;       // Callback port (The Server 2 Port - Client)
input bool DEBUG = true;                          // Write to Socket

//+------------------------------------------------------------------+
// Server socket
ServerSocket *glbServerSocket = NULL;

// Array of current clients
ClientSocket *glbClients[16];

// Watch for need to create timer;
bool glbCreatedTimer = false;

// Variables for handling price data stream
struct RequestSubscription
{
    string host;
    ushort port;
    string command;
    string chartTf;
    datetime lastBar;
    ClientSocket *Socket;
};

RequestSubscription requestQueueSubscriptions[64];
int requestQueueSubscriptionCount = 0;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
    // Create the server socket
    glbServerSocket = new ServerSocket(REQ_PORT, false);
    if (!glbServerSocket.Created())
    {
        if (DEBUG)
        {
            Print("Server socket FAILED - is the port already in use?");
        }

        return INIT_FAILED;
    }

    // Note: this can fail if MT4/5 starts up
    // with the EA already attached to a chart. Therefore,
    // we repeat in OnTick()
    glbCreatedTimer = EventSetMillisecondTimer(MILLISECOND_TIMER);

    if (DEBUG)
    {
        Print("Server socket created \n Accepting new connections...");
    }

    return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
    EventKillTimer();

    // free server socket and any clients
    glbCreatedTimer = false;

    // Delete all clients currently connected
    for (int i = 0; i < ArraySize(requestQueueSubscriptions); i++)
    {
        if (requestQueueSubscriptions[i].Socket)
        {
            delete requestQueueSubscriptions[i].Socket;
            requestQueueSubscriptions[i].Socket = NULL;
        }
    }

    // Free the server socket
    if (!glbServerSocket)
    {
        Print("An error occurred while closing Socket...");
    }

    delete glbServerSocket;
    glbServerSocket = NULL;

    Print("Socket Closed...");
}

//+------------------------------------------------------------------+

void OnTimer()
{
    if (!TerminalInfoInteger(TERMINAL_CONNECTED))
        return;

    if (ProcessRequest() != INIT_SUCCEEDED)
        return;

    if (ProcessRequest() != INIT_SUCCEEDED)
        return;
}

// Use OnTick() to watch for failure to create the timer in OnInit()
void OnTick()
{
    if (!glbCreatedTimer)
        glbCreatedTimer = EventSetMillisecondTimer(MILLISECOND_TIMER);
}

//+------------------------------------------------------------------+

//+------------------------------------------------------------------+
//| Process incoming client requests                                 |
//+------------------------------------------------------------------+
int ProcessRequest()
{
    // Accept new client connections
    while (true)
    {
        ClientSocket *pNewClient = glbServerSocket.Accept();
        if (pNewClient == NULL)
            break;

        // Ensure there's room in the subscriptions array
        if (requestQueueSubscriptionCount < ArraySize(requestQueueSubscriptions))
        {
            // Get request from new client and add it to subscription

            // Read incoming data
            string RequestMsg = pNewClient.Receive();
            if (RequestMsg == "")
            {
                break;
            }
            Print("Received message: ", RequestMsg);

            CJAVal Request;

            if (!Request.Deserialize(RequestMsg))
            {
                if (DEBUG)
                {
                    Print("Failed to deserialize request: ", RequestMsg);
                }
                break;
            }

            // Handle specific commands
            if (Request == "q")
            {
                break;
            }

            // Initialize a new subscription
            RequestSubscription newSubscription;
            newSubscription.host = Request["host"].ToStr();
            if (newSubscription.host == "")
            {
                newSubscription.host = DEFAULT_CALLBACK_HOST;
            }
            newSubscription.port = (ushort)Request["port"].ToInt();
            if (newSubscription.port == 0)
            {
                newSubscription.port = DEFAULT_CALLBACK_PORT;
            }
            newSubscription.Socket = new ClientSocket(newSubscription.host, newSubscription.port);

            // Add to the subscriptions array
            requestQueueSubscriptions[requestQueueSubscriptionCount] = newSubscription;
            requestQueueSubscriptionCount++;

            Print("Connection received from ", newSubscription.host, ":", newSubscription.port);
            pNewClient.Send("Connected to the MT5 Server!\r\n");
        }
        else
        {
            Print("Maximum number of subscriptions reached. Connection refused.");
            delete pNewClient;
        }
    }

    // Process incoming data from clients
    for (int i = requestQueueSubscriptionCount - 1; i >= 0; i--)
    {
        RequestSubscription subscription = requestQueueSubscriptions[i];
        ClientSocket *pClient = subscription.Socket;

        if (pClient == NULL)
            continue;

        // Check if the client is still connected
        if (!pClient.IsSocketConnected())
        {
            Print("Client disconnected.");
            delete pClient;
            subscription.Socket = NULL;
            // Remove the subscription
            for (int j = i; j < requestQueueSubscriptionCount - 1; j++)
            {
                requestQueueSubscriptions[j] = requestQueueSubscriptions[j + 1];
            }
            requestQueueSubscriptionCount--;
            ArrayResize(requestQueueSubscriptions, requestQueueSubscriptionCount);
        }
    }

    return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
//| Stream data to subscribed clients                                |
//+------------------------------------------------------------------+
void ProcessResponse()
{
    // Stream data to clients
    for (int i = requestQueueSubscriptionCount - 1; i >= 0; i--)
    {
        RequestSubscription subscription = requestQueueSubscriptions[i];
        ClientSocket *pClient = subscription.Socket;

        if (pClient == NULL)
            continue;

        if (pClient.IsSocketConnected())
        {
            // TODO: Get action and send data to client
            Print("Streaming data to client at ", subscription.host, ":", subscription.port);
            // Prepare the data to be sent
            string jsonData = "{...}"; // Replace with actual data
            pClient.Send(jsonData);
        }
        else
        {
            Print("Client at ", subscription.host, ":", subscription.port, " is not connected.");
            delete pClient;
            subscription.Socket = NULL;
            // Remove the subscription
            for (int j = i; j < requestQueueSubscriptionCount - 1; j++)
            {
                requestQueueSubscriptions[j] = requestQueueSubscriptions[j + 1];
            }
            requestQueueSubscriptionCount--;
            ArrayResize(requestQueueSubscriptions, requestQueueSubscriptionCount);
        }
    }
}

//+------------------------------------------------------------------+
//|                                            MT5Ext.mqh            |
//+------------------------------------------------------------------+
#property copyright "QuantsPub"
#property version "0.1"

#include <MT5Ext\socket-library-mt4-mt5.mqh>
#include <MT5Ext\helpers.mqh>
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
        restServer = NULL;
    }

    if (streamingServer != NULL)
    {
        delete streamingServer;
        streamingServer = NULL;
    }

    for (int i = 0; i < ArraySize(streamingClients); i++)
    {
        if (streamingClients[i] != NULL)
        {
            delete streamingClients[i];
            streamingClients[i] = NULL;
        }
    }
}

void AcceptClients(bool onlyStream)
{
    if (restServer != NULL)
    {
        ClientSocket *client = restServer.Accept();
        if (client != NULL && client.IsSocketConnected())
        {
            Print("New REST client connected: ", client);
            Print("Processing client request...");
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
    uchar buffer[4098];
    int received = client.Receive(buffer);

    if (received > 0)
    {
        Print("Received ", received, " bytes from client: ", &client);
        // Print("Received data: ");
        // ArrayPrint(buffer);
        string request = CharArrayToString(buffer, 0, received);
        Print("Received request: " + request);

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
        if (streamingClients[i] != NULL && streamingClients[i].IsSocketConnected())
        {
            streamingClients[i].Send(data);
        }
    }
}

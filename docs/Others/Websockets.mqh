//+------------------------------------------------------------------+
//|                                      Websockets.mqh             |
//+------------------------------------------------------------------+
#property copyright "metatrader5ext"
#property version "0.1"
#property strict

// -------------------------------------------------------------
// Winsock constants and structures
// -------------------------------------------------------------

#define SOCKET_HANDLE32 uint
#define SOCKET_HANDLE64 ulong
#define AF_INET 2
#define SOCK_STREAM 1
#define IPPROTO_TCP 6
#define INVALID_SOCKET32 0xFFFFFFFF
#define INVALID_SOCKET64 0xFFFFFFFFFFFFFFFF
#define SOCKET_ERROR -1
#define INADDR_NONE 0xFFFFFFFF
#define FIONBIO 0x8004667E
#define WSAWOULDBLOCK 10035

// -------------------------------------------------------------
// DLL imports
// -------------------------------------------------------------

#import "websocket-sharp.dll"
int Connect(const uchar &url[], int port, int command_wait_timeout, const uchar &path[], const uchar &url[]);
int GetCommand(uchar &data[]);
int SetCallback(const uchar &url[], const uchar &format[]);
int SetCommandResponse(const uchar &command[], const uchar &response[]);
int RaiseEvent(const uchar &data[]);
int SetAuthToken(const uchar &token[]);
void Deinit();
#import


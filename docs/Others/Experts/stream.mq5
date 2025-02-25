//+------------------------------------------------------------------+
//|                                      Collector(live)_v4.1.mq5 |
//+------------------------------------------------------------------+
#property copyright     "Ramin Rostami"
#property version       "0.1"
#define DEBUG_PRINT     true

#include <Arrays\ArrayString.mqh>
#include <Arrays\List.mqh>
#define MSVCRT_DLL

#include <socket-library-mt4-mt5.mqh>

//+------------------------------------------------------------------+
input string InpSymbolsList="";//List of tools
input uint   InpUpdateMSec=250;//Update period, ms
//---
input string socket_options="=== TCP Socket ===";
input bool   InpSocketUse=true;       //Write to Socket
input string   Hostname = "127.0.0.1";    // Server hostname or IP address

input ushort   LIVE_PORT = 15557;
input ushort   STREAM_PORT = 15558;        // Server port
//+------------------------------------------------------------------+
// Server socket
ServerSocket * glbServerSocket = NULL;

// Array of current clients
ClientSocket * glbClients[];

// Watch for need to create timer;
bool glbCreatedTimer = false;


// --------------------------------------------------------------------
// Global variables and constants
// --------------------------------------------------------------------

ClientSocket * StreamSocket = NULL;
ClientSocket * LiveSocket = NULL;
// --------------------------------------------------------------------
//--- class for working with the tool
class CMyData : public CObject
  {
public:
   string            symbol;
   int               digits;
   double            close;


   //+------------------------------------------------------------------+

   //+------------------------------------------------------------------+

  };
//---
CList list;
datetime wm_time_current=0;
int wm_symbols_total=0;
int csv_handle=INVALID_HANDLE;
int line_index=0;

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
string str_login=(string)AccountInfoInteger(ACCOUNT_LOGIN);
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int OnInit()
  {


   CArrayString symbols;

   if(_UninitReason==REASON_PROGRAM ||    //start of the program
      _UninitReason==REASON_PARAMETERS)   //change parameters
     {

      if(InpSymbolsList=="")
        {
         //--- all instruments from Market Watch
         int total=SymbolsTotal(true);
         for(int i=0; i<total; i++)
           {
            string _symbol=SymbolName(i,true);
            if(!SymbolInfoInteger(_symbol,SYMBOL_CUSTOM) && symbols.SearchLinear(_symbol)==-1)
               symbols.Add(_symbol);
           }

         if(symbols.Total()==0)
            Print("The list of tools is empty.");

        }
      else
        {
         //--- tool string parsing

         string symb_list=InpSymbolsList;
         StringReplace(symb_list,";"," ");
         StringReplace(symb_list,","," ");
         while(StringReplace(symb_list,"  "," ")>0);
         //---
         string result[];
         int total=StringSplit(symb_list,' ',result);
         for(int i=0; i<total; i++)
           {
            //--- checking for empty string
            if(StringLen(result[i])==0)
               continue;
            //---
            if(SymbolSelect(result[i],true))
              {
               if(symbols.SearchLinear(result[i])==-1)
                  symbols.Add(result[i]);
              }
            else
              {
               Print("Tool '",result[i],"' not found.");
              }
           }
         //---
         if(symbols.Total()==0)
            Print("The tool list is empty.");
        }
     }

//--- adding tools
   int total=symbols.Total();
   for(int i=0; i<total; i++)
     {
      string _symbol=symbols.At(i);
      //---checking if the tool is in the list

      bool found=false;
      int _total= list.Total();
      for(int k=0; k<_total; k++)
        {
         CMyData *item=list.GetNodeAtIndex(k);
         if(item.symbol==_symbol)
           {
            found=true;
            break;
           }
        }

      //--- add if not in the list
      if(!found)
        {
         if(DEBUG_PRINT)
            Print("Adding ",_symbol," to the list of tools.");
         //---
         list.Add(new CMyData);
         CMyData *item=list.GetCurrentNode();
         item.symbol=_symbol;
         item.digits=(int)SymbolInfoInteger(_symbol,SYMBOL_DIGITS);


        }
     }

//--- removing unnecessary tools (left over from previous launches/settings)
   total=list.Total();
   for(int i=total-1; i>=0; i--)
     {
      CMyData *item=list.GetNodeAtIndex(i);
      if(symbols.SearchLinear(item.symbol)==-1)
        {
         //--- remove from market review
         SymbolSelect(item.symbol,false);
         if(DEBUG_PRINT)
            Print("Removing ",item.symbol," from the list of tools.");
         list.Delete(i);
        }
     }

//---
   EventSetMillisecondTimer(InpUpdateMSec);

//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {

//--- removing indicator handles
   int total=list.Total();
   for(int i=total-1; i>=0; i--)

     {
      CMyData *item=list.GetNodeAtIndex(i);
     }
//---
// Sockets Clean
   if(StreamSocket)
     {
      delete StreamSocket;
      StreamSocket = NULL;
     }
//---
   list.Clear();

   if(csv_handle!=INVALID_HANDLE)
      FileClose(csv_handle);

   EventKillTimer();
  }
//+------------------------------------------------------------------+
void OnTimer()
  {
   if(!TerminalInfoInteger(TERMINAL_CONNECTED))
      return;

//--- updating tools in the market overview
//--- necessary for indicators to work
   if(wm_time_current!=TimeCurrent() && wm_symbols_total!=SymbolsTotal(true))
     {
      wm_time_current=TimeCurrent();
      wm_symbols_total=SymbolsTotal(true);
      //---
      int total=list.Total();
      for(int i=0; i<total; i++)
        {
         CMyData *item=list.GetNodeAtIndex(i);
         SymbolSelect(item.symbol,true);
        }
     }

   MqlDateTime mdt;
   TimeToStruct(TimeCurrent(),mdt);

//--- write data to the database in one request
   int index=0;
   int _total=list.Total();
   for(int k=0; k<_total; k++)
     {
      CMyData *item=list.GetNodeAtIndex(k);

      double bid=SymbolInfoDouble(item.symbol,SYMBOL_BID);

      if(fabs(bid-item.close)<_Point)
         continue;
      //Print(item.symbol," ",DoubleToString(item.close,item.digits)," -> ",DoubleToString(bid,item.digits));
      item.close=bid;

      //---
      MqlRates rates[];
      ArraySetAsSeries(rates,true);




      //string json = "{'Open':" + DoubleToString(rates[0].open, item.digits) +
      //              ",'High':" + DoubleToString(rates[0].high, item.digits) +
      //              ",'Low':" + DoubleToString(rates[0].low, item.digits) +
      //              ",'Close':" + DoubleToString(rates[0].close, item.digits) +
      //              ",'Tick_Volume':" + (string)rates[0].tick_volume +
      //              ",'Spread':" + (string)SymbolInfoInteger(item.symbol, SYMBOL_SPREAD) +
      //              ",'TimeCurrent':'" + TimeCurrent() + "'" +
      //              ",'TimeLocal':'" + TimeLocal() + "'" +
      //              ",'TimeLocal_Unix':" + DoubleToString(TimeLocal(), 0) +
      //              ",'Symbol':'" + (string)item.symbol + "'" + // Add the symbol name here
      //              "}";


      string json = "{'Symbol':'" + (string)item.symbol + "'}";



      // Socket Stream
      if(InpSocketUse)
        {
         if(!StreamSocket)
           {
            StreamSocket = new ClientSocket(Hostname, STREAM_PORT);
            if(StreamSocket.IsSocketConnected())
              {
               Print("Start Send Data");
               StreamSocket.Send(json);
              }
            else
              {
               Print("Client connection failed");
              }
           }

         if(StreamSocket)
           {
            delete StreamSocket;
            StreamSocket = NULL;
           }
        }

      // Socket Stream
      if(InpSocketUse)
        {
         if(!LiveSocket)
           {
            LiveSocket = new ClientSocket(Hostname, STREAM_PORT);
            if(LiveSocket.IsSocketConnected())
              {
               Print("Start Send Data");
               LiveSocket.Send(json);
              }
            else
              {
               Print("Client connection failed");
              }
           }

         if(LiveSocket)
           {
            delete LiveSocket;
            LiveSocket = NULL;
           }
        }




     }

  }
//+------------------------------------------------------------------+

//+------------------------------------------------------------------+

#include "MQL5Socket/SocketLib.mqh"
#include "Parse.mqh"

input string Host="127.0.0.1";
input ushort Port=1235;
input ushort StreamPort=1236;

SOCKET64 server = INVALID_SOCKET64;

int OnInit(){
   EventSetMillisecondTimer(1);
   return 0;
}

void OnDeinit(const int reason){
   EventKillTimer();
   delete trade;
   CloseClean();   
}

void OnTimer(){
   if(server != INVALID_SOCKET64){
      char buf[1024]={0};
      ref_sockaddr ref={{0}}; 
      int len=ArraySize(ref.ref);
      int res=recvfrom(server,buf,1024,0,ref.ref,len);
      if (res>=0){ 
         string receive = CharArrayToString(buf);
         Print("receive: ", receive);
         string respSend = Parse(receive);
         uchar data[]; StringToCharArray(respSend, data);
         if(sendto(server,data,ArraySize(data),0,ref.ref,ArraySize(ref.ref))==SOCKET_ERROR){
            int err=WSAGetLastError();
            if(err!=WSAEWOULDBLOCK) { Print("-Send failed error: "+WSAErrorDescript(err)); CloseClean(); }
         }
         else
            Print("Send: ", respSend);
      }
      else{
         int err=WSAGetLastError();
         if(err!=WSAEWOULDBLOCK) { Print("-receive failed error: "+WSAErrorDescript(err)+". Cleanup socket"); CloseClean(); return; }
      }

   }
   else{
      
      char wsaData[]; ArrayResize(wsaData,sizeof(WSAData));
      int res=WSAStartup(MAKEWORD(2,2), wsaData);
      if(res!=0) { Print("-WSAStartup failed error: "+string(res)); return; }

      // create a socket
      server=socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP);
      if(server==INVALID_SOCKET64) { Print("-Create failed error: "+WSAErrorDescript(WSAGetLastError())); CloseClean(); return; }

      // bind to address and port
      Print("try bind..."+Host+":"+string(Port));

      char ch[]; StringToCharArray(Host,ch);
      sockaddr_in addrin;
      addrin.sin_family=AF_INET;
      addrin.sin_addr.u.S_addr=inet_addr(ch);
      addrin.sin_port=htons(Port);
      ref_sockaddr ref; ref.in=addrin;
      if(bind(server,ref.ref,sizeof(addrin))==SOCKET_ERROR){
         int err=WSAGetLastError();
         if(err!=WSAEISCONN) { Print("-Connect failed error: "+WSAErrorDescript(err)+". Cleanup socket"); CloseClean(); return; }
      }

      // set to nonblocking mode
      int non_block=1;
      res=ioctlsocket(server,(int)FIONBIO,non_block);
      if(res!=NO_ERROR) { Print("ioctlsocket failed error: "+string(res)); CloseClean(); return; }

      Print("start server ok");
     }
  }

void CloseClean(){
   printf("Shutdown server");
   if(server!=INVALID_SOCKET64) { closesocket(server); server=INVALID_SOCKET64; } // close the server
   WSACleanup();
}
//+------------------------------------------------------------------+
//|                                        Spy Control panel MCM.mq5 |
//|                                            Copyright 2010, Lizar |
//|                            https://www.mql5.com/en/users/Lizar |
//+------------------------------------------------------------------+
#define VERSION       "1.00 Build 3 (26 Dec 2010)"

#property copyright   "Copyright 2010, Lizar"
#property link        "https://www.mql5.com/en/users/Lizar"
#property version     VERSION
#property description "This is the MCM Control Panel agent-indicator."
#property description "Is launched on the required symbol on any time-frame"
#property description "and generates the custom NewBar event and/or NewTick"
#property description "for the chart which receives the event"

#property indicator_chart_window
  
input long                    chart_id;                 // identifier of the chart which receives the event
input ushort                  custom_event_id;          // event identifier  
input ENUM_CHART_EVENT_SYMBOL flag_event=CHARTEVENT_NO;// indicator, which determines the event type.

MqlDateTime time, prev_time;

//+------------------------------------------------------------------+
//| Custom indicator iteration function                              |
//+------------------------------------------------------------------+
int OnCalculate (const int rates_total,       // size of the price[] array
                 const int prev_calculated, // bars processed at the previous call
                 const int begin,           // where the data begins
                 const double& price[]      // calculations array
   )
  {  
   double price_current=price[rates_total-1];

   TimeCurrent(time);
   
   if(prev_calculated==0)
     {
      EventCustom(CHARTEVENT_INIT,price_current);
      prev_time=time; 
      return(rates_total);
     }
   
//--- new tick
   if((flag_event & CHARTEVENT_TICK)!=0) EventCustom(CHARTEVENT_TICK,price_current);       

//--- check change time
   if(time.min==prev_time.min && 
      time.hour==prev_time.hour && 
      time.day==prev_time.day &&
      time.mon==prev_time.mon) return(rates_total);

//--- new minute
   if((flag_event & CHARTEVENT_NEWBAR_M1)!=0) EventCustom(CHARTEVENT_NEWBAR_M1,price_current);     
   if(time.min%2 ==0 && (flag_event & CHARTEVENT_NEWBAR_M2)!=0)  EventCustom(CHARTEVENT_NEWBAR_M2,price_current);
   if(time.min%3 ==0 && (flag_event & CHARTEVENT_NEWBAR_M3)!=0)  EventCustom(CHARTEVENT_NEWBAR_M3,price_current); 
   if(time.min%4 ==0 && (flag_event & CHARTEVENT_NEWBAR_M4)!=0)  EventCustom(CHARTEVENT_NEWBAR_M4,price_current);      
   if(time.min%5 ==0 && (flag_event & CHARTEVENT_NEWBAR_M5)!=0)  EventCustom(CHARTEVENT_NEWBAR_M5,price_current);     
   if(time.min%6 ==0 && (flag_event & CHARTEVENT_NEWBAR_M6)!=0)  EventCustom(CHARTEVENT_NEWBAR_M6,price_current);     
   if(time.min%10==0 && (flag_event & CHARTEVENT_NEWBAR_M10)!=0) EventCustom(CHARTEVENT_NEWBAR_M10,price_current);      
   if(time.min%12==0 && (flag_event & CHARTEVENT_NEWBAR_M12)!=0) EventCustom(CHARTEVENT_NEWBAR_M12,price_current);      
   if(time.min%15==0 && (flag_event & CHARTEVENT_NEWBAR_M15)!=0) EventCustom(CHARTEVENT_NEWBAR_M15,price_current);      
   if(time.min%20==0 && (flag_event & CHARTEVENT_NEWBAR_M20)!=0) EventCustom(CHARTEVENT_NEWBAR_M20,price_current);      
   if(time.min%30==0 && (flag_event & CHARTEVENT_NEWBAR_M30)!=0) EventCustom(CHARTEVENT_NEWBAR_M30,price_current);      
   if(time.min!=0) {prev_time=time; return(rates_total);}
//--- new hour
   if((flag_event & CHARTEVENT_NEWBAR_H1)!=0) EventCustom(CHARTEVENT_NEWBAR_H1,price_current);
   if(time.hour%2 ==0 && (flag_event & CHARTEVENT_NEWBAR_H2)!=0)  EventCustom(CHARTEVENT_NEWBAR_H2,price_current);
   if(time.hour%3 ==0 && (flag_event & CHARTEVENT_NEWBAR_H3)!=0)  EventCustom(CHARTEVENT_NEWBAR_H3,price_current);      
   if(time.hour%4 ==0 && (flag_event & CHARTEVENT_NEWBAR_H4)!=0)  EventCustom(CHARTEVENT_NEWBAR_H4,price_current);      
   if(time.hour%6 ==0 && (flag_event & CHARTEVENT_NEWBAR_H6)!=0)  EventCustom(CHARTEVENT_NEWBAR_H6,price_current);      
   if(time.hour%8 ==0 && (flag_event & CHARTEVENT_NEWBAR_H8)!=0)  EventCustom(CHARTEVENT_NEWBAR_H8,price_current);      
   if(time.hour%12==0 && (flag_event & CHARTEVENT_NEWBAR_H12)!=0) EventCustom(CHARTEVENT_NEWBAR_H12,price_current);      
   if(time.hour!=0) {prev_time=time; return(rates_total);}
//--- new day
   if((flag_event & CHARTEVENT_NEWBAR_D1)!=0) EventCustom(CHARTEVENT_NEWBAR_D1,price_current);      
//--- new week
   if(time.day_of_week==1 && (flag_event & CHARTEVENT_NEWBAR_W1)!=0) EventCustom(CHARTEVENT_NEWBAR_W1,price_current);      
//--- new month
   if(time.day==1 && (flag_event & CHARTEVENT_NEWBAR_MN1)!=0) EventCustom(CHARTEVENT_NEWBAR_MN1,price_current);      
   prev_time=time;
//--- return value of prev_calculated for next call
   return(rates_total);
  }
//+------------------------------------------------------------------+

void EventCustom(ENUM_CHART_EVENT_SYMBOL event,double price)
  {
   EventChartCustom(chart_id,custom_event_id,(long)event,price,_Symbol);
   return;
  } 


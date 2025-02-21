///////////////////////////////////////////////////////////////////////////////////
//    Common
///////////////////////////////////////////////////////////////////////////////////

#include <Trade\Trade.mqh>

ENUM_TIMEFRAMES StringToTimeFrame(string tf)
{
    // Standard timeframes
    if (tf == "M1")
        return PERIOD_M1;
    if (tf == "M2")
        return PERIOD_M2;
    if (tf == "M3")
        return PERIOD_M3;
    if (tf == "M4")
        return PERIOD_M4;
    if (tf == "M5")
        return PERIOD_M5;
    if (tf == "M6")
        return PERIOD_M6;
    if (tf == "M10")
        return PERIOD_M10;
    if (tf == "M12")
        return PERIOD_M12;
    if (tf == "M15")
        return PERIOD_M15;
    if (tf == "M20")
        return PERIOD_M20;
    if (tf == "M30")
        return PERIOD_M30;
    if (tf == "H1")
        return PERIOD_H1;
    if (tf == "H2")
        return PERIOD_H2;
    if (tf == "H3")
        return PERIOD_H3;
    if (tf == "H4")
        return PERIOD_H4;
    if (tf == "H6")
        return PERIOD_H6;
    if (tf == "H8")
        return PERIOD_H8;
    if (tf == "H12")
        return PERIOD_H12;
    if (tf == "D1")
        return PERIOD_D1;
    if (tf == "W1")
        return PERIOD_W1;
    if (tf == "MN1")
        return PERIOD_MN1;
    return -1;
}

string TimeFrameToString(ENUM_TIMEFRAMES tf)
{
    // Standard timeframes
    switch (tf)
    {
    case PERIOD_M1:
        return "M1";
    case PERIOD_M2:
        return "M2";
    case PERIOD_M3:
        return "M3";
    case PERIOD_M4:
        return "M4";
    case PERIOD_M5:
        return "M5";
    case PERIOD_M6:
        return "M6";
    case PERIOD_M10:
        return "M10";
    case PERIOD_M12:
        return "M12";
    case PERIOD_M15:
        return "M15";
    case PERIOD_M20:
        return "M20";
    case PERIOD_M30:
        return "M30";
    case PERIOD_H1:
        return "H1";
    case PERIOD_H2:
        return "H2";
    case PERIOD_H3:
        return "H3";
    case PERIOD_H4:
        return "H4";
    case PERIOD_H6:
        return "H6";
    case PERIOD_H8:
        return "H8";
    case PERIOD_H12:
        return "H12";
    case PERIOD_D1:
        return "D1";
    case PERIOD_W1:
        return "W1";
    case PERIOD_MN1:
        return "MN1";
    default:
        return "UNKNOWN";
    }
}

// use string so that we can have the same in MT5.
string OrderTypeToString(int orderType)
{
    if (orderType == POSITION_TYPE_BUY)
        return "POSITION_TYPE_BUY";
    if (orderType == POSITION_TYPE_SELL)
        return "POSITION_TYPE_SELL";
    if (orderType == ORDER_TYPE_BUY_LIMIT)
        return "ORDER_TYPE_BUY_LIMIT";
    if (orderType == ORDER_TYPE_SELL_LIMIT)
        return "ORDER_TYPE_SELL_LIMIT";
    if (orderType == ORDER_TYPE_BUY_STOP)
        return "ORDER_TYPE_BUY_STOP";
    if (orderType == ORDER_TYPE_SELL_STOP)
        return "ORDER_TYPE_SELL_STOP";
    return "UNKNOWN";
}

int StringToOrderType(string orderTypeStr)
{
    if (orderTypeStr == "POSITION_TYPE_BUY")
        return POSITION_TYPE_BUY;
    if (orderTypeStr == "POSITION_TYPE_SELL")
        return POSITION_TYPE_SELL;
    if (orderTypeStr == "ORDER_TYPE_BUY_LIMIT")
        return ORDER_TYPE_BUY_LIMIT;
    if (orderTypeStr == "ORDER_TYPE_SELL_LIMIT")
        return ORDER_TYPE_SELL_LIMIT;
    if (orderTypeStr == "ORDER_TYPE_BUY_STOP")
        return ORDER_TYPE_BUY_STOP;
    if (orderTypeStr == "ORDER_TYPE_SELL_STOP")
        return ORDER_TYPE_SELL_STOP;
    if (orderTypeStr == "ORDER_TYPE_BUY_STOP_LIMIT")
        return ORDER_TYPE_BUY_STOP_LIMIT;
    if (orderTypeStr == "ORDER_TYPE_SELL_STOP_LIMIT")
        return ORDER_TYPE_SELL_STOP_LIMIT;
    return -1;
}

string HistoryDealTypeToString(int dealType)
{
    if (dealType == DEAL_TYPE_BUY)
        return "DEAL_TYPE_BUY";
    if (dealType == DEAL_TYPE_SELL)
        return "DEAL_TYPE_SELL";
    if (dealType == DEAL_TYPE_BUY_CANCELED)
        return "DEAL_TYPE_BUY_CANCELED";
    if (dealType == DEAL_TYPE_SELL_CANCELED)
        return "DEAL_TYPE_SELL_CANCELED";
    if (dealType == DEAL_TYPE_BALANCE)
        return "DEAL_TYPE_BALANCE";
    if (dealType == DEAL_TYPE_COMMISSION)
        return "DEAL_TYPE_COMMISSION";
    if (dealType == DEAL_TYPE_BONUS)
        return "DEAL_TYPE_BONUS";
    if (dealType == DEAL_TYPE_CHARGE)
        return "DEAL_TYPE_CHARGE";
    if (dealType == DEAL_TYPE_CREDIT)
        return "DEAL_TYPE_CREDIT";
    if (dealType == DEAL_TYPE_CORRECTION)
        return "DEAL_TYPE_CORRECTION";
    if (dealType == DEAL_TYPE_INTEREST)
        return "DEAL_TYPE_INTEREST";
    return "UNKNOWN";
}

string HistoryDealEntryTypeToString(int entryType)
{
    if (entryType == DEAL_ENTRY_IN)
        return "DEAL_ENTRY_IN";
    if (entryType == DEAL_ENTRY_OUT)
        return "DEAL_ENTRY_OUT";
    if (entryType == DEAL_ENTRY_OUT_BY)
        return "DEAL_ENTRY_OUT_BY";
    if (entryType == DEAL_ENTRY_INOUT)
        return "DEAL_ENTRY_INOUT";
    if (entryType == DEAL_ENTRY_STATE)
        return "DEAL_ENTRY_STATE";
    return "UNKNOWN";
}
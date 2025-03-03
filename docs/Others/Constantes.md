### Trading Constants


####  [PositionsTotal](https://www.mql5.com/pt/docs/trading/positionstotal)

------------
**Returns the number of open positions.**

PositionsTotal()

Example:
```python
mql5.PositionsTotal()
```


####  [PositionAll](https://www.mql5.com/pt/docs/constants/tradingconstants/positionproperties)

------------
**Returns an array of [type PropertiesPosition](#PropertiesPosition "PropertiesPosition") with all open positions**

PositionAll()

Example:
```python
mql5.PositionAll()
```

####  [OrdersTotal](https://www.mql5.com/pt/docs/trading/orderstotal)

------------
**Returns the number of pending orders.**

*Value of type **Double**.*

OrdersTotal()
 

Example:
```python
mql5.OrdersTotal()
```

#### [OrderAll](https://www.mql5.com/pt/docs/constants/tradingconstants/orderproperties)

------------
**Returns an array of type [type PropertiesOrder](#PropertiesOrder "PropertiesOrder") with all pending orders**


OrderAll()
 

Example:
```python
mql5.OrderAll()
```

####  [HistoryDealTotalDay](https://www.mql5.com/pt/docs/trading/historydealstotal)

------------
**Returns the number of orders and trades in the day's history.**


HistoryDealTotalDay()
 

Example:
```python
mql5.HistoryDealTotalDay()
```

####  [HistoryDealTotal](https://www.mql5.com/pt/docs/trading/historydealstotal)

------------
**Returns the number of orders and trades in history for a specified time period.**


HistoryDealTotal(Start_Time, Stop_Time)
 

Example:
```python
mql5.HistoryDealTotal("2019.07.16 10:25:10", "2019.07.18 12:00:00")
```

####  [HistoryDealAllDay](https://www.mql5.com/pt/docs/constants/tradingconstants/dealproperties)

------------
**Returns an array of [PropertiesDeal type](#PropertiesDeal "PropertiesDeal") with all orders and trades in the day's history**


HistoryDealAllDay()
 

Example:
```python
mql5.HistoryDealAllDay()
```

####  [HistoryDealAll](https://www.mql5.com/pt/docs/constants/tradingconstants/dealproperties)

------------
**Returns an array of [type PropertiesDeal](#PropertiesDeal "PropertiesDeal") with all orders and deals in history for a specified time period.**


HistoryDealAll(Start_Time, Stop_Time)
 

Example:
```python
mql5.HistoryDealAll("2019.07.16 10:25:10", "2019.07.18 12:00:00")
```

####  [PropertiesPosition](https://www.mql5.com/pt/docs/constants/tradingconstants/positionproperties)
------------
*The PropertiesPosition Type is a dictionary that has the following model (Properties of a Position):*
```python
{ 
	'TICKET': int, # Position ticket. A unique number assigned to each position.
	'TIME': date, # Time a position was opened
	'TIME_MSC': int, # Opening time position in milliseconds since 01.01.1970
	'TIME_UPDATE': int, # Change time position in seconds since 01.01.1970
	'TIME_UPDATE_MSC': int, # Change time position in milliseconds since 01.01.1970
	'TYPE': ENUM_POSITION_TYPE, # Position type
	'MAGIC': int, # Magic number of a position
	'IDENTIFIER': int, # Position identifier is a unique number that is assigned to every new position opened and does not change
	'REASON': ENUM_POSITION_REASON, # Reason for opening the position
	'VOLUME': float, # Volume of a position
	'PRICE_OPEN': float, # Opening price of a position
	'SL': float, # Stop Loss level of an open position
	'TP': float, # Take Profit level of an open position
	'PRICE_CURRENT': float, # Current asset price of a position
	'PROFIT': float, # Current profit
	'SYMBOL': String, # Active (symbol) position
	'COMMENT': String, # Comment of a position
	'EXTERNAL_ID': String # Position ID in external trading system (on stock exchange)
}
```
[ENUM_POSITION_TYPE](https://www.mql5.com/pt/docs/constants/tradingconstants/positionproperties#enum_position_type "ENUM_POSITION_TYPE")
[ENUM_POSITION_REASON](https://www.mql5.com/pt/docs/constants/tradingconstants/positionproperties#enum_position_reason "ENUM_POSITION_REASON")

#### [PropertiesOrder](https://www.mql5.com/pt/docs/constants/tradingconstants/orderproperties)
------------
*The PropertiesOrder Type is a dictionary that has the following model (Properties of an Order):*
```python
{
	'TICKET': int, # Order ticket. A unique number assigned to each order
	'TIME_SETUP': date, # Time an order was set up
	'TYPE': ENUM_ORDER_TYPE, # Order type
	'STATE': ENUM_ORDER_STATE, # State of an order
	'TIME_EXPIRATION': date, # Expiration time of an order
	'TIME_DONE': date, # Time an order was executed or cancelled
	'TIME_SETUP_MSC': int, # The time to place an order for execution in milliseconds since 01.01.1970
	'TIME_DONE_MSC': int, # Order execution and cancellation time in milliseconds since 01.01.1970
	'TYPE_FILLING': ENUM_ORDER_TYPE_FILLING, # Type of filling of an order
	'TYPE_TIME': ENUM_ORDER_TYPE_TIME, # duration time of an order
	'MAGIC': int, # ID of an Expert Advisor that placed the order
	'POSITION_ID': int, # Position identifier that is set to an order as soon as it is executed.
	'POSITION_BY_ID': int, # Identifier of the opposite position for orders of type
	'VOLUME_INITIAL': float, # Initial volume of an order
	'VOLUME_CURRENT': float, # Current volume of an order
	'PRICE_OPEN': float, # Price specified in the order
	'SL': float, # Valor de Stop Loss
	'TP': float, # Valor de Take Profit
	'PRICE_CURRENT': float, # The current price of an order's asset
	'PRICE_STOPLIMIT': float, # The Limit order price for a StopLimit order
	'SYMBOL': String, # Asset (symbol) of an order
	'COMMENT': String # Comment on order
}
```
[ENUM_ORDER_TYPE](https://www.mql5.com/pt/docs/constants/tradingconstants/orderproperties#enum_order_type"ENUM_ORDER_TYPE")
[ENUM_ORDER_STATE](https://www.mql5.com/pt/docs/constants/tradingconstants/orderproperties#enum_order_state"ENUM_ORDER_STATE")
[ENUM_ORDER_TYPE_FILLING](https://www.mql5.com/pt/docs/constants/tradingconstants/orderproperties#enum_order_type_filling"ENUM_ORDER_TYPE_FILLING")
[ENUM_ORDER_TYPE_TIME](https://www.mql5.com/pt/docs/constants/tradingconstants/orderproperties#enum_order_type_time"ENUM_ORDER_TYPE_TIME")

####  [PropertiesDeal](https://www.mql5.com/pt/docs/constants/tradingconstants/positionproperties)
------------
*The PropertiesDeal Type is a dictionary that has the following model (Transaction Properties):*
```python
{
 	'TICKET': int,# Transaction ticket. A unique number assigned to each transaction.
	'ORDER': int, # Transaction order number.
	'TIME': date, # Transaction Properties
	'TIME_MSC': int, # The trade execution time in milliseconds since 01.01.1970
	'TYPE': ENUM_DEAL_TYPE, # Transaction type
	'ENTRY': ENUM_DEAL_ENTRY, # Entry of a transaction - entry, exit, rollback
	'MAGIC': int, # Magic number for a transaction
    'REASON': ENUM_DEAL_REASON, # Reason or origin for performing the transaction
    'POSITION_ID': int, # Identifier of a position, in the opening, modification or closing of which this transaction took part
    'VOLUME': float, # Transaction volume
    'PRICE': float, # Transaction price
    'COMMISSION': float, # Transaction price
    'SWAP': float, # Cumulative swap at close
    'PROFIT': float, # Profit from the transaction
    'SYMBOL': String, # Asset (symbol) of the transaction
    'COMMENT': String # Transaction comment
}
```
[ENUM_DEAL_TYPE](https://www.mql5.com/pt/docs/constants/tradingconstants/dealproperties#enum_deal_type "ENUM_DEAL_TYPE")
[ENUM_DEAL_ENTRY](https://www.mql5.com/pt/docs/constants/tradingconstants/dealproperties#enum_deal_entry "ENUM_DEAL_ENTRY")
[ENUM_DEAL_REASON](https://www.mql5.com/pt/docs/constants/tradingconstants/dealproperties#enum_deal_reason "ENUM_DEAL_REASON")

### Trade


####  [Buy](https://www.mql5.com/pt/docs/standardlibrary/tradeclasses/ctrade/ctradebuy)

------------
**Opens a long position with the specified parameters.**

*Returns -1 if any parameter error occurs, otherwise returns the ticket number (order number)*

Buy(Symbol, Volume, Price, SL, TP, Comment)
 

Example:
```python
mql5.Buy("BTCUSD",  100, 27.50, 27.01, 27.98, "Qualquer comentario")
```

####  [Sell](https://www.mql5.com/pt/docs/standardlibrary/tradeclasses/ctrade/ctradesell)

------------
**Opens a short position with the given parameters.**

*Returns -1 if any parameter error occurs, otherwise returns the ticket number (order number)*

Sell(Symbol, Volume, Price, SL, TP, Comment)
 

Example:
```python
mql5.Sell("BTCUSD",  100, 27.50, 27.98, 27.01 , "Qualquer comentario")
```

####  [BuyLimit](https://www.mql5.com/pt/docs/standardlibrary/tradeclasses/ctrade/ctradebuylimit)

------------
**Places a pending order of the Buy Limit type (buy at a price lower than the current market price) with specified parameters.**

*Returns -1 if any parameter error occurs, otherwise returns the ticket number (order number)*

BuyLimit(Symbol, Volume, Price, SL, TP, Comment)
 

Example:
```python
mql5.BuyLimit("BTCUSD",  100, 27.50, 27.01, 27.98, "Qualquer comentario")
```

####  [SellLimit](https://www.mql5.com/pt/docs/standardlibrary/tradeclasses/ctrade/ctradeselllimit)

------------
**Places a pending order of the Sell Limit type (sell at a price higher than the current market price) with specified parameters.**

*Returns -1 if any parameter error occurs, otherwise returns the ticket number (order number)*

SellLimit(Symbol, Volume, Price, SL, TP, Comment)

Example:
```python
mql5.SellLimit("BTCUSD", 100, 27.50, 27.98, 27.01, "Any comment")
```

####  [BuyStop](https://www.mql5.com/pt/docs/standardlibrary/tradeclasses/ctrade/ctradebuystop)

------------
**Places a pending Buy Stop order (buy at a price higher than the current market price) with specified parameters.**

*Returns -1 if any parameter error occurs, otherwise returns the ticket number (order number)*

BuyStop(Symbol, Volume, Price, SL, TP, Comment)
 

Example:
```python
mql5.BuyStop("BTCUSD", 100, 27.50, 27.01, 27.98, "Any comments")
```

####  [SellStop](https://www.mql5.com/pt/docs/standardlibrary/tradeclasses/ctrade/ctradesellstop)

------------
**Places a pending order of the Sell Stop type (sell at a price lower than the current market price) with specified parameters.**

*Returns -1 if any parameter error occurs, otherwise returns the ticket number (order number)*

SellStop(Symbol, Volume, Price, SL, TP, Comment)
 

Example:
```python
mql5.SellStop("BTCUSD", 100, 27.50, 27.98, 27.01, "Any comments")
```

####  [OrderDelete](https://www.mql5.com/pt/docs/standardlibrary/tradeclasses/ctrade/ctradeorderdelete)

------------
**Deletes pending order.**

*Returns 1 - in case of successful verification of basic structures, otherwise - 0.*

OrderDelete(Ticket)
 
Example:
```python
mql5.OrderDelete(125663)
```

####  [CancelAllOrder](https://www.mql5.com/pt/docs/standardlibrary/tradeclasses/ctrade/ctradeorderdelete)

------------
**Deletes all pending orders.**

*Returns 1 - in case of successful verification of basic structures, otherwise - 0.*

CancelAllOrder()
 
Example:
```python
mql5.CancelAllOrder()
```

####  [PositionCloseSymbol](https://www.mql5.com/pt/docs/standardlibrary/tradeclasses/ctrade/ctradepositionclose)

------------
**Closes the position by the specified symbol**

*Returns 1 - in case of successful verification of basic structures, otherwise - 0.*

PositionCloseSymbol(Symbol)
 
Example:
```python
mql5.PositionCloseSymbol("BTCUSD")
```

####  [PositionCloseTicket](https://www.mql5.com/pt/docs/standardlibrary/tradeclasses/ctrade/ctradepositionclose)

------------
**Closes the position with the indicated ticket.**

*Returns 1 - in case of successful verification of basic structures, otherwise - 0.*

PositionCloseTicket(Ticket)
 
Example:
```python
mql5.PositionCloseTicket(125663)
```
####  [PositionClosePartial](https://www.mql5.com/pt/docs/standardlibrary/tradeclasses/ctrade/ctradepositionclosepartial)

------------
**Closes part of the position with the indicated ticket, when hedge accounting is active.**

*Returns 1 - in case of successful verification of basic structures, otherwise - 0.*

PositionClosePartial(Ticket, Volume)
 
Example:
```python
mql5.PositionClosePartial(125663, 100)
```

####  [PositionModifySymbol](https://www.mql5.com/pt/docs/standardlibrary/tradeclasses/ctrade/ctradepositionmodify)

------------
**Modifies the position parameters by the given symbol.**

*Returns 1 - in case of successful verification of basic structures, otherwise - 0.*

PositionModifySymbol(Symbol, SL, TP)
 
Example:
```python
mql5.PositionModifySymbol("BTCUSD",  27.40, 27.90)
```

####  [PositionModifyTicket](https://www.mql5.com/pt/docs/standardlibrary/tradeclasses/ctrade/ctradepositionmodify)

------------
**Changes the position parameters according to the indicated ticket.**

*Returns 1 - in case of successful verification of basic structures, otherwise - 0.*

PositionModifyTicket(Ticket, SL, TP)

Example:
```python
mql5.PositionModifyTicket(125663,  27.40, 27.90)
```

####  [CancelAllPositon](https://www.mql5.com/pt/docs/standardlibrary/tradeclasses/ctrade/ctradepositionclose)

------------
**Closes all open positions.**

*Returns 1 - in case of successful verification of basic structures, otherwise - 0.*

CancelAllPositon()

Example:
```python
mql5.CancelAllPositon()
```

####  [SetEAMagicNumber](https://www.mql5.com/pt/docs/standardlibrary/tradeclasses/ctrade/ctradepositionclose)

------------
**Expert Advisor ID. Allows you to organize analytical processing of trading orders. Each Expert Advisor can set its own unique ID (identifier) ​​when sending a trading request.**

*Return 1*

SetEAMagicNumber(Number)

Example:
```python
mql5.SetEAMagicNumber(10000)
```

#### [PositionsTotal](https://www.mql5.com/en/docs/trading/positionstotal)

------------
**Returns the number of open positions.**

*Value of type **int**.*

PositionsTotal()
 

Example:
```python
mql5.PositionsTotal()
```

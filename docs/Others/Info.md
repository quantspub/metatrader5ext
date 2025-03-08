### Information

#### [AccountInfoAll](https://www.mql5.com/pt/docs/constants/environment_state/accountinformation)

------------
**To get information about the current account with a dictionary of [type PropertiesAccount](#PropertiesAccount "type PropertiesAccount") .**

AccountInfoAll()

Example:
```python
mql5.AccountInfoAll()
```

#### [SymbolInfoAll](https://www.mql5.com/pt/docs/constants/environment_state/marketinfoconstants)

------------
**To get current market information with a dictionary of [type PropertiesSymbol](#SymbolInfoAll "type SymbolInfoAll") .**

SymbolInfoAll(Symbol)

Example:
```python
mql5.SymbolInfoAll("BTCUSD")
```

#### [OptionInfo](https://www.mql5.com/pt/docs/constants/environment_state/marketinfoconstants)

------------
**To get the current information about an option with a dictionary of [type PropertiesOptionInfo](#PropertiesOptionInfo "type PropertiesOptionInfo") .**

OptionInfo(Symbol)

Example:
```python
mql5.OptionInfo("PETRH285")
```


#### [PropertiesAccount](https://www.mql5.com/pt/docs/constants/environment_state/accountinformation)
------------
*The PropertiesAccount Type is a dictionary that has the following model (Account Properties):*
```python
{
    'LOGIN': int, # Account number
    'TRADE_MODE' : ENUM_ACCOUNT_TRADE_MODE, # Account trading mode
    'LEVERAGE': , # Account leverage
    'LIMIT_ORDERS': int, # Maximum allowed number of active pending orders
    'MARGIN_SO_MODE': ENUM_ACCOUNT_STOPOUT_MODE, # Mode to set minimum allowed margin
    'TRADE_ALLOWED': int, # Trading allowed for the current account
    'TRADE_EXPERT': int, # Trading allowed for an Expert Advisor
    'MARGIN_MODE': ENUM_ACCOUNT_MARGIN_MODE, # Margin calculation mode
    'CURRENCY_DIGITS': int, # Number of decimal places for the account currency.
    'BALANCE': float, # Account balance in deposit currency
    'CREDIT': float, # Account credit in deposit currency
    'PROFIT': float, # Current profit of an account in the deposit currency
    'EQUITY': float, # Market balance of the account in the deposit currency
    'MARGIN': float, # Account margin used in deposit currency
    'MARGIN_FREE': float, # Free margin of an account in the deposit currency
    'MARGIN_LEVEL': float, # Account margin level in percentage
    'MARGIN_SO_CALL' : float, # Margin call level. Depending on the setting, ACCOUNT_MARGIN_SO_MODE
    'MARGIN_INITIAL': float, # Initial margin. The amount set aside in an account to cover the margin for all pending orders
    'MARGIN_MAINTENANCE': float, # Maintenance margin. The minimum equity set aside in an account to cover the minimum value of all open positions
    'ASSETS': float, # The current assets of an account
    'LIABILITIES': float, # The current liabilities of an account
    'COMMISSION_BLOCKED': float, # The current blocked commission amount on an account
    'NAME': String, # Customer name
    'SERVER': String, # Name of the trading server
    'CURRENCY': String, # Account currency
    'COMPANY': String # Name of a company serving the account
}
```
[ENUM_ACCOUNT_TRADE_MODE](https://www.mql5.com/pt/docs/constants/environment_state/accountinformation#enum_account_trade_mode "ENUM_ACCOUNT_TRADE_MODE")
[ENUM_ACCOUNT_STOPOUT_MODE](https://www.mql5.com/pt/docs/constants/environment_state/accountinformation#enum_account_stopout_mode "ENUM_ACCOUNT_STOPOUT_MODE")
[ENUM_ACCOUNT_MARGIN_MODE](https://www.mql5.com/pt/docs/constants/environment_state/accountinformation#enum_account_margin_mode "ENUM_ACCOUNT_MARGIN_MODE")


#### [PropertiesSymbol](https://www.mql5.com/pt/docs/constants/environment_state/accountinformation)
------------
*The PropertiesSymbol Type is a dictionary that has the following model (Asset Properties):*
```python
{

}
```

#### [PropertiesOptionInfo](https://www.mql5.com/pt/docs/constants/environment_state/accountinformation)
------------
*The PropertiesOptionInfo Type is a dictionary that has the following model (Option Properties):*
```python
{
    'OPTION_MODE': ENUM_SYMBOL_OPTION_MODE,
    'OPTION_RIGHT': ENUM_SYMBOL_OPTION_RIGHT,
    'START_TIME': date,
    'EXPIRATION_TIME': date,
    'OPTION_STRIKE': float,
    'BID': float,
    'ASK': float,
    'LAST': float,
    'VOLUME_REAL': float
}
```
[ENUM_SYMBOL_OPTION_MODE](https://www.mql5.com/pt/docs/constants/environment_state/marketinfoconstants#enum_symbol_option_mode "ENUM_SYMBOL_OPTION_MODE")
[ENUM_SYMBOL_OPTION_RIGHT](https://www.mql5.com/pt/docs/constants/environment_state/marketinfoconstants#enum_symbol_option_right "ENUM_SYMBOL_OPTION_RIGHT")

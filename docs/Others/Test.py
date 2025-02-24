from MTAPI import MTAPI
mql5 = MTAPI()
# test = mql5.iClose("BTCUSD", "M5", 0)
# test = mql5.CopyRates("BTCUSD", "D1", 0, 10)
# test = mql5.Buy(symbol="BTCUSD", volume=0.01,price=99820.0, sl=99700.0, tp=99900.0,comment="Teste")
ss = mql5.AccountInfoAll()
print(ss)

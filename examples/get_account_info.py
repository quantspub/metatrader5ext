from metatrader5ext import MetaTrader5ExtConfig, MetaTrader5Ext

config = MetaTrader5ExtConfig()
client = MetaTrader5Ext(config=config)
client.connect()
print(client.is_connected())

print(client.account_info())

client.disconnect()

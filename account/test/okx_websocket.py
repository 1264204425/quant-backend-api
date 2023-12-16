import time
import ccxt
import websocket
import asyncio
import json
import zlib

OKEX_CONFIG = {
    # 'apiKey': 'cf13d92e-1b38-438a-ba99-c62374f635b7',
    'apiKey': '14ad974e-b21d-4e29-9cd1-3ed5ae40568c',
    # 'secret': '232BF88138ABC5E33CC7311BBC0537F2',
    'secret': '6A967B02CA9767AEFFD587B7CDA2DB58',
    # 'password': 'Jzh2001327.',
    'password': 'Jzhiauhs2001.',
    'proxies': {
        'http': 'http://localhost:55169',
        'https': 'http://localhost:55169',
    },
}

okx = ccxt.okex5(OKEX_CONFIG)
# account = okx.fetch_balance()
# print(account)
# funding = okx.ccurencies(['BTC']['fee'])
params = {
    'instld': 'BTC-USD-SWAP'
}
# params = {
#     'instType': 'SPOT'
# }
# a = okx.publicGetPublicInstruments(params=params)
funding = okx.fetch_funding_history(symbol='BTC-USDT-SWAP')
# funding = okx.publicGetPublicFundingRateHistory(params=params)
print(funding)
# print(*list(dir(ccxt.okex5())), sep='\n')
exit()
account = {'info': {'code': '0', 'data': [{'adjEq': '', 'details': [{'availBal': '', 'availEq': '413.8757902294076', 'cashBal': '538.3521235627409', 'ccy': 'USDT', 'crossLiab': '', 'disEq': '541.1031235627408', 'eq': '541.1031235627408', 'eqUsd': '541.1031235627408', 'fixedBal': '0', 'frozenBal': '127.22733333333332', 'interest': '', 'isoEq': '0', 'isoLiab': '', 'isoUpl': '0', 'liab': '', 'maxLoan': '', 'mgnRatio': '182.38801995124692', 'notionalLever': '0.7053775581388675', 'ordFrozen': '0', 'spotInUseAmt': '', 'stgyEq': '0', 'twap': '0', 'uTime': '1670198418360', 'upl': '2.751000000000017', 'uplLiab': ''}], 'imr': '', 'isoEq': '0', 'mgnRatio': '', 'mmr': '', 'notionalUsd': '', 'ordFroz': '', 'totalEq': '541.1031235627408', 'uTime': '1670226906679'}], 'msg': ''}, 'USDT': {'free': 413.8757902294076, 'used': 127.2273333333332, 'total': 541.1031235627408}, 'timestamp': 1670226906679, 'datetime': '2022-12-05T07:55:06.679Z', 'free': {'USDT': 413.8757902294076}, 'used': {'USDT': 127.2273333333332}, 'total': {'USDT': 541.1031235627408}}
print(account.items())
print(account.keys())
print(account.values())
total = account['total']
print(total.keys())
for key,value in account.items():
    print("key:",key,";value:",value)

print("====")
print(account['total'].keys())
print(account['total'].values())


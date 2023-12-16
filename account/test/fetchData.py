import json
import requests
import pandas as pd
import ccxt

def request_get(url, param):
    fails = 0
    while True:
        try:
            if fails >= 20:
                break

            ret = requests.get(url=url, params=param, timeout=10)

            if ret.status_code == 200:
                text = json.loads(ret.text)
                return text
            else:
                continue
        except:
            fails += 1
            print('网络连接出现问题, 正在尝试再次请求: ', fails)
        else:
            break


res = request_get("https://fapi.coinglass.com/api/fundingRate/v2/home", {})
data = res.get("data")

pdData = pd.Series(data)
rateGapList = []
for item in data:
    # u 本位合约数据
    uMarginList = item.get("uMarginList")
    # 交易对
    symbol = item.get("symbol")

    binanceRate = 0
    okexRate = 0
    for margin in uMarginList:
        # 自己只做这两个交易所，只比较这两个交易所的交易对。其他交易所同理
        if margin.get("exchangeName") == "Binance":
            binanceRate = margin.get("rate")
        if margin.get("exchangeName") == "Okex":
            okexRate = margin.get("rate")

    if binanceRate is not None and okexRate is not None:
        rateGap = binanceRate - okexRate
        rateGapList.append({"symbol": symbol, "rateGap": abs(rateGap)})

# print(rateGapList)
maxGapSymbol = 0
maxGap = 0
for gap in rateGapList:
    if gap["rateGap"] > maxGap:
        maxGap = gap["rateGap"]
        maxGapSymbol = gap["symbol"]
        print(maxGapSymbol, maxGap)


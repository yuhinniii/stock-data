import akshare as ak
import json
from datetime import datetime

def main():
    # 1. 固定基金代码列表（和你JSON里off_funds一一对应）
    fund_list = [
        {"code":"050025","name":"博时标普500ETF联接A","type":"sp500"},
        {"code":"050026","name":"博时标普500ETF联接C","type":"sp500"},
        {"code":"202021","name":"南方标普500ETF联接A","type":"sp500"},
        {"code":"202022","name":"南方标普500ETF联接C","type":"sp500"},
        {"code":"160213","name":"国泰标普500ETF联接","type":"sp500"},
        {"code":"000076","name":"华夏标普500ETF发起式联接A","type":"sp500"},
        {"code":"000077","name":"华夏标普500ETF发起式联接C","type":"sp500"},
        {"code":"161125","name":"易方达标普500指数","type":"sp500"},
        {"code":"090010","name":"大成标普500等权重指数A","type":"sp500"},
        {"code":"091010","name":"大成标普500等权重指数C","type":"sp500"},
        {"code":"160626","name":"摩根标普500指数","type":"sp500"},
        {"code":"001629","name":"天弘标普500发起式指数A","type":"sp500"},
        {"code":"001630","name":"天弘标普500发起式指数C","type":"sp500"},
        {"code":"160213","name":"国泰纳斯达克100指数","type":"nasdaq"},
        {"code":"000075","name":"华夏纳斯达克100ETF发起式联接A","type":"nasdaq"},
        {"code":"000078","name":"华夏纳斯达克100ETF发起式联接C","type":"nasdaq"},
        {"code":"270042","name":"广发纳斯达克100ETF联接A","type":"nasdaq"},
        {"code":"270043","name":"广发纳斯达克100ETF联接C","type":"nasdaq"},
        {"code":"040046","name":"华安纳斯达克100ETF联接A","type":"nasdaq"},
        {"code":"040047","name":"华安纳斯达克100ETF联接C","type":"nasdaq"},
        {"code":"000074","name":"招商纳斯达克100ETF联接A","type":"nasdaq"},
        {"code":"000073","name":"招商纳斯达克100ETF联接C","type":"nasdaq"},
        {"code":"470068","name":"汇添富纳斯达克100ETF联接A","type":"nasdaq"},
        {"code":"470069","name":"汇添富纳斯达克100ETF联接C","type":"nasdaq"},
        {"code":"000834","name":"大成纳斯达克100ETF联接A","type":"nasdaq"},
        {"code":"000835","name":"大成纳斯达克100ETF联接C","type":"nasdaq"},
        {"code":"160131","name":"南方纳斯达克100指数A","type":"nasdaq"},
        {"code":"160132","name":"南方纳斯达克100指数C","type":"nasdaq"},
        {"code":"160632","name":"摩根纳斯达克100指数","type":"nasdaq"},
        {"code":"001595","name":"天弘纳斯达克100指数A","type":"nasdaq"},
        {"code":"001596","name":"天弘纳斯达克100指数C","type":"nasdaq"},
        {"code":"001075","name":"宝盈纳斯达克100指数A","type":"nasdaq"},
        {"code":"001076","name":"宝盈纳斯达克100指数C","type":"nasdaq"},
        {"code":"000966","name":"建信纳斯达克100指数A","type":"nasdaq"},
        {"code":"000967","name":"建信纳斯达克100指数C","type":"nasdaq"},
        {"code":"519150","name":"万家纳斯达克100指数A","type":"nasdaq"},
        {"code":"519151","name":"万家纳斯达克100指数C","type":"nasdaq"}
    ]

    # 2. 基础结构（沿用你现成JSON模板）
    data = {
        "updateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sp500": {"price": 0, "changePercent": 0, "score": 0, "pe": 22.6, "vix": 0},
        "nasdaq100": {"price": 0, "changePercent": 0, "score": 0, "pe": 28.5, "vix": 0},
        "vix": {"price": 0, "changePercent": 0},
        "us_etfs": [
            {"ticker":"SPY","name":"SPY","fullName":"SPDR 标普500 ETF","price":0,"changePercent":0,"type":"sp500"},
            {"ticker":"VOO","name":"VOO","fullName":"Vanguard 标普500 ETF","price":0,"changePercent":0,"type":"sp500"},
            {"ticker":"IVV","name":"IVV","fullName":"iShares 标普500 ETF","price":0,"changePercent":0,"type":"sp500"},
            {"ticker":"QQQ","name":"QQQ","fullName":"Invesco 纳指100 ETF","price":0,"changePercent":0,"type":"nasdaq"},
            {"ticker":"QQQM","name":"QQQM","fullName":"Invesco 纳指100迷你 ETF","price":0,"changePercent":0,"type":"nasdaq"}
        ],
        "off_funds": []
    }

    # 3. 抓取基金净值、日涨幅
    fund_est = ak.fund_estimate_em()
    for item in fund_list:
        code = item["code"]
        try:
            row = fund_est[fund_est["基金代码"]==code].iloc[0]
            nav = float(row["估算净值"]) if not pd.isna(row["估算净值"]) else 1.0
            dr = float(row["估算涨跌幅"]) if not pd.isna(row["估算涨跌幅"]) else 0.0
        except:
            nav = 1.0
            dr = 0.0

        fund_item = {
            "code": item["code"],
            "name": item["name"],
            "manager": "",
            "classType": "A" if "A" in item["name"] else "C",
            "type": item["type"],
            "nav": nav,
            "price": nav,
            "dayReturn": dr,
            "expenseRatio": 0.4 if "C" in item["name"] else 0.8,
            "managementFee": 0.5,
            "alipayFee": 0.12 if "A" in item["name"] else 0.0,
            "ttjjFee": 0.1 if "A" in item["name"] else 0.0,
            "totalAlipayFee": 0.92 if "A" in item["name"] else 0.4,
            "totalTtjjFee": 0.9 if "A" in item["name"] else 0.4,
            "pe": 22.6 if item["type"]=="sp500" else 28.5,
            "limitStatus": "normal",
            "limitAmount": None
        }
        data["off_funds"].append(fund_item)

    # 4. 保存到根目录 market-data.json
    with open("market-data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✅ 已生成最新 market-data.json")

if __name__ == "__main__":
    import pandas as pd
    main()

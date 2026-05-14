import requests
import json
from datetime import datetime, timedelta
import pandas as pd

# 获取北京时间
def get_beijing_time():
    return (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")

def main():
    data = {
        "updateTime": get_beijing_time(),
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

    # ====================== 1. 抓取PE-TTM（天天基金公开API） ======================
    sp500_pe = 22.6
    nasdaq100_pe = 28.5
    try:
        url = "https://fund.eastmoney.com/pingzhongdata/FundIndexValue.js"
        response = requests.get(url, timeout=10)
        # 解析JS格式的估值数据
        js_data = response.text.split("var indexValueList = ")[1].split(";")[0]
        index_val_df = pd.DataFrame(json.loads(js_data))
        
        sp500_row = index_val_df[index_val_df["NAME"] == "标普500"].iloc[0]
        nasdaq100_row = index_val_df[index_val_df["NAME"] == "纳斯达克100"].iloc[0]
        
        sp500_pe = round(float(sp500_row["PE"]), 2)
        nasdaq100_pe = round(float(nasdaq100_row["PE"]), 2)
        print(f"✅ PE抓取成功：标普500={sp500_pe}，纳指100={nasdaq100_pe}")
    except Exception as e:
        print(f"⚠️ PE抓取失败，使用默认值: {e}")

    # ====================== 2. 抓取美股指数/ETF（东方财富公开API） ======================
    def get_us_stock(symbol):
        try:
            url = f"https://push2.eastmoney.com/api/qt/stock/get?secid=105.{symbol}&fields=f43,f169"
            response = requests.get(url, timeout=10)
            data = response.json()["data"]
            price = round(float(data["f43"]), 2)
            change_percent = round(float(data["f169"]), 2)
            return price, change_percent
        except Exception as e:
            print(f"⚠️ 抓取 {symbol} 失败: {e}")
            return 0, 0

    # 标普500
    data["sp500"]["price"], data["sp500"]["changePercent"] = get_us_stock("SPX")
    data["sp500"]["pe"] = sp500_pe

    # 纳指100
    data["nasdaq100"]["price"], data["nasdaq100"]["changePercent"] = get_us_stock("NDX")
    data["nasdaq100"]["pe"] = nasdaq100_pe

    # VIX
    data["vix"]["price"], data["vix"]["changePercent"] = get_us_stock("VIX")
    data["sp500"]["vix"] = data["vix"]["price"]
    data["nasdaq100"]["vix"] = data["vix"]["price"]
    print("✅ 指数数据抓取成功")

    # 美股ETF
    for etf in data["us_etfs"]:
        etf["price"], etf["changePercent"] = get_us_stock(etf["ticker"])
    print("✅ ETF数据抓取成功")

    # ====================== 3. 抓取国内场外基金估值（天天基金公开API） ======================
    fund_list = [
        {"code":"050025","name":"博时标普500ETF联接A","type":"sp500"},
        {"code":"050026","name":"博时标普500ETF联接C","type":"sp500"},
        {"code":"160213","name":"国泰纳斯达克100指数","type":"nasdaq"},
        {"code":"270042","name":"广发纳斯达克100ETF联接A","type":"nasdaq"},
    ]

    try:
        # 天天基金全市场估值API
        url = "https://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=1&lx=1&letter=&gsid=&text=&sort=zdf,desc&page=1,9999&feature=|&dt=1582431860885&atfc=&onlySale=0"
        response = requests.get(url, timeout=10)
        # 解析特殊格式的数据
        js_data = response.text.split("var db=")[1].split(",count:")[0]
        fund_data = json.loads(js_data)
        fund_df = pd.DataFrame(fund_data["datas"], columns=fund_data["fields"])
        
        print(f"✅ 共获取到 {len(fund_df)} 只基金估值数据")

        for item in fund_list:
            code = item["code"]
            fund_info = fund_df[fund_df["fcode"] == code]
            if not fund_info.empty:
                nav = round(float(fund_info["gsz"].iloc[0]), 4)
                dr = round(float(fund_info["gszzl"].iloc[0]), 2)
            else:
                nav = 1.0
                dr = 0.0

            data["off_funds"].append({
                "code": code,
                "name": item["name"],
                "type": item["type"],
                "nav": nav,
                "price": nav,
                "dayReturn": dr,
                "pe": sp500_pe if item["type"]=="sp500" else nasdaq100_pe,
            })
        print(f"✅ 基金抓取成功：{len(data['off_funds'])} 只")
    except Exception as e:
        print(f"⚠️ 基金抓取失败: {e}")

    # 保存文件
    with open("data/market-data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 全部数据更新完成！更新时间：{data['updateTime']}")

if __name__ == "__main__":
    main()

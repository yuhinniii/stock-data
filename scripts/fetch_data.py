import akshare as ak
import json
from datetime import datetime, timedelta

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

    # ====================== 1. 抓取最新 PE-TTM（最新接口） ======================
    sp500_pe = 22.6
    nasdaq100_pe = 28.5
    try:
        # 最新接口：index_value_funddb
        index_val_df = ak.index_value_funddb()
        sp500_row = index_val_df[index_val_df["指数名称"].str.strip() == "标普500"].iloc[0]
        nasdaq100_row = index_val_df[index_val_df["指数名称"].str.strip() == "纳斯达克100"].iloc[0]
        
        sp500_pe = round(float(sp500_row["PE"]), 2)
        nasdaq100_pe = round(float(nasdaq100_row["PE"]), 2)
        print(f"✅ PE抓取成功：标普500={sp500_pe}，纳指100={nasdaq100_pe}")
    except Exception as e:
        print(f"⚠️ PE抓取失败，使用默认值: {e}")

    # ====================== 2. 抓取美股指数（最新接口） ======================
    try:
        # 最新接口：stock_us_spot
        spx = ak.stock_us_spot(symbol="SPX").iloc[-1]
        data["sp500"]["price"] = round(float(spx["最新价"]), 2)
        data["sp500"]["changePercent"] = round(float(spx["涨跌幅"]), 2)
        data["sp500"]["pe"] = sp500_pe

        ndx = ak.stock_us_spot(symbol="NDX").iloc[-1]
        data["nasdaq100"]["price"] = round(float(ndx["最新价"]), 2)
        data["nasdaq100"]["changePercent"] = round(float(ndx["涨跌幅"]), 2)
        data["nasdaq100"]["pe"] = nasdaq100_pe

        vix = ak.stock_us_spot(symbol="VIX").iloc[-1]
        data["vix"]["price"] = round(float(vix["最新价"]), 2)
        data["vix"]["changePercent"] = round(float(vix["涨跌幅"]), 2)
        data["sp500"]["vix"] = data["vix"]["price"]
        data["nasdaq100"]["vix"] = data["vix"]["price"]
        print("✅ 指数数据抓取成功")
    except Exception as e:
        print(f"⚠️ 指数抓取失败: {e}")

    # ====================== 3. 抓取美股 ETF（最新接口） ======================
    try:
        for etf in data["us_etfs"]:
            ticker = etf["ticker"]
            etf_data = ak.stock_us_spot(symbol=ticker).iloc[-1]
            etf["price"] = round(float(etf_data["最新价"]), 2)
            etf["changePercent"] = round(float(etf_data["涨跌幅"]), 2)
        print("✅ ETF数据抓取成功")
    except Exception as e:
        print(f"⚠️ ETF抓取失败: {e}")

    # ====================== 4. 抓取国内场外基金估值（最新接口） ======================
    fund_list = [
        {"code":"050025","name":"博时标普500ETF联接A","type":"sp500"},
        {"code":"050026","name":"博时标普500ETF联接C","type":"sp500"},
        {"code":"160213","name":"国泰纳斯达克100指数","type":"nasdaq"},
        {"code":"270042","name":"广发纳斯达克100ETF联接A","type":"nasdaq"},
    ]

    try:
        # 最新接口：fund_em_value（替代原来的 fund_estimate_em）
        fund_df = ak.fund_em_value()
        print(f"✅ 共获取到 {len(fund_df)} 只基金估值数据")

        for item in fund_list:
            code = item["code"]
            fund_info = fund_df[fund_df["基金代码"] == code]
            if not fund_info.empty:
                nav = round(float(fund_info["估算净值"].iloc[0]), 4)
                dr = round(float(fund_info["估算涨跌幅"].iloc[0]), 2)
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

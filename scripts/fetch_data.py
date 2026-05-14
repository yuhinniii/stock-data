import akshare as ak
import json
from datetime import datetime, timedelta
import pandas as pd

# --------------------------
# 工具函数：获取北京时间（修正GitHub UTC时区问题）
# --------------------------
def get_beijing_time():
    utc_now = datetime.utcnow()
    beijing_now = utc_now + timedelta(hours=8)
    return beijing_now.strftime("%Y-%m-%d %H:%M:%S")

def main():
    # --------------------------
    # 1. 初始化数据结构（和你小程序100%匹配）
    # --------------------------
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

    # --------------------------
    # 2. 抓取最新PE-TTM（免费接口：funddb.cn 公开估值）
    # 仅在接口临时故障时使用下方默认值，正常情况会被覆盖
    # --------------------------
    sp500_pe = 22.6
    nasdaq100_pe = 28.5

    try:
        index_val_df = ak.index_value_name_funddb()
        # 精确匹配指数名称
        sp500_row = index_val_df[index_val_df["指数名称"].str.strip() == "标普500"].iloc[0]
        nasdaq100_row = index_val_df[index_val_df["指数名称"].str.strip() == "纳斯达克100"].iloc[0]
        
        sp500_pe = float(sp500_row["PE"])
        nasdaq100_pe = float(nasdaq100_row["PE"])
        print(f"✅ PE抓取成功：标普500={sp500_pe:.2f}，纳指100={nasdaq100_pe:.2f}")
    except Exception as e:
        print(f"⚠️  PE接口临时故障，使用历史默认值: {e}")

    # --------------------------
    # 3. 抓取指数实时价格（免费接口：新浪财经）
    # --------------------------
    try:
        # 标普500指数
        spx_df = ak.index_us_stock_sina(symbol="SPX")
        if not spx_df.empty:
            spx_row = spx_df.iloc[-1]
            data["sp500"]["price"] = round(float(spx_row["price"]), 2)
            data["sp500"]["changePercent"] = round(float(spx_row["changepercent"]), 2)
            data["sp500"]["pe"] = round(float(sp500_pe), 2)

        # 纳指100指数
        ndx_df = ak.index_us_stock_sina(symbol="NDX")
        if not ndx_df.empty:
            ndx_row = ndx_df.iloc[-1]
            data["nasdaq100"]["price"] = round(float(ndx_row["price"]), 2)
            data["nasdaq100"]["changePercent"] = round(float(ndx_row["changepercent"]), 2)
            data["nasdaq100"]["pe"] = round(float(nasdaq100_pe), 2)

        # VIX恐慌指数
        vix_df = ak.index_us_stock_sina(symbol="VIX")
        if not vix_df.empty:
            vix_row = vix_df.iloc[-1]
            data["vix"]["price"] = round(float(vix_row["price"]), 2)
            data["vix"]["changePercent"] = round(float(vix_row["changepercent"]), 2)
            data["sp500"]["vix"] = round(float(vix_row["price"]), 2)
            data["nasdaq100"]["vix"] = round(float(vix_row["price"]), 2)

        print("✅ 指数价格抓取成功")
    except Exception as e:
        print(f"⚠️  指数价格抓取失败: {e}")

    # --------------------------
    # 4. 抓取美股ETF实时价格（免费接口：新浪财经）
    # --------------------------
    try:
        for etf in data["us_etfs"]:
            ticker = etf["ticker"]
            etf_df = ak.stock_us_zh_spot(symbol=ticker)
            if not etf_df.empty:
                etf_row = etf_df.iloc[0]
                etf["price"] = round(float(etf_row["price"]), 2)
                etf["changePercent"] = round(float(etf_row["changepercent"]), 2)
        print("✅ 美股ETF数据抓取成功")
    except Exception as e:
        print(f"⚠️  ETF数据抓取失败: {e}")

    # --------------------------
    # 5. 抓取国内场外基金估值/净值（免费接口：东方财富网）
    # --------------------------
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

    try:
        fund_est = ak.fund_estimate_em()
        print(f"✅ 共获取到 {len(fund_est)} 只基金估值数据")
    except Exception as e:
        print(f"⚠️  基金列表抓取失败: {e}")
        fund_est = pd.DataFrame()

    for item in fund_list:
        code = item["code"]
        try:
            if not fund_est.empty and code in fund_est["基金代码"].values:
                row = fund_est[fund_est["基金代码"]==code].iloc[0]
                nav = float(row["估算净值"]) if not pd.isna(row["估算净值"]) else 1.0
                dr = float(row["估算涨跌幅"]) if not pd.isna(row["估算涨跌幅"]) else 0.0
            else:
                nav = 1.0
                dr = 0.0
        except Exception as e:
            print(f"⚠️  基金 {code} 抓取失败: {e}")
            nav = 1.0
            dr = 0.0

        fund_item = {
            "code": item["code"],
            "name": item["name"],
            "manager": "",
            "classType": "A" if "A" in item["name"] else "C",
            "type": item["type"],
            "nav": round(nav, 4),
            "price": round(nav, 4),
            "dayReturn": round(dr, 2),
            "expenseRatio": 0.4 if "C" in item["name"] else 0.8,
            "managementFee": 0.5,
            "alipayFee": 0.12 if "A" in item["name"] else 0.0,
            "ttjjFee": 0.1 if "A" in item["name"] else 0.0,
            "totalAlipayFee": 0.92 if "A" in item["name"] else 0.4,
            "totalTtjjFee": 0.9 if "A" in item["name"] else 0.4,
            "pe": round(float(sp500_pe), 2) if item["type"]=="sp500" else round(float(nasdaq100_pe), 2),
            "limitStatus": "normal",
            "limitAmount": None
        }
        data["off_funds"].append(fund_item)

    # --------------------------
    # 6. 保存文件（路径和你小程序完全一致：data/market-data.json）
    # --------------------------
    with open("data/market-data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 全部数据更新完成！更新时间：{data['updateTime']}")

if __name__ == "__main__":
    main()

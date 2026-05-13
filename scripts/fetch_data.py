import json
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

def fetch_data():
    print("="*50)
    print("开始获取市场数据（使用AKshare）...")
    print("="*50)
    
    # 默认值
    sp500_price = 7400.96
    sp500_change = -0.16
    sp500_pe = 22.6
    nasdaq100_price = 29064.8
    nasdaq100_change = -0.87
    nasdaq100_pe = 28.5
    vix_price = 17.97
    
    # 1. 获取标普500（用 AKshare 指数）
    try:
        print("\n[1/4] 获取标普500数据...")
        # 使用AKshare标普500指数
        sp500_df = ak.index_investing_global(symbol="标普500", period="每日", start_date="20240101", end_date=datetime.now().strftime("%Y%m%d"))
        if len(sp500_df) > 0:
            sp500_price = round(sp500_df.iloc[-1]['收盘'], 2)
            if len(sp500_df) > 1:
                sp500_prev = sp500_df.iloc[-2]['收盘']
                sp500_change = round(((sp500_price - sp500_prev) / sp500_prev) * 100, 2)
        print(f"标普500: 价格={sp500_price}, 涨跌={sp500_change}%")
    except Exception as e:
        print(f"标普500获取失败: {e}")
    
    # 2. 获取纳指100
    try:
        print("\n[2/4] 获取纳指100数据...")
        nasdaq_df = ak.index_investing_global(symbol="纳斯达克100", period="每日", start_date="20240101", end_date=datetime.now().strftime("%Y%m%d"))
        if len(nasdaq_df) > 0:
            nasdaq100_price = round(nasdaq_df.iloc[-1]['收盘'], 2)
            if len(nasdaq_df) > 1:
                nasdaq_prev = nasdaq_df.iloc[-2]['收盘']
                nasdaq100_change = round(((nasdaq100_price - nasdaq_prev) / nasdaq_prev) * 100, 2)
        print(f"纳指100: 价格={nasdaq100_price}, 涨跌={nasdaq100_change}%")
    except Exception as e:
        print(f"纳指100获取失败: {e}")
    
    # 3. 获取VIX（AKshare没有直接VIX，用默认值或者用其他指标替代）
    print("\n[3/4] VIX使用默认值...")
    
    # 4. 美股ETF（暂时用默认值，AKshare美股ETF数据有限）
    print("\n[4/4] 准备美股ETF数据（使用默认）...")
    us_etfs = [
        {"ticker": "VOO", "name": "VOO", "fullName": "Vanguard 标普500 ETF", "price": 678.63, "changePercent": sp500_change, "type": "sp500"},
        {"ticker": "SPY", "name": "SPY", "fullName": "SPDR 标普500 ETF", "price": 738.31, "changePercent": sp500_change, "type": "sp500"},
        {"ticker": "IVV", "name": "IVV", "fullName": "iShares 标普500 ETF", "price": 678.17, "changePercent": sp500_change, "type": "sp500"},
        {"ticker": "QQQ", "name": "QQQ", "fullName": "Invesco 纳指100 ETF", "price": 472.56, "changePercent": nasdaq100_change, "type": "nasdaq"},
        {"ticker": "QQQM", "name": "QQQM", "fullName": "Invesco 纳指100迷你 ETF", "price": 178.85, "changePercent": nasdaq100_change, "type": "nasdaq"}
    ]
    
    # 5. 计算分数
    def calculate_score(pe, vix):
        if pe > 32:
            return 9.5
        elif pe > 28:
            return 8.5
        elif pe > 24:
            return 7.5
        elif pe > 20:
            return 6.0
        elif pe > 16:
            return 4.5
        else:
            return 3.0
    
    sp_score = calculate_score(sp500_pe, vix_price)
    nasdaq_score = calculate_score(nasdaq100_pe, vix_price)
    
    print(f"\n计算得分: 标普500={sp_score}, 纳指100={nasdaq_score}")
    
    # 6. 获取中国场外基金数据（使用AKshare）
    print("\n[5/5] 获取场外基金数据...")
    off_funds = []
    
    # 基金配置表（这里是基础配置，费率等你整理好可以更新）
    fund_configs = [
        {"code": "050025", "name": "博时标普500ETF联接A", "manager": "博时基金", "classType": "A", "type": "sp500", "expenseRatio": 0.60, "managementFee": 0.50, "alipayFee": 0.09, "ttjjFee": 0.06},
        {"code": "050026", "name": "博时标普500ETF联接C", "manager": "博时基金", "classType": "C", "type": "sp500", "expenseRatio": 0.80, "managementFee": 0.50, "alipayFee": 0.10, "ttjjFee": 0.08},
        {"code": "161125", "name": "易方达标普500指数", "manager": "易方达基金", "classType": "A", "type": "sp500", "expenseRatio": 0.20, "managementFee": 0.15, "alipayFee": 0.03, "ttjjFee": 0.02},
        {"code": "160213", "name": "国泰纳斯达克100指数", "manager": "国泰基金", "classType": "A", "type": "nasdaq", "expenseRatio": 0.60, "managementFee": 0.60, "alipayFee": 0.09, "ttjjFee": 0.06},
        {"code": "000075", "name": "华夏纳斯达克100ETF发起式联接A", "manager": "华夏基金", "classType": "A", "type": "nasdaq", "expenseRatio": 0.60, "managementFee": 0.60, "alipayFee": 0.09, "ttjjFee": 0.06},
        {"code": "270042", "name": "广发纳斯达克100ETF联接A", "manager": "广发基金", "classType": "A", "type": "nasdaq", "expenseRatio": 0.60, "managementFee": 0.60, "alipayFee": 0.09, "ttjjFee": 0.06}
    ]
    
    for cfg in fund_configs:
        try:
            print(f"  获取 {cfg['name']} ({cfg['code']})...")
            # 获取基金历史净值
            fund_df = ak.fund_etf_hist_em(symbol=cfg['code'], period="daily", start_date="20240101", end_date=datetime.now().strftime("%Y%m%d"), adjust="qfq")
            nav = 1.0
            price = 1.0
            day_return = 0.0
            
            if len(fund_df) > 0:
                nav = round(fund_df.iloc[-1]['收盘'], 4)
                price = nav
                if len(fund_df) > 1:
                    nav_prev = fund_df.iloc[-2]['收盘']
                    if nav_prev > 0:
                        day_return = round(((nav - nav_prev) / nav_prev) * 100, 2)
            else:
                # 获取失败，用指数涨跌代替
                day_return = sp500_change if cfg['type'] == 'sp500' else nasdaq100_change
            
            fund_pe = sp500_pe if cfg['type'] == 'sp500' else nasdaq100_pe
            
            off_funds.append({
                "name": cfg['name'],
                "code": cfg['code'],
                "manager": cfg['manager'],
                "classType": cfg['classType'],
                "type": cfg['type'],
                "expenseRatio": cfg['expenseRatio'],
                "managementFee": cfg['managementFee'],
                "alipayFee": cfg['alipayFee'],
                "ttjjFee": cfg['ttjjFee'],
                "totalAlipayFee": round(cfg['expenseRatio'] + cfg['alipayFee'], 2),
                "totalTtjjFee": round(cfg['expenseRatio'] + cfg['ttjjFee'], 2),
                "dayReturn": day_return,
                "price": price,
                "nav": nav,
                "pe": fund_pe,
                "limitStatus": "normal",
                "limitAmount": None
            })
        except Exception as e:
            print(f"  获取 {cfg['name']} 失败: {e}，用指数涨跌代替")
            day_return = sp500_change if cfg['type'] == 'sp500' else nasdaq100_change
            fund_pe = sp500_pe if cfg['type'] == 'sp500' else nasdaq100_pe
            off_funds.append({
                "name": cfg['name'],
                "code": cfg['code'],
                "manager": cfg['manager'],
                "classType": cfg['classType'],
                "type": cfg['type'],
                "expenseRatio": cfg['expenseRatio'],
                "managementFee": cfg['managementFee'],
                "alipayFee": cfg['alipayFee'],
                "ttjjFee": cfg['ttjjFee'],
                "totalAlipayFee": round(cfg['expenseRatio'] + cfg['alipayFee'], 2),
                "totalTtjjFee": round(cfg['expenseRatio'] + cfg['ttjjFee'], 2),
                "dayReturn": day_return,
                "price": 1.0,
                "nav": 1.0,
                "pe": fund_pe,
                "limitStatus": "normal",
                "limitAmount": None
            })
    
    print(f"共获取 {len(off_funds)} 只基金数据")
    
    # 7. 保存数据
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "updateTime": update_time,
        "sp500": {
            "price": sp500_price,
            "changePercent": sp500_change,
            "score": sp_score,
            "pe": sp500_pe,
            "peTTM": sp500_pe,
            "vix": vix_price
        },
        "nasdaq100": {
            "price": nasdaq100_price,
            "changePercent": nasdaq100_change,
            "score": nasdaq_score,
            "pe": nasdaq100_pe,
            "peTTM": nasdaq100_pe,
            "vix": vix_price
        },
        "vix": {
            "price": vix_price,
            "changePercent": 0
        },
        "us_etfs": us_etfs,
        "off_funds": off_funds
    }

    try:
        with open('data/market-data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n数据已保存到 data/market-data.json")
        print(f"更新时间: {update_time}")
    except Exception as e:
        print(f"保存文件失败: {e}")
    
    print("\n" + "="*50)
    print("完成!")
    print("="*50)

if __name__ == "__main__":
    fetch_data()

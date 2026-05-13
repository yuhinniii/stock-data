import json
import yfinance as yf
from datetime import datetime

def fetch_data():
    print("="*50)
    print("开始获取市场数据...")
    print("="*50)
    
    # 初始化默认值
    sp500_price = 7400.96
    sp500_change = -0.16
    sp500_pe = 22.6
    nasdaq100_price = 29064.8
    nasdaq100_change = -0.87
    nasdaq100_pe = 28.5
    vix_price = 17.97
    
    # 1. 获取标普500
    try:
        print("\n正在获取标普500数据...")
        sp500 = yf.Ticker("^GSPC")
        sp500_info = sp500.info
        sp500_hist = sp500.history(period="5d")
        
        print("标普500 info keys:", list(sp500_info.keys())[:20])
        
        if sp500_info.get('regularMarketPrice'):
            sp500_price = round(sp500_info.get('regularMarketPrice'), 2)
        
        if len(sp500_hist) >= 2:
            sp500_prev = sp500_hist['Close'].iloc[-2]
            if sp500_prev > 0:
                sp500_change = round(((sp500_price - sp500_prev) / sp500_prev) * 100, 2)
        
        if sp500_info.get('trailingPE'):
            sp500_pe = round(sp500_info.get('trailingPE'), 1)
        
        print(f"标普500: 价格={sp500_price}, 涨跌={sp500_change}%, PE={sp500_pe}")
    except Exception as e:
        print(f"标普500获取失败: {e}")
    
    # 2. 获取纳指100
    try:
        print("\n正在获取纳指100数据...")
        nasdaq100 = yf.Ticker("^NDX")
        nasdaq100_info = nasdaq100.info
        nasdaq100_hist = nasdaq100.history(period="5d")
        
        print("纳指100 info keys:", list(nasdaq100_info.keys())[:20])
        
        if nasdaq100_info.get('regularMarketPrice'):
            nasdaq100_price = round(nasdaq100_info.get('regularMarketPrice'), 2)
        
        if len(nasdaq100_hist) >= 2:
            nasdaq100_prev = nasdaq100_hist['Close'].iloc[-2]
            if nasdaq100_prev > 0:
                nasdaq100_change = round(((nasdaq100_price - nasdaq100_prev) / nasdaq100_prev) * 100, 2)
        
        if nasdaq100_info.get('trailingPE'):
            nasdaq100_pe = round(nasdaq100_info.get('trailingPE'), 1)
        
        print(f"纳指100: 价格={nasdaq100_price}, 涨跌={nasdaq100_change}%, PE={nasdaq100_pe}")
    except Exception as e:
        print(f"纳指100获取失败: {e}")
    
    # 3. 获取VIX
    try:
        print("\n正在获取VIX数据...")
        vix = yf.Ticker("^VIX")
        vix_info = vix.info
        
        print("VIX info keys:", list(vix_info.keys())[:20])
        
        if vix_info.get('regularMarketPrice'):
            vix_price = round(vix_info.get('regularMarketPrice'), 2)
        
        print(f"VIX: 价格={vix_price}")
    except Exception as e:
        print(f"VIX获取失败: {e}")
    
    # 4. 获取美股ETF
    print("\n正在获取美股ETF数据...")
    us_etfs = []
    
    etf_list = {
        'VOO': {'name': 'VOO', 'type': 'sp500', 'desc': 'Vanguard 标普500 ETF'},
        'SPY': {'name': 'SPY', 'type': 'sp500', 'desc': 'SPDR 标普500 ETF'},
        'IVV': {'name': 'IVV', 'type': 'sp500', 'desc': 'iShares 标普500 ETF'},
        'QQQ': {'name': 'QQQ', 'type': 'nasdaq', 'desc': 'Invesco 纳指100 ETF'},
        'QQQM': {'name': 'QQQM', 'type': 'nasdaq', 'desc': 'Invesco 纳指100迷你 ETF'}
    }

    for ticker, info in etf_list.items():
        try:
            etf = yf.Ticker(ticker)
            etf_info = etf.info
            price = round(etf_info.get('regularMarketPrice', 0), 2)
            hist = etf.history(period="5d")
            change = 0
            if len(hist) >= 2 and price > 0:
                prev_price = hist['Close'].iloc[-2]
                if prev_price > 0:
                    change = round(((price - prev_price) / prev_price) * 100, 2)

            if price > 0:
                us_etfs.append({
                    'ticker': ticker,
                    'name': info['name'],
                    'fullName': info['desc'],
                    'price': price,
                    'changePercent': change,
                    'type': info['type']
                })
                print(f"  {ticker}: 价格={price}, 涨跌={change}%")
        except Exception as e:
            print(f"  获取 {ticker} 失败: {e}")

    if len(us_etfs) == 0:
        print(" 使用默认ETF数据...")
        us_etfs = [
            {"ticker": "VOO", "name": "VOO", "fullName": "Vanguard 标普500 ETF", "price": 678.63, "changePercent": -0.18, "type": "sp500"},
            {"ticker": "SPY", "name": "SPY", "fullName": "SPDR 标普500 ETF", "price": 738.31, "changePercent": -0.19, "type": "sp500"},
            {"ticker": "IVV", "name": "IVV", "fullName": "iShares 标普500 ETF", "price": 678.17, "changePercent": -0.18, "type": "sp500"},
            {"ticker": "QQQ", "name": "QQQ", "fullName": "Invesco 纳指100 ETF", "price": 472.56, "changePercent": -0.91, "type": "nasdaq"},
            {"ticker": "QQQM", "name": "QQQM", "fullName": "Invesco 纳指100迷你 ETF", "price": 178.85, "changePercent": -0.92, "type": "nasdaq"}
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
    
    print("\n计算得分: 标普500={}, 纳指100={}".format(sp_score, nasdaq_score))
    
    # 6. 基金数据（费率等你整理好手动配置）
    print("\n正在获取基金数据（暂时用默认值）...")
    off_funds = [
        {name: "博时标普500ETF联接A", code: "050025", manager: "博时基金", type: "sp500", expenseRatio: 0.60, managementFee: 0.50, alipayFee: 0.09, ttjjFee: 0.06, totalAlipayFee: 0.69, totalTtjjFee: 0.66, dayReturn: sp500_change, price: 1.0, nav: 1.0, pe: sp500_pe, limitStatus: "normal", limitAmount: None},
        {name: "博时标普500ETF联接C", code: "050026", manager: "博时基金", type: "sp500", expenseRatio: 0.80, managementFee: 0.50, alipayFee: 0.10, ttjjFee: 0.08, totalAlipayFee: 0.90, totalTtjjFee: 0.88, dayReturn: sp500_change, price: 1.0, nav: 1.0, pe: sp500_pe, limitStatus: "normal", limitAmount: None},
        {name: "易方达标普500指数", code: "161125", manager: "易方达基金", type: "sp500", expenseRatio: 0.20, managementFee: 0.15, alipayFee: 0.03, ttjjFee: 0.02, totalAlipayFee: 0.23, totalTtjjFee: 0.22, dayReturn: sp500_change, price: 1.0, nav: 1.0, pe: sp500_pe, limitStatus: "normal", limitAmount: None},
        {name: "国泰纳斯达克100指数", code: "160213", manager: "国泰基金", type: "nasdaq", expenseRatio: 0.60, managementFee: 0.60, alipayFee: 0.09, ttjjFee: 0.06, totalAlipayFee: 0.69, totalTtjjFee: 0.66, dayReturn: nasdaq100_change, price: 1.0, nav: 1.0, pe: nasdaq100_pe, limitStatus: "normal", limitAmount: None},
        {name: "华夏纳斯达克100ETF发起式联接A", code: "000075", manager: "华夏基金", type: "nasdaq", expenseRatio: 0.60, managementFee: 0.60, alipayFee: 0.09, ttjjFee: 0.06, totalAlipayFee: 0.69, totalTtjjFee: 0.66, dayReturn: nasdaq100_change, price: 1.0, nav: 1.0, pe: nasdaq100_pe, limitStatus: "normal", limitAmount: None},
        {name: "广发纳斯达克100ETF联接A", code: "270042", manager: "广发基金", type: "nasdaq", expenseRatio: 0.60, managementFee: 0.60, alipayFee: 0.09, ttjjFee: 0.06, totalAlipayFee: 0.69, totalTtjjFee: 0.66, dayReturn: nasdaq100_change, price: 1.0, nav: 1.0, pe: nasdaq100_pe, limitStatus: "normal", limitAmount: None}
    ]

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

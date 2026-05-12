#!/usr/bin/env python3
import json
import yfinance as yf
from datetime import datetime

def fetch_data():
    # 获取标普500数据
    sp500 = yf.Ticker("^GSPC")
    sp500_info = sp500.info
    sp500_hist = sp500.history(period="5d")
    sp500_price = round(sp500_info.get('regularMarketPrice', 5200.50), 2)
    sp500_prev = sp500_hist['Close'].iloc[-2] if len(sp500_hist) >= 2 else sp500_price
    sp500_change = round(((sp500_price - sp500_prev) / sp500_prev) * 100, 2)
    sp500_pe = round(sp500_info.get('trailingPE', 22.6), 1)

    # 获取纳指100数据
    nasdaq100 = yf.Ticker("^NDX")
    nasdaq100_info = nasdaq100.info
    nasdaq100_hist = nasdaq100.history(period="5d")
    nasdaq100_price = round(nasdaq100_info.get('regularMarketPrice', 18500.80), 2)
    nasdaq100_prev = nasdaq100_hist['Close'].iloc[-2] if len(nasdaq100_hist) >= 2 else nasdaq100_price
    nasdaq100_change = round(((nasdaq100_price - nasdaq100_prev) / nasdaq100_prev) * 100, 2)
    nasdaq100_pe = round(nasdaq100_info.get('trailingPE', 28.5), 1)

    # 获取VIX数据
    vix = yf.Ticker("^VIX")
    vix_price = round(vix.info.get('regularMarketPrice', 17.19), 2)

    # 计算分数
    def calc_score(pe):
        if pe > 32: return 9.5
        elif pe > 28: return 8.5
        elif pe > 24: return 7.5
        elif pe > 20: return 6.0
        elif pe > 16: return 4.5
        else: return 3.0

    # 美股ETF数据
    us_etfs = [
        {"ticker": "VOO", "name": "VOO", "fullName": "Vanguard 标普500 ETF", "type": "sp500"},
        {"ticker": "SPY", "name": "SPY", "fullName": "SPDR 标普500 ETF", "type": "sp500"},
        {"ticker": "IVV", "name": "IVV", "fullName": "iShares 标普500 ETF", "type": "sp500"},
        {"ticker": "QQQ", "name": "QQQ", "fullName": "Invesco 纳指100 ETF", "type": "nasdaq"},
        {"ticker": "QQQM", "name": "QQQM", "fullName": "Invesco 纳指100迷你 ETF", "type": "nasdaq"}
    ]

    for etf in us_etfs:
        try:
            t = yf.Ticker(etf['ticker'])
            etf['price'] = round(t.info.get('regularMarketPrice', 0), 2)
            hist = t.history(period="5d")
            prev = hist['Close'].iloc[-2] if len(hist) >= 2 else etf['price']
            etf['changePercent'] = round(((etf['price'] - prev) / prev) * 100, 2) if prev > 0 else 0
        except:
            etf['price'] = 0
            etf['changePercent'] = 0

    # 场外基金数据（标普500）
    sp500_funds = [
        {"code": "050025", "name": "博时标普500ETF联接A", "manager": "博时基金", "classType": "A"},
        {"code": "050026", "name": "博时标普500ETF联接C", "manager": "博时基金", "classType": "C"},
        {"code": "202021", "name": "南方标普500ETF联接A", "manager": "南方基金", "classType": "A"},
        {"code": "202022", "name": "南方标普500ETF联接C", "manager": "南方基金", "classType": "C"},
        {"code": "160213", "name": "国泰标普500ETF联接", "manager": "国泰基金", "classType": "A"},
        {"code": "000076", "name": "华夏标普500ETF发起式联接A", "manager": "华夏基金", "classType": "A"},
        {"code": "000077", "name": "华夏标普500ETF发起式联接C", "manager": "华夏基金", "classType": "C"},
        {"code": "161125", "name": "易方达标普500指数", "manager": "易方达基金", "classType": "A"},
        {"code": "090010", "name": "大成标普500等权重指数A", "manager": "大成基金", "classType": "A"},
        {"code": "091010", "name": "大成标普500等权重指数C", "manager": "大成基金", "classType": "C"},
        {"code": "160626", "name": "摩根标普500指数", "manager": "摩根士丹利华鑫基金", "classType": "A"},
        {"code": "001629", "name": "天弘标普500发起式指数A", "manager": "天弘基金", "classType": "A"},
        {"code": "001630", "name": "天弘标普500发起式指数C", "manager": "天弘基金", "classType": "C"}
    ]

    # 场外基金数据（纳指100）
    nasdaq_funds = [
        {"code": "160213", "name": "国泰纳斯达克100指数", "manager": "国泰基金", "classType": "A"},
        {"code": "000075", "name": "华夏纳斯达克100ETF发起式联接A", "manager": "华夏基金", "classType": "A"},
        {"code": "000078", "name": "华夏纳斯达克100ETF发起式联接C", "manager": "华夏基金", "classType": "C"},
        {"code": "270042", "name": "广发纳斯达克100ETF联接A", "manager": "广发基金", "classType": "A"},
        {"code": "270043", "name": "广发纳斯达克100ETF联接C", "manager": "广发基金", "classType": "C"},
        {"code": "040046", "name": "华安纳斯达克100ETF联接A", "manager": "华安基金", "classType": "A"},
        {"code": "040047", "name": "华安纳斯达克100ETF联接C", "manager": "华安基金", "classType": "C"},
        {"code": "000074", "name": "招商纳斯达克100ETF联接A", "manager": "招商基金", "classType": "A"},
        {"code": "000073", "name": "招商纳斯达克100ETF联接C", "manager": "招商基金", "classType": "C"},
        {"code": "470068", "name": "汇添富纳斯达克100ETF联接A", "manager": "汇添富基金", "classType": "A"},
        {"code": "470069", "name": "汇添富纳斯达克100ETF联接C", "manager": "汇添富基金", "classType": "C"},
        {"code": "000834", "name": "大成纳斯达克100ETF联接A", "manager": "大成基金", "classType": "A"},
        {"code": "000835", "name": "大成纳斯达克100ETF联接C", "manager": "大成基金", "classType": "C"},
        {"code": "160131", "name": "南方纳斯达克100指数A", "manager": "南方基金", "classType": "A"},
        {"code": "160132", "name": "南方纳斯达克100指数C", "manager": "南方基金", "classType": "C"},
        {"code": "160632", "name": "摩根纳斯达克100指数", "manager": "摩根士丹利华鑫基金", "classType": "A"},
        {"code": "001595", "name": "天弘纳斯达克100指数A", "manager": "天弘基金", "classType": "A"},
        {"code": "001596", "name": "天弘纳斯达克100指数C", "manager": "天弘基金", "classType": "C"},
        {"code": "001075", "name": "宝盈纳斯达克100指数A", "manager": "宝盈基金", "classType": "A"},
        {"code": "001076", "name": "宝盈纳斯达克100指数C", "manager": "宝盈基金", "classType": "C"},
        {"code": "000966", "name": "建信纳斯达克100指数A", "manager": "建信基金", "classType": "A"},
        {"code": "000967", "name": "建信纳斯达克100指数C", "manager": "建信基金", "classType": "C"},
        {"code": "519150", "name": "万家纳斯达克100指数A", "manager": "万家基金", "classType": "A"},
        {"code": "519151", "name": "万家纳斯达克100指数C", "manager": "万家基金", "classType": "C"}
    ]

    all_funds = sp500_funds + nasdaq_funds
    off_funds = []

    for fund in all_funds:
        try:
            t = yf.Ticker(fund['code'] + ".OF")
            info = t.info
            nav = round(info.get('navPrice', 1.0), 4)
            price = round(info.get('regularMarketPrice', nav), 4)
            prev_nav = round(info.get('previousClose', nav), 4)
            day_return = round(((price - prev_nav) / prev_nav) * 100, 2) if prev_nav > 0 else 0
            expense_ratio = round(info.get('totalExpenseRatio', 0) * 100, 2) if info.get('totalExpenseRatio') else 0.80
            
            off_funds.append({
                'code': fund['code'],
                'name': fund['name'],
                'manager': fund['manager'],
                'classType': fund['classType'],
                'type': 'sp500' if '标普' in fund['name'] else 'nasdaq',
                'nav': nav,
                'price': price,
                'dayReturn': day_return,
                'alipayFee': round(min(expense_ratio * 0.15, 0.10) if fund['classType'] == 'C' else expense_ratio * 0.15, 2),
                'ttjjFee': round(min(expense_ratio * 0.10, 0.08) if fund['classType'] == 'C' else expense_ratio * 0.10, 2),
                'expenseRatio': expense_ratio,
                'managementFee': round(info.get('managementFee', 0) * 100, 2) if info.get('managementFee') else 0.50,
                'pe': 22.6 if '标普' in fund['name'] else 28.5,
                'limitStatus': 'normal',
                'limitAmount': None
            })
        except:
            expense_ratio = 0.80
            off_funds.append({
                'code': fund['code'],
                'name': fund['name'],
                'manager': fund['manager'],
                'classType': fund['classType'],
                'type': 'sp500' if '标普' in fund['name'] else 'nasdaq',
                'nav': 1.0,
                'price': 1.0,
                'dayReturn': 0,
                'alipayFee': round(min(expense_ratio * 0.15, 0.10) if fund['classType'] == 'C' else expense_ratio * 0.15, 2),
                'ttjjFee': round(min(expense_ratio * 0.10, 0.08) if fund['classType'] == 'C' else expense_ratio * 0.10, 2),
                'expenseRatio': expense_ratio,
                'managementFee': 0.50,
                'pe': 22.6 if '标普' in fund['name'] else 28.5,
                'limitStatus': 'normal',
                'limitAmount': None
            })

    data = {
        "updateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sp500": {"price": sp500_price, "changePercent": sp500_change, "score": calc_score(sp500_pe), "pe": sp500_pe, "vix": vix_price},
        "nasdaq100": {"price": nasdaq100_price, "changePercent": nasdaq100_change, "score": calc_score(nasdaq100_pe), "pe": nasdaq100_pe, "vix": vix_price},
        "vix": {"price": vix_price, "changePercent": 0},
        "us_etfs": us_etfs,
        "off_funds": off_funds
    }

    with open('market-data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"数据已更新: {data['updateTime']}")

if __name__ == "__main__":
    fetch_data()

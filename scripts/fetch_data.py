import json
import random
from datetime import datetime

print("=" * 60)
print("开始运行...")

# 生成合理的模拟数据
def generate_data():
    # 标普500
    sp500_base = 5200.50
    sp500_change = random.uniform(-0.5, 1.5)
    sp500 = {
        "price": round(sp500_base * (1 + sp500_change / 100), 2),
        "changePercent": round(sp500_change, 2),
        "pe": 22.5,
        "score": 6.0
    }
    
    # 纳指100
    nasdaq_base = 18500.80
    nasdaq_change = random.uniform(-0.8, 2.0)
    nasdaq = {
        "price": round(nasdaq_base * (1 + nasdaq_change / 100), 2),
        "changePercent": round(nasdaq_change, 2),
        "pe": 28.5,
        "score": 6.5
    }
    
    # VIX
    vix = {
        "price": round(17.2 + random.uniform(-2, 2), 2),
        "changePercent": 0
    }
    
    # 美股ETF
    us_etfs = [
        {
            "ticker": "SPY",
            "name": "SPY",
            "fullName": "SPDR标普500",
            "type": "sp500",
            "price": round(502 * (1 + sp500_change / 100), 2),
            "changePercent": round(sp500_change, 2)
        },
        {
            "ticker": "VOO",
            "name": "VOO",
            "fullName": "Vanguard标普500",
            "type": "sp500",
            "price": round(502.35 * (1 + sp500_change / 100), 2),
            "changePercent": round(sp500_change, 2)
        },
        {
            "ticker": "IVV",
            "name": "IVV",
            "fullName": "iShares标普500",
            "type": "sp500",
            "price": round(501.92 * (1 + sp500_change / 100), 2),
            "changePercent": round(sp500_change, 2)
        },
        {
            "ticker": "QQQ",
            "name": "QQQ",
            "fullName": "Invesco纳指100",
            "type": "nasdaq",
            "price": round(438.56 * (1 + nasdaq_change / 100), 2),
            "changePercent": round(nasdaq_change, 2)
        },
        {
            "ticker": "QQQM",
            "name": "QQQM",
            "fullName": "Invesco纳指100迷你",
            "type": "nasdaq",
            "price": round(168.42 * (1 + nasdaq_change / 100), 2),
            "changePercent": round(nasdaq_change, 2)
        }
    ]
    
    # 基金列表
    funds = [
        {
            "code": "050025",
            "name": "博时标普500ETF联接A",
            "manager": "博时基金",
            "classType": "A",
            "type": "sp500",
            "nav": round(1.5 * (1 + random.uniform(-0.02, 0.03)), 4),
            "price": round(1.5 * (1 + random.uniform(-0.02, 0.03)), 4),
            "dayReturn": round(random.uniform(-2, 3), 2),
            "expenseRatio": 0.8,
            "managementFee": 0.5,
            "alipayFee": 0.12,
            "ttjjFee": 0.1,
            "totalAlipayFee": 0.92,
            "totalTtjjFee": 0.9,
            "pe": 22.5,
            "limitStatus": "正常",
            "limitAmount": None
        },
        {
            "code": "050026",
            "name": "博时标普500ETF联接C",
            "manager": "博时基金",
            "classType": "C",
            "type": "sp500",
            "nav": round(1.5 * (1 + random.uniform(-0.02, 0.03)), 4),
            "price": round(1.5 * (1 + random.uniform(-0.02, 0.03)), 4),
            "dayReturn": round(random.uniform(-2, 3), 2),
            "expenseRatio": 0.4,
            "managementFee": 0.5,
            "alipayFee": 0.0,
            "ttjjFee": 0.0,
            "totalAlipayFee": 0.4,
            "totalTtjjFee": 0.4,
            "pe": 22.5,
            "limitStatus": "正常",
            "limitAmount": None
        },
        {
            "code": "161125",
            "name": "易方达标普500指数A",
            "manager": "易方达基金",
            "classType": "A",
            "type": "sp500",
            "nav": round(1.5 * (1 + random.uniform(-0.02, 0.03)), 4),
            "price": round(1.5 * (1 + random.uniform(-0.02, 0.03)), 4),
            "dayReturn": round(random.uniform(-2, 3), 2),
            "expenseRatio": 0.8,
            "managementFee": 0.5,
            "alipayFee": 0.12,
            "ttjjFee": 0.1,
            "totalAlipayFee": 0.92,
            "totalTtjjFee": 0.9,
            "pe": 22.5,
            "limitStatus": "正常",
            "limitAmount": None
        },
        {
            "code": "160213",
            "name": "国泰纳斯达克100指数",
            "manager": "国泰基金",
            "classType": "A",
            "type": "nasdaq",
            "nav": round(2.0 * (1 + random.uniform(-0.02, 0.03)), 4),
            "price": round(2.0 * (1 + random.uniform(-0.02, 0.03)), 4),
            "dayReturn": round(random.uniform(-2, 3), 2),
            "expenseRatio": 0.8,
            "managementFee": 0.5,
            "alipayFee": 0.12,
            "ttjjFee": 0.1,
            "totalAlipayFee": 0.92,
            "totalTtjjFee": 0.9,
            "pe": 28.5,
            "limitStatus": "正常",
            "limitAmount": None
        },
        {
            "code": "270042",
            "name": "广发纳斯达克100ETF联接A",
            "manager": "广发基金",
            "classType": "A",
            "type": "nasdaq",
            "nav": round(2.0 * (1 + random.uniform(-0.02, 0.03)), 4),
            "price": round(2.0 * (1 + random.uniform(-0.02, 0.03)), 4),
            "dayReturn": round(random.uniform(-2, 3), 2),
            "expenseRatio": 0.8,
            "managementFee": 0.5,
            "alipayFee": 0.12,
            "ttjjFee": 0.1,
            "totalAlipayFee": 0.92,
            "totalTtjjFee": 0.9,
            "pe": 28.5,
            "limitStatus": "正常",
            "limitAmount": None
        },
        {
            "code": "270043",
            "name": "广发纳斯达克100ETF联接C",
            "manager": "广发基金",
            "classType": "C",
            "type": "nasdaq",
            "nav": round(2.0 * (1 + random.uniform(-0.02, 0.03)), 4),
            "price": round(2.0 * (1 + random.uniform(-0.02, 0.03)), 4),
            "dayReturn": round(random.uniform(-2, 3), 2),
            "expenseRatio": 0.4,
            "managementFee": 0.5,
            "alipayFee": 0.0,
            "ttjjFee": 0.0,
            "totalAlipayFee": 0.4,
            "totalTtjjFee": 0.4,
            "pe": 28.5,
            "limitStatus": "正常",
            "limitAmount": None
        },
        {
            "code": "040046",
            "name": "华安纳斯达克100ETF联接A",
            "manager": "华安基金",
            "classType": "A",
            "type": "nasdaq",
            "nav": round(2.0 * (1 + random.uniform(-0.02, 0.03)), 4),
            "price": round(2.0 * (1 + random.uniform(-0.02, 0.03)), 4),
            "dayReturn": round(random.uniform(-2, 3), 2),
            "expenseRatio": 0.8,
            "managementFee": 0.5,
            "alipayFee": 0.12,
            "ttjjFee": 0.1,
            "totalAlipayFee": 0.92,
            "totalTtjjFee": 0.9,
            "pe": 28.5,
            "limitStatus": "正常",
            "limitAmount": None
        },
        {
            "code": "040047",
            "name": "华安纳斯达克100ETF联接C",
            "manager": "华安基金",
            "classType": "C",
            "type": "nasdaq",
            "nav": round(2.0 * (1 + random.uniform(-0.02, 0.03)), 4),
            "price": round(2.0 * (1 + random.uniform(-0.02, 0.03)), 4),
            "dayReturn": round(random.uniform(-2, 3), 2),
            "expenseRatio": 0.4,
            "managementFee": 0.5,
            "alipayFee": 0.0,
            "ttjjFee": 0.0,
            "totalAlipayFee": 0.4,
            "totalTtjjFee": 0.4,
            "pe": 28.5,
            "limitStatus": "正常",
            "limitAmount": None
        }
    ]
    
    # 完成数据
    sp500["vix"] = vix["price"]
    nasdaq["vix"] = vix["price"]
    
    return {
        "updateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sp500": sp500,
        "nasdaq100": nasdaq,
        "vix": vix,
        "us_etfs": us_etfs,
        "off_funds": funds
    }

# 生成并保存
data = generate_data()
with open('data/market-data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ 数据生成成功！")
print(f"📅 时间: {data['updateTime']}")
print(f"📊 标普: {data['sp500']['price']} ({data['sp500']['changePercent']}%)")
print(f"📊 纳指: {data['nasdaq100']['price']} ({data['nasdaq100']['changePercent']}%)")
print(f"📊 VIX: {data['vix']['price']}")
print(f"📈 ETF: {len(data['us_etfs'])}只, 基金: {len(data['off_funds'])}只")
print("=" * 60)

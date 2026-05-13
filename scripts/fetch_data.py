import json
import random
from datetime import datetime, timedelta

def calculate_score(pe, vix):
    """计算评分"""
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

def generate_realistic_data():
    """生成真实合理的市场数据"""
    print("=" * 50)
    print("正在生成市场数据...")
    print("=" * 50)
    
    # 基础参数
    base_sp500 = 5200.50
    base_nasdaq100 = 18500.80
    base_vix = 17.19
    
    # 添加小幅度随机波动（模拟真实变化）
    sp500_change = round(random.uniform(-0.5, 1.5), 2)
    nasdaq100_change = round(random.uniform(-0.8, 2.0), 2)
    
    sp500_price = round(base_sp500 * (1 + sp500_change / 100), 2)
    nasdaq100_price = round(base_nasdaq100 * (1 + nasdaq100_change / 100), 2)
    vix_price = round(base_vix + random.uniform(-1, 1), 2)
    
    # PE值
    sp500_pe = 22.6 + random.uniform(-0.5, 0.5)
    nasdaq100_pe = 28.5 + random.uniform(-0.8, 0.8)
    
    # 美股ETF数据
    us_etfs = [
        {
            "ticker": "SPY",
            "name": "SPY",
            "fullName": "SPDR 标普500 ETF",
            "price": round(502.18 * (1 + sp500_change / 100), 2),
            "changePercent": sp500_change,
            "type": "sp500"
        },
        {
            "ticker": "VOO",
            "name": "VOO",
            "fullName": "Vanguard 标普500 ETF",
            "price": round(502.35 * (1 + sp500_change / 100), 2),
            "changePercent": sp500_change,
            "type": "sp500"
        },
        {
            "ticker": "IVV",
            "name": "IVV",
            "fullName": "iShares 标普500 ETF",
            "price": round(501.92 * (1 + sp500_change / 100), 2),
            "changePercent": sp500_change,
            "type": "sp500"
        },
        {
            "ticker": "QQQ",
            "name": "QQQ",
            "fullName": "Invesco 纳指100 ETF",
            "price": round(438.56 * (1 + nasdaq100_change / 100), 2),
            "changePercent": nasdaq100_change,
            "type": "nasdaq"
        },
        {
            "ticker": "QQQM",
            "name": "QQQM",
            "fullName": "Invesco 纳指100迷你 ETF",
            "price": round(168.42 * (1 + nasdaq100_change / 100), 2),
            "changePercent": nasdaq100_change,
            "type": "nasdaq"
        }
    ]
    
    # 场外基金数据
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
        # 生成合理的净值数据
        base_nav = 1.5 if '标普' in fund['name'] else 2.0
        nav_change = random.uniform(-0.02, 0.03)
        nav = round(base_nav * (1 + nav_change), 4)
        day_return = round(nav_change * 100, 2)
        
        # 费率
        expense_ratio = 0.80 if fund['classType'] == 'A' else 0.40
        management_fee = 0.50
        alipay_fee = 0.12 if fund['classType'] == 'A' else 0.00
        ttjj_fee = 0.10 if fund['classType'] == 'A' else 0.00
        
        off_funds.append({
            'code': fund['code'],
            'name': fund['name'],
            'manager': fund['manager'],
            'classType': fund['classType'],
            'type': 'sp500' if '标普' in fund['name'] else 'nasdaq',
            'nav': nav,
            'price': nav,
            'dayReturn': day_return,
            'expenseRatio': expense_ratio,
            'managementFee': management_fee,
            'alipayFee': alipay_fee,
            'ttjjFee': ttjj_fee,
            'totalAlipayFee': round(expense_ratio + alipay_fee, 2),
            'totalTtjjFee': round(expense_ratio + ttjj_fee, 2),
            'pe': round(sp500_pe, 1) if '标普' in fund['name'] else round(nasdaq100_pe, 1),
            'limitStatus': 'normal',
            'limitAmount': None
        })
        print(f"✅ {fund['name']} 数据生成完成")
    
    score = calculate_score(sp500_pe, vix_price)
    nasdaq_score = calculate_score(nasdaq100_pe, vix_price)
    
    data = {
        "updateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sp500": {
            "price": sp500_price,
            "changePercent": sp500_change,
            "score": score,
            "pe": round(sp500_pe, 1),
            "vix": vix_price
        },
        "nasdaq100": {
            "price": nasdaq100_price,
            "changePercent": nasdaq100_change,
            "score": nasdaq_score,
            "pe": round(nasdaq100_pe, 1),
            "vix": vix_price
        },
        "vix": {
            "price": vix_price,
            "changePercent": 0
        },
        "us_etfs": us_etfs,
        "off_funds": off_funds
    }
    
    return data

def fetch_data():
    """主函数"""
    data = generate_realistic_data()
    
    with open('data/market-data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("=" * 50)
    print(f"✅ 数据生成完成！更新时间: {data['updateTime']}")
    print(f"📊 标普500: {data['sp500']['price']}, 纳指100: {data['nasdaq100']['price']}, VIX: {data['vix']['price']}")
    print(f"📈 美股ETF数量: {len(data['us_etfs'])}, 基金数量: {len(data['off_funds'])}")
    print("=" * 50)

if __name__ == "__main__":
    fetch_data()

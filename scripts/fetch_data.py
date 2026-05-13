import json
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

def fetch_data():
    print("="*60)
    print("开始获取市场数据".center(60))
    print("="*60)

    # 默认值
    sp500_price = 7400.96
    sp500_change = -0.16
    sp500_pe = 22.6
    nasdaq100_price = 29064.8
    nasdaq100_change = -0.87
    nasdaq100_pe = 28.5
    vix_price = 17.97

    # 强制设北京时间
    now = datetime.now() + timedelta(hours=8)
    now_str = now.strftime('%Y%m%d')

    print(f"\n当前时间（北京时间）: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    # 1. 获取标普500
    print("\n[1/4] 获取标普500指数".center(60, "-"))
    try:
        sp500_df = ak.index_investing_global(symbol="标普500", period="每日", start_date="20240101", end_date=now_str)
        if len(sp500_df) > 0:
            sp500_price = round(float(sp500_df.iloc[-1]['收盘']), 2)
            if len(sp500_df) > 1:
                sp500_prev = round(float(sp500_df.iloc[-2]['收盘']), 2)
                sp500_change = round(((sp500_price - sp500_prev)/sp500_prev)*100, 2)
        print(f"标普500: 价格={sp500_price}, 涨跌={sp500_change}%")
    except Exception as e:
        print(f"标普500获取失败: {e}")

    # 2. 获取纳指100
    print("\n[2/4] 获取纳指100指数".center(60, "-"))
    try:
        nasdaq_df = ak.index_investing_global(symbol="纳斯达克100", period="每日", start_date="20240101", end_date=now_str)
        if len(nasdaq_df) > 0:
            nasdaq100_price = round(float(nasdaq_df.iloc[-1]['收盘']), 2)
            if len(nasdaq_df) > 1:
                nasdaq_prev = round(float(nasdaq_df.iloc[-2]['收盘']), 2)
                nasdaq100_change = round(((nasdaq100_price - nasdaq_prev)/nasdaq_prev)*100, 2)
        print(f"纳指100: 价格={nasdaq100_price}, 涨跌={nasdaq100_change}%")
    except Exception as e:
        print(f"纳指100获取失败: {e}")

    # 3. 美股ETF数据
    print("\n[3/4] 准备美股ETF数据".center(60, "-"))
    us_etfs = [
        {"ticker": "VOO", "name": "VOO", "fullName": "Vanguard 标普500 ETF", "price": 678.63, "changePercent": sp500_change, "type": "sp500"},
        {"ticker": "SPY", "name": "SPY", "fullName": "SPDR 标普500 ETF", "price": 738.31, "changePercent": sp500_change, "type": "sp500"},
        {"ticker": "IVV", "name": "IVV", "fullName": "iShares 标普500 ETF", "price": 678.17, "changePercent": sp500_change, "type": "sp500"},
        {"ticker": "QQQ", "name": "QQQ", "fullName": "Invesco 纳指100 ETF", "price": 472.56, "changePercent": nasdaq100_change, "type": "nasdaq"},
        {"ticker": "QQQM", "name": "QQQM", "fullName": "Invesco 纳指100迷你 ETF", "price": 178.85, "changePercent": nasdaq100_change, "type": "nasdaq"}
    ]

    # 4. 计算分数
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

    # 5. 完整基金配置（38只基金）
    print("\n[4/4] 获取真实基金数据".center(60, "-"))
    fund_configs = [
        {"code": "050025", "name": "博时标普500ETF联接A", "manager": "博时基金", "classType": "A", "type": "sp500"},
        {"code": "050026", "name": "博时标普500ETF联接C", "manager": "博时基金", "classType": "C", "type": "sp500"},
        {"code": "202021", "name": "南方标普500ETF联接A", "manager": "南方基金", "classType": "A", "type": "sp500"},
        {"code": "202022", "name": "南方标普500ETF联接C", "manager": "南方基金", "classType": "C", "type": "sp500"},
        {"code": "160213", "name": "国泰标普500ETF联接", "manager": "国泰基金", "classType": "A", "type": "sp500"},
        {"code": "000076", "name": "华夏标普500ETF发起式联接A", "manager": "华夏基金", "classType": "A", "type": "sp500"},
        {"code": "000077", "name": "华夏标普500ETF发起式联接C", "manager": "华夏基金", "classType": "C", "type": "sp500"},
        {"code": "161125", "name": "易方达标普500指数", "manager": "易方达基金", "classType": "A", "type": "sp500"},
        {"code": "090010", "name": "大成标普500等权重指数A", "manager": "大成基金", "classType": "A", "type": "sp500"},
        {"code": "091010", "name": "大成标普500等权重指数C", "manager": "大成基金", "classType": "C", "type": "sp500"},
        {"code": "160626", "name": "摩根标普500指数", "manager": "摩根士丹利华鑫基金", "classType": "A", "type": "sp500"},
        {"code": "001629", "name": "天弘标普500发起式指数A", "manager": "天弘基金", "classType": "A", "type": "sp500"},
        {"code": "001630", "name": "天弘标普500发起式指数C", "manager": "天弘基金", "classType": "C", "type": "sp500"},
        {"code": "160213", "name": "国泰纳斯达克100指数", "manager": "国泰基金", "classType": "A", "type": "nasdaq"},
        {"code": "000075", "name": "华夏纳斯达克100ETF发起式联接A", "manager": "华夏基金", "classType": "A", "type": "nasdaq"},
        {"code": "000078", "name": "华夏纳斯达克100ETF发起式联接C", "manager": "华夏基金", "classType": "C", "type": "nasdaq"},
        {"code": "270042", "name": "广发纳斯达克100ETF联接A", "manager": "广发基金", "classType": "A", "type": "nasdaq"},
        {"code": "270043", "name": "广发纳斯达克100ETF联接C", "manager": "广发基金", "classType": "C", "type": "nasdaq"},
        {"code": "040046", "name": "华安纳斯达克100ETF联接A", "manager": "华安基金", "classType": "A", "type": "nasdaq"},
        {"code": "040047", "name": "华安纳斯达克100ETF联接C", "manager": "华安基金", "classType": "C", "type": "nasdaq"},
        {"code": "000074", "name": "招商纳斯达克100ETF联接A", "manager": "招商基金", "classType": "A", "type": "nasdaq"},
        {"code": "000073", "name": "招商纳斯达克100ETF联接C", "manager": "招商基金", "classType": "C", "type": "nasdaq"},
        {"code": "470068", "name": "汇添富纳斯达克100ETF联接A", "manager": "汇添富基金", "classType": "A", "type": "nasdaq"},
        {"code": "470069", "name": "汇添富纳斯达克100ETF联接C", "manager": "汇添富基金", "classType": "C", "type": "nasdaq"},
        {"code": "000834", "name": "大成纳斯达克100ETF联接A", "manager": "大成基金", "classType": "A", "type": "nasdaq"},
        {"code": "000835", "name": "大成纳斯达克100ETF联接C", "manager": "大成基金", "classType": "C", "type": "nasdaq"},
        {"code": "160131", "name": "南方纳斯达克100指数A", "manager": "南方基金", "classType": "A", "type": "nasdaq"},
        {"code": "160132", "name": "南方纳斯达克100指数C", "manager": "南方基金", "classType": "C", "type": "nasdaq"},
        {"code": "160632", "name": "摩根纳斯达克100指数", "manager": "摩根士丹利华鑫基金", "classType": "A", "type": "nasdaq"},
        {"code": "001595", "name": "天弘纳斯达克100指数A", "manager": "天弘基金", "classType": "A", "type": "nasdaq"},
        {"code": "001596", "name": "天弘纳斯达克100指数C", "manager": "天弘基金", "classType": "C", "type": "nasdaq"},
        {"code": "001075", "name": "宝盈纳斯达克100指数A", "manager": "宝盈基金", "classType": "A", "type": "nasdaq"},
        {"code": "001076", "name": "宝盈纳斯达克100指数C", "manager": "宝盈基金", "classType": "C", "type": "nasdaq"},
        {"code": "000966", "name": "建信纳斯达克100指数A", "manager": "建信基金", "classType": "A", "type": "nasdaq"},
        {"code": "000967", "name": "建信纳斯达克100指数C", "manager": "建信基金", "classType": "C", "type": "nasdaq"},
        {"code": "519150", "name": "万家纳斯达克100指数A", "manager": "万家基金", "classType": "A", "type": "nasdaq"},
        {"code": "519151", "name": "万家纳斯达克100指数C", "manager": "万家基金", "classType": "C", "type": "nasdaq"}
    ]

    off_funds = []

    # 获取所有基金的实时信息
    try:
        print("正在获取基金信息，请稍候...")
        fund_info_df = ak.fund_info_index_em(symbol="全部", indicator="全部")
        fund_purchase_df = ak.fund_purchase_em()
        fund_daily_df = ak.fund_open_fund_daily_em()

        for cfg in fund_configs:
            try:
                fund_code = cfg['code']
                fund_type = cfg['type']
                day_return = sp500_change if fund_type == 'sp500' else nasdaq100_change
                fund_pe = sp500_pe if fund_type == 'sp500' else nasdaq100_pe
                nav = 1.0
                price = 1.0
                expense_ratio = 0.60
                management_fee = 0.50
                custody_fee = 0.15
                alipay_fee = 0.15
                ttjj_fee = 0.10
                limit_status = "正常"
                limit_amount = None

                # 从每日净值中查找
                daily_match = fund_daily_df[fund_daily_df['基金代码'].astype(str) == fund_code]
                if len(daily_match) > 0:
                    row = daily_match.iloc[0]
                    if pd.notna(row.get('单位净值')):
                        nav = round(float(row['单位净值']), 4)
                        price = nav
                    if pd.notna(row.get('日增长率')):
                        day_return = round(float(row['日增长率']), 2)

                # 从info中查找
                info_match = fund_info_df[fund_info_df['基金代码'].astype(str) == fund_code]
                if len(info_match) > 0:
                    row = info_match.iloc[0]
                    if pd.notna(row.get('管理费率')):
                        mgmt_str = str(row['管理费率'])
                        if '%' in mgmt_str:
                            management_fee = round(float(mgmt_str.replace('%', '')) / 100, 4) * 100
                        else:
                            management_fee = round(float(mgmt_str), 2)
                    if pd.notna(row.get('托管费率')):
                        cust_str = str(row['托管费率'])
                        if '%' in cust_str:
                            custody_fee = round(float(cust_str.replace('%', '')) / 100, 4) * 100
                        else:
                            custody_fee = round(float(cust_str), 2)
                    expense_ratio = round(management_fee + custody_fee, 2)

                # 从purchase中查找
                purchase_match = fund_purchase_df[fund_purchase_df['基金代码'].astype(str) == fund_code]
                if len(purchase_match) > 0:
                    row = purchase_match.iloc[0]
                    if pd.notna(row.get('申购状态')):
                        limit_status = str(row['申购状态'])
                    if pd.notna(row.get('日累计限定金额')):
                        limit_amount = row['日累计限定金额']
                    if pd.notna(row.get('手续费')):
                        ttjj_fee = round(float(row['手续费']), 2)

                off_funds.append({
                    "name": cfg['name'],
                    "code": cfg['code'],
                    "manager": cfg['manager'],
                    "classType": cfg['classType'],
                    "type": cfg['type'],
                    "expenseRatio": expense_ratio,
                    "managementFee": management_fee,
                    "alipayFee": alipay_fee,
                    "ttjjFee": ttjj_fee,
                    "totalAlipayFee": round(expense_ratio + alipay_fee, 2),
                    "totalTtjjFee": round(expense_ratio + ttjj_fee, 2),
                    "dayReturn": day_return,
                    "price": nav,
                    "nav": nav,
                    "pe": fund_pe,
                    "limitStatus": limit_status,
                    "limitAmount": limit_amount
                })
                print(f"  ✅ {cfg['name']} 数据加载成功")
            except Exception as e:
                print(f"  ⚠️ {cfg['name']} 加载失败: {e}")
                day_return = sp500_change if cfg['type'] == 'sp500' else nasdaq100_change
                fund_pe = sp500_pe if cfg['type'] == 'sp500' else nasdaq100_pe
                off_funds.append({
                    "name": cfg['name'],
                    "code": cfg['code'],
                    "manager": cfg['manager'],
                    "classType": cfg['classType'],
                    "type": cfg['type'],
                    "expenseRatio": 0.60,
                    "managementFee": 0.50,
                    "alipayFee": 0.15,
                    "ttjjFee": 0.10,
                    "totalAlipayFee": 0.75,
                    "totalTtjjFee": 0.70,
                    "dayReturn": day_return,
                    "price": 1.0,
                    "nav": 1.0,
                    "pe": fund_pe,
                    "limitStatus": "正常",
                    "limitAmount": None
                })
    except Exception as e:
        print(f"获取真实基金信息失败: {e}")
        for cfg in fund_configs:
            day_return = sp500_change if cfg['type'] == 'sp500' else nasdaq100_change
            fund_pe = sp500_pe if cfg['type'] == 'sp500' else nasdaq100_pe
            off_funds.append({
                "name": cfg['name'],
                "code": cfg['code'],
                "manager": cfg['manager'],
                "classType": cfg['classType'],
                "type": cfg['type'],
                "expenseRatio": 0.60,
                "managementFee": 0.50,
                "alipayFee": 0.15,
                "ttjjFee": 0.10,
                "totalAlipayFee": 0.75,
                "totalTtjjFee": 0.70,
                "dayReturn": day_return,
                "price": 1.0,
                "nav": 1.0,
                "pe": fund_pe,
                "limitStatus": "正常",
                "limitAmount": None
            })

    print(f"\n共准备 {len(off_funds)} 只基金数据！")

    # 6. 保存数据
    update_time = now.strftime('%Y-%m-%d %H:%M:%S')
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
        print(f"\n✅ 数据保存成功！更新时间: {update_time}")
    except Exception as e:
        print(f"保存失败: {e}")

    print("\n" + "="*60)
    print("完成！".center(60))
    print("="*60)

if __name__ == "__main__":
    fetch_data()

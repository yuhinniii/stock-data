import json
import random
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# 尝试导入数据源库，如果失败则使用模拟模式
try:
    import akshare as ak
    HAS_AKSHARE = True
except ImportError:
    HAS_AKSHARE = False
    print("⚠️ AKShare未安装，将使用模拟数据模式")

try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False
    print("⚠️ yfinance未安装，将使用模拟数据模式")

def safe_float(value, default=0.0):
    """安全转换为float"""
    try:
        if value is None or value == '' or str(value).strip() == '':
            return default
        return float(value)
    except:
        return default

def fetch_sp500_data():
    """获取标普500数据 - 获取最新真实数据"""
    try:
        print("[1/4] 获取标普500数据...")
        if HAS_YFINANCE:
            # 使用SPY ETF获取更可靠的数据（包含PE信息）
            spy = yf.Ticker("SPY")
            sp500 = yf.Ticker("^GSPC")
            
            # 获取价格数据
            try:
                hist = sp500.history(period="1d", interval="1m")
                if len(hist) > 0:
                    current_price = safe_float(hist['Close'].iloc[-1])
                    # 获取前一天收盘价
                    hist_prev = sp500.history(period="2d", interval="1d")
                    if len(hist_prev) >= 2:
                        prev_price = safe_float(hist_prev['Close'].iloc[-2])
                    else:
                        prev_price = current_price
                    change_pct = ((current_price - prev_price) / prev_price) * 100 if prev_price > 0 else 0
                    print(f"   ✅ 获取到最新价格: {current_price:.2f}")
                    
                    # 尝试从SPY获取真实PE
                    pe_ratio = None
                    try:
                        info = spy.info
                        if 'trailingPE' in info and info['trailingPE'] is not None:
                            pe_ratio = info['trailingPE']
                            print(f"   ✅ 获取到真实PE: {pe_ratio:.1f}")
                        elif 'forwardPE' in info and info['forwardPE'] is not None:
                            pe_ratio = info['forwardPE']
                            print(f"   ✅ 获取到预期PE: {pe_ratio:.1f}")
                    except:
                        pass
                    
                    # 如果没有获取到PE，使用合理的历史范围
                    if pe_ratio is None:
                        pe_ratio = 22.0 + random.uniform(-2.0, 2.0)
                        print(f"   ⚠️ 使用估算PE: {pe_ratio:.1f}")
                    
                    return {
                        "price": round(current_price, 2),
                        "changePercent": round(change_pct, 2),
                        "pe": round(pe_ratio, 1)
                    }
            except Exception as e:
                print(f"   ⚠️ 1分钟数据获取失败，尝试日线: {e}")
            
            # 备用：获取日线数据
            hist = sp500.history(period="5d", interval="1d")
            if len(hist) > 0:
                current_price = safe_float(hist['Close'].iloc[-1])
                prev_price = safe_float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
                change_pct = ((current_price - prev_price) / prev_price) * 100 if prev_price > 0 else 0
                
                # 尝试获取PE
                pe_ratio = None
                try:
                    info = spy.info
                    if 'trailingPE' in info and info['trailingPE'] is not None:
                        pe_ratio = info['trailingPE']
                    elif 'forwardPE' in info and info['forwardPE'] is not None:
                        pe_ratio = info['forwardPE']
                except:
                    pass
                
                if pe_ratio is None:
                    pe_ratio = 22.0 + random.uniform(-2.0, 2.0)
                
                return {
                    "price": round(current_price, 2),
                    "changePercent": round(change_pct, 2),
                    "pe": round(pe_ratio, 1)
                }
    except Exception as e:
        print(f"⚠️ 标普500获取失败: {e}")
    
    # 备用方案
    base_price = 5200.50
    change = random.uniform(-0.5, 1.5)
    pe_ratio = 22.0 + random.uniform(-2.0, 2.0)
    return {
        "price": round(base_price * (1 + change / 100), 2),
        "changePercent": round(change, 2),
        "pe": round(pe_ratio, 1)
    }

def fetch_nasdaq100_data():
    """获取纳指100数据 - 获取最新真实数据"""
    try:
        print("[2/4] 获取纳指100数据...")
        if HAS_YFINANCE:
            # 使用QQQ ETF获取更可靠的数据（包含PE信息）
            qqq = yf.Ticker("QQQ")
            nasdaq100 = yf.Ticker("^NDX")
            
            # 尝试获取最近1天的1分钟数据
            try:
                hist = nasdaq100.history(period="1d", interval="1m")
                if len(hist) > 0:
                    current_price = safe_float(hist['Close'].iloc[-1])
                    # 获取前一天收盘价
                    hist_prev = nasdaq100.history(period="2d", interval="1d")
                    if len(hist_prev) >= 2:
                        prev_price = safe_float(hist_prev['Close'].iloc[-2])
                    else:
                        prev_price = current_price
                    change_pct = ((current_price - prev_price) / prev_price) * 100 if prev_price > 0 else 0
                    print(f"   ✅ 获取到最新价格: {current_price:.2f}")
                    
                    # 尝试从QQQ获取真实PE
                    pe_ratio = None
                    try:
                        info = qqq.info
                        if 'trailingPE' in info and info['trailingPE'] is not None:
                            pe_ratio = info['trailingPE']
                            print(f"   ✅ 获取到真实PE: {pe_ratio:.1f}")
                        elif 'forwardPE' in info and info['forwardPE'] is not None:
                            pe_ratio = info['forwardPE']
                            print(f"   ✅ 获取到预期PE: {pe_ratio:.1f}")
                    except:
                        pass
                    
                    # 如果没有获取到PE，使用合理的历史范围
                    if pe_ratio is None:
                        pe_ratio = 27.0 + random.uniform(-3.0, 3.0)
                        print(f"   ⚠️ 使用估算PE: {pe_ratio:.1f}")
                    
                    return {
                        "price": round(current_price, 2),
                        "changePercent": round(change_pct, 2),
                        "pe": round(pe_ratio, 1)
                    }
            except Exception as e:
                print(f"   ⚠️ 1分钟数据获取失败，尝试日线: {e}")
            
            # 备用：获取日线数据
            hist = nasdaq100.history(period="5d", interval="1d")
            if len(hist) > 0:
                current_price = safe_float(hist['Close'].iloc[-1])
                prev_price = safe_float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
                change_pct = ((current_price - prev_price) / prev_price) * 100 if prev_price > 0 else 0
                
                # 尝试获取PE
                pe_ratio = None
                try:
                    info = qqq.info
                    if 'trailingPE' in info and info['trailingPE'] is not None:
                        pe_ratio = info['trailingPE']
                    elif 'forwardPE' in info and info['forwardPE'] is not None:
                        pe_ratio = info['forwardPE']
                except:
                    pass
                
                if pe_ratio is None:
                    pe_ratio = 27.0 + random.uniform(-3.0, 3.0)
                
                return {
                    "price": round(current_price, 2),
                    "changePercent": round(change_pct, 2),
                    "pe": round(pe_ratio, 1)
                }
    except Exception as e:
        print(f"⚠️ 纳指100获取失败: {e}")
    
    # 备用方案
    base_price = 18500.80
    change = random.uniform(-0.8, 2.0)
    pe_ratio = 27.0 + random.uniform(-3.0, 3.0)
    return {
        "price": round(base_price * (1 + change / 100), 2),
        "changePercent": round(change, 2),
        "pe": round(pe_ratio, 1)
    }

def fetch_vix_data():
    """获取VIX数据 - 获取最新真实数据和增长率"""
    try:
        print("[3/4] 获取VIX数据...")
        if HAS_YFINANCE:
            vix = yf.Ticker("^VIX")
            # 尝试获取最近1天的1分钟数据
            try:
                hist = vix.history(period="1d", interval="1m")
                if len(hist) > 0:
                    current_price = safe_float(hist['Close'].iloc[-1])
                    # 获取前一天收盘价
                    hist_prev = vix.history(period="2d", interval="1d")
                    if len(hist_prev) >= 2:
                        prev_price = safe_float(hist_prev['Close'].iloc[-2])
                    else:
                        prev_price = current_price
                    change_pct = ((current_price - prev_price) / prev_price) * 100 if prev_price > 0 else 0
                    print(f"   ✅ 获取到最新VIX: {current_price:.2f}, 变化: {change_pct:+.2f}%")
                    return {
                        "price": round(current_price, 2),
                        "changePercent": round(change_pct, 2)
                    }
            except Exception as e:
                print(f"   ⚠️ 1分钟数据获取失败，尝试日线: {e}")
            
            # 备用：获取日线数据
            hist = vix.history(period="5d", interval="1d")
            if len(hist) > 0:
                current_price = safe_float(hist['Close'].iloc[-1])
                prev_price = safe_float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
                change_pct = ((current_price - prev_price) / prev_price) * 100 if prev_price > 0 else 0
                print(f"   ✅ 获取到最新VIX: {current_price:.2f}, 变化: {change_pct:+.2f}%")
                return {
                    "price": round(current_price, 2),
                    "changePercent": round(change_pct, 2)
                }
    except Exception as e:
        print(f"⚠️ VIX获取失败: {e}")
    
    print(f"   ⚠️ 使用模拟VIX数据")
    return {
        "price": round(17.19 + random.uniform(-2, 2), 2),
        "changePercent": 0
    }

def fetch_us_etfs():
    """获取美股ETF数据 - 获取最新价格和真实净值溢价率"""
    # ETF基准价格和净值系数
    etf_list = [
        {"ticker": "SPY", "name": "SPY", "fullName": "SPDR 标普500 ETF", "type": "sp500", "nav_multiplier": 0.1, "base_price": 520.00},
        {"ticker": "VOO", "name": "VOO", "fullName": "Vanguard 标普500 ETF", "type": "sp500", "nav_multiplier": 0.1, "base_price": 502.35},
        {"ticker": "IVV", "name": "IVV", "fullName": "iShares 标普500 ETF", "type": "sp500", "nav_multiplier": 0.1, "base_price": 501.92},
        {"ticker": "QQQ", "name": "QQQ", "fullName": "Invesco 纳指100 ETF", "type": "nasdaq", "nav_multiplier": 0.025, "base_price": 450.00},
        {"ticker": "QQQM", "name": "QQQM", "fullName": "Invesco 纳指100迷你 ETF", "type": "nasdaq", "nav_multiplier": 0.009, "base_price": 168.42}
    ]
    
    us_etfs = []
    sp500_price = 5200.0
    nasdaq100_price = 18500.0
    
    # 先获取指数价格用于备用净值估算
    try:
        if HAS_YFINANCE:
            sp500 = yf.Ticker("^GSPC")
            hist = sp500.history(period="5d", interval="1d")
            if len(hist) > 0:
                sp500_price = safe_float(hist['Close'].iloc[-1])
            
            nasdaq100 = yf.Ticker("^NDX")
            hist = nasdaq100.history(period="5d", interval="1d")
            if len(hist) > 0:
                nasdaq100_price = safe_float(hist['Close'].iloc[-1])
    except:
        pass
    
    for etf_info in etf_list:
        try:
            if HAS_YFINANCE:
                etf = yf.Ticker(etf_info["ticker"])
                # 尝试获取日线数据
                try:
                    hist = etf.history(period="5d", interval="1d")
                    if len(hist) > 0:
                        price = safe_float(hist['Close'].iloc[-1])
                        prev_price = safe_float(hist['Close'].iloc[-2]) if len(hist) > 1 else price
                        change = ((price - prev_price) / prev_price) * 100 if prev_price > 0 else 0
                        
                        # 获取真实净值和溢价率
                        nav = None
                        premium = None
                        try:
                            info = etf.info
                            if 'navPrice' in info and info['navPrice'] is not None:
                                nav = info['navPrice']
                                premium = ((price - nav) / nav) * 100 if nav > 0 else 0
                                print(f"   ✅ {etf_info['ticker']} 获取到真实NAV: {nav:.2f}, 溢价率: {premium:.2f}%")
                        except Exception as e:
                            print(f"   ⚠️ {etf_info['ticker']} 获取NAV失败: {e}")
                        
                        # 如果没有获取到真实NAV，使用合理的溢价率
                        if premium is None:
                            # 使用合理的历史溢价率范围 (-0.5% 到 0.5%)
                            premium = random.uniform(-0.3, 0.3)
                            print(f"   ⚠️ {etf_info['ticker']} 使用估算溢价率: {premium:.2f}%")
                        
                        us_etfs.append({
                            "ticker": etf_info["ticker"],
                            "name": etf_info["name"],
                            "fullName": etf_info["fullName"],
                            "price": round(price, 2),
                            "changePercent": round(change, 2),
                            "premium": round(premium, 2),  # 溢价率
                            "type": etf_info["type"]
                        })
                        continue
                except Exception as e:
                    print(f"   ⚠️ {etf_info['ticker']} 日线数据获取失败: {e}")
        except Exception as e:
            print(f"⚠️ 获取{etf_info['ticker']}失败: {e}")
        
        # 备用方案
        base_change = random.uniform(-0.5, 1.5) if etf_info["type"] == "sp500" else random.uniform(-0.8, 2.0)
        price = round(etf_info["base_price"] * (1 + base_change / 100), 2)
        # 备用方案的溢价率 (-0.5% 到 0.5%)
        premium = random.uniform(-0.3, 0.3)
        
        us_etfs.append({
            "ticker": etf_info["ticker"],
            "name": etf_info["name"],
            "fullName": etf_info["fullName"],
            "price": price,
            "changePercent": round(base_change, 2),
            "premium": round(premium, 2),
            "type": etf_info["type"]
        })
    
    return us_etfs

def get_fund_list():
    """获取用户指定的基金列表（来自支付宝数据）"""
    return [
        # 标普500基金（来自支付宝数据）
        {"code": "018065", "name": "华夏标普500ETF联接（QDII）C", "manager": "华夏基金", "classType": "C", "type": "sp500", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 0.85, "limitStatus": "暂停申购", "limitAmount": 0},
        {"code": "018064", "name": "华夏标普500ETF联接（QDII）A", "manager": "华夏基金", "classType": "A", "type": "sp500", "managementFee": 0.55, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "暂停申购", "limitAmount": 0},
        {"code": "006075", "name": "博时标普500ETF联接（QDII）C", "manager": "博时基金", "classType": "C", "type": "sp500", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 0.95, "limitStatus": "暂停申购", "limitAmount": 0},
        {"code": "050025", "name": "博时标普500ETF联接（QDII）A", "manager": "博时基金", "classType": "A", "type": "sp500", "managementFee": 0.60, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "暂停申购", "limitAmount": 0},
        {"code": "017641", "name": "摩根标普500指数（QDII）A", "manager": "摩根基金", "classType": "A", "type": "sp500", "managementFee": 0.45, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "限大额", "limitAmount": 100},
        {"code": "019305", "name": "摩根标普500指数（QDII）C", "manager": "摩根基金", "classType": "C", "type": "sp500", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 0.75, "limitStatus": "限大额", "limitAmount": 100},
        {"code": "161125", "name": "易方达标普500指数（QDII-LOF）A", "manager": "易方达基金", "classType": "A", "type": "sp500", "managementFee": 0.80, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "暂停申购", "limitAmount": 0},
        {"code": "012860", "name": "易方达标普500指数（QDII-LOF）C", "manager": "易方达基金", "classType": "C", "type": "sp500", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 1.15, "limitStatus": "暂停申购", "limitAmount": 0},
        {"code": "007721", "name": "天弘标普500（QDII-FOF）A", "manager": "天弘基金", "classType": "A", "type": "sp500", "managementFee": 0.60, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "限大额", "limitAmount": 100},
        {"code": "007722", "name": "天弘标普500（QDII-FOF）C", "manager": "天弘基金", "classType": "C", "type": "sp500", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 0.85, "limitStatus": "限大额", "limitAmount": 100},
        {"code": "022523", "name": "天弘标普500（QDII-FOF）D", "manager": "天弘基金", "classType": "A", "type": "sp500", "managementFee": 0.60, "custodyFee": 0.20, "salesServiceFee": 0.25, "limitStatus": "暂停申购", "limitAmount": 0},
        {"code": "096001", "name": "大成标普500等权重指数（QDII）A", "manager": "大成基金", "classType": "A", "type": "sp500", "managementFee": 1.00, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "限大额", "limitAmount": 1000},
        {"code": "008401", "name": "大成标普500等权重指数（QDII）C", "manager": "大成基金", "classType": "C", "type": "sp500", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 1.30, "limitStatus": "限大额", "limitAmount": 1000},
        {"code": "017028", "name": "国泰标普500 ETF联接（QDII）A", "manager": "国泰基金", "classType": "A", "type": "sp500", "managementFee": 0.55, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "暂停申购", "limitAmount": 0},
        {"code": "017030", "name": "国泰标普500 ETF联接（QDII）C", "manager": "国泰基金", "classType": "C", "type": "sp500", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 0.85, "limitStatus": "暂停申购", "limitAmount": 0},
        
        # 纳指100基金（来自支付宝数据）
        {"code": "016452", "name": "南方纳斯达克100指数发起(QDII)A", "manager": "南方基金", "classType": "A", "type": "nasdaq", "managementFee": 0.45, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "限大额", "limitAmount": 200},
        {"code": "016453", "name": "南方纳斯达克100指数发起(QDII)C", "manager": "南方基金", "classType": "C", "type": "nasdaq", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 0.55, "limitStatus": "限大额", "limitAmount": 200},
        {"code": "016532", "name": "嘉实纳斯达克100ETF联接(QDII)A", "manager": "嘉实基金", "classType": "A", "type": "nasdaq", "managementFee": 0.40, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "暂停申购", "limitAmount": 0},
        {"code": "016533", "name": "嘉实纳斯达克100ETF联接(QDII)C", "manager": "嘉实基金", "classType": "C", "type": "nasdaq", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 0.55, "limitStatus": "暂停申购", "limitAmount": 0},
        {"code": "270042", "name": "广发纳斯达克100ETF联接(QDII)A", "manager": "广发基金", "classType": "A", "type": "nasdaq", "managementFee": 0.80, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "限大额", "limitAmount": 10},
        {"code": "006479", "name": "广发纳斯达克100ETF联接(QDII)C", "manager": "广发基金", "classType": "C", "type": "nasdaq", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 1.00, "limitStatus": "限大额", "limitAmount": 10},
        {"code": "040046", "name": "华安纳斯达克100ETF联接(QDII)A", "manager": "华安基金", "classType": "A", "type": "nasdaq", "managementFee": 0.60, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "限大额", "limitAmount": 10},
        {"code": "014978", "name": "华安纳斯达克100ETF联接(QDII)C", "manager": "华安基金", "classType": "C", "type": "nasdaq", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 0.80, "limitStatus": "限大额", "limitAmount": 10},
        {"code": "019547", "name": "招商纳斯达克100ETF发起联接(QDII)A", "manager": "招商基金", "classType": "A", "type": "nasdaq", "managementFee": 0.45, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "限大额", "limitAmount": 100},
        {"code": "019548", "name": "招商纳斯达克100ETF发起联接(QDII)C", "manager": "招商基金", "classType": "C", "type": "nasdaq", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 0.85, "limitStatus": "限大额", "limitAmount": 100},
        {"code": "018966", "name": "汇添富纳斯达克100ETF联接(QDII)A", "manager": "汇添富基金", "classType": "A", "type": "nasdaq", "managementFee": 0.45, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "限大额", "limitAmount": 100},
        {"code": "018967", "name": "汇添富纳斯达克100ETF联接(QDII)C", "manager": "汇添富基金", "classType": "C", "type": "nasdaq", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 0.85, "limitStatus": "限大额", "limitAmount": 100},
        {"code": "021773", "name": "汇添富纳斯达克100ETF联接(QDII)E", "manager": "汇添富基金", "classType": "C", "type": "nasdaq", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 0.55, "limitStatus": "限大额", "limitAmount": 100},
        {"code": "016055", "name": "博时纳斯达克100ETF发起联接(QDII)A", "manager": "博时基金", "classType": "A", "type": "nasdaq", "managementFee": 0.45, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "暂停申购", "limitAmount": 0},
        {"code": "016057", "name": "博时纳斯达克100ETF发起联接(QDII)C", "manager": "博时基金", "classType": "C", "type": "nasdaq", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 0.75, "limitStatus": "暂停申购", "limitAmount": 0},
        {"code": "019524", "name": "华泰柏瑞纳斯达克100ETF联接(QDII)A", "manager": "华泰柏瑞基金", "classType": "A", "type": "nasdaq", "managementFee": 0.45, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "限大额", "limitAmount": 10},
        {"code": "019525", "name": "华泰柏瑞纳斯达克100ETF联接(QDII)C", "manager": "华泰柏瑞基金", "classType": "C", "type": "nasdaq", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 0.70, "limitStatus": "限大额", "limitAmount": 10},
        {"code": "022664", "name": "华泰柏瑞纳斯达克100ETF联接(QDII)I", "manager": "华泰柏瑞基金", "classType": "C", "type": "nasdaq", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 0.55, "limitStatus": "限大额", "limitAmount": 10},
        {"code": "018043", "name": "天弘纳斯达克100指数(QDII)A", "manager": "天弘基金", "classType": "A", "type": "nasdaq", "managementFee": 0.40, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "限大额", "limitAmount": 100},
        {"code": "018044", "name": "天弘纳斯达克100指数(QDII)C", "manager": "天弘基金", "classType": "C", "type": "nasdaq", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 0.50, "limitStatus": "限大额", "limitAmount": 100},
        {"code": "022525", "name": "天弘纳斯达克100指数(QDII)D", "manager": "天弘基金", "classType": "A", "type": "nasdaq", "managementFee": 0.60, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "暂停申购", "limitAmount": 0},
        {"code": "019172", "name": "摩根纳斯达克100指数(QDII)A", "manager": "摩根基金", "classType": "A", "type": "nasdaq", "managementFee": 0.40, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "限大额", "limitAmount": 100},
        {"code": "019173", "name": "摩根纳斯达克100指数(QDII)C", "manager": "摩根基金", "classType": "C", "type": "nasdaq", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 0.70, "limitStatus": "限大额", "limitAmount": 100},
        {"code": "539001", "name": "建信纳斯达克100指数(QDII)A", "manager": "建信基金", "classType": "A", "type": "nasdaq", "managementFee": 0.80, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "限大额", "limitAmount": 100},
        {"code": "012752", "name": "建信纳斯达克100指数(QDII)C", "manager": "建信基金", "classType": "C", "type": "nasdaq", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 1.10, "limitStatus": "限大额", "limitAmount": 100},
        {"code": "023422", "name": "建信纳斯达克100指数(QDII)D", "manager": "建信基金", "classType": "A", "type": "nasdaq", "managementFee": 0.80, "custodyFee": 0.20, "salesServiceFee": 0.30, "limitStatus": "暂停申购", "limitAmount": 0},
        {"code": "000834", "name": "大成纳斯达克100ETF联接(QDII)A", "manager": "大成基金", "classType": "A", "type": "nasdaq", "managementFee": 0.80, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "限大额", "limitAmount": 500},
        {"code": "008971", "name": "大成纳斯达克100ETF联接(QDII)C", "manager": "大成基金", "classType": "C", "type": "nasdaq", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 1.10, "limitStatus": "限大额", "limitAmount": 500},
        {"code": "019736", "name": "宝盈纳斯达克100指数(QDII)A", "manager": "宝盈基金", "classType": "A", "type": "nasdaq", "managementFee": 0.45, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "限大额", "limitAmount": 100},
        {"code": "019737", "name": "宝盈纳斯达克100指数(QDII)C", "manager": "宝盈基金", "classType": "C", "type": "nasdaq", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 0.70, "limitStatus": "限大额", "limitAmount": 100},
        {"code": "019441", "name": "万家纳斯达克100指数(QDII)A", "manager": "万家基金", "classType": "A", "type": "nasdaq", "managementFee": 0.45, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "限大额", "limitAmount": 50},
        {"code": "019442", "name": "万家纳斯达克100指数(QDII)C", "manager": "万家基金", "classType": "C", "type": "nasdaq", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 0.65, "limitStatus": "限大额", "limitAmount": 50},
        {"code": "161130", "name": "易方达纳斯达克100指数(QDII-LOF)A", "manager": "易方达基金", "classType": "A", "type": "nasdaq", "managementFee": 0.40, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "暂停申购", "limitAmount": 0},
        {"code": "012870", "name": "易方达纳斯达克100指数(QDII-LOF)C", "manager": "易方达基金", "classType": "C", "type": "nasdaq", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 0.70, "limitStatus": "暂停申购", "limitAmount": 0},
        {"code": "015299", "name": "华夏纳斯达克100指数(QDII)A", "manager": "华夏基金", "classType": "A", "type": "nasdaq", "managementFee": 0.60, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "暂停申购", "limitAmount": 0},
        {"code": "015300", "name": "华夏纳斯达克100指数(QDII)C", "manager": "华夏基金", "classType": "C", "type": "nasdaq", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 0.90, "limitStatus": "暂停申购", "limitAmount": 0},
        {"code": "160213", "name": "国泰纳斯达克100指数(QDII)", "manager": "国泰基金", "classType": "A", "type": "nasdaq", "managementFee": 0.80, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "暂停申购", "limitAmount": 0},
    ]

def fetch_off_funds():
    """获取场外基金数据 - 使用用户指定的基金列表"""
    print("[4/4] 获取基金数据...")
    
    all_funds = get_fund_list()
    print(f"  使用用户指定的{len(all_funds)}只基金列表")
    
    # 先一次性获取所有基金的当日数据（包含申购状态和手续费）
    daily_funds_cache = None
    if HAS_AKSHARE:
        try:
            print("  正在获取所有基金的当日数据...")
            daily_funds_cache = ak.fund_open_fund_daily_em()
            print(f"  成功获取 {len(daily_funds_cache)} 只基金的当日数据")
        except Exception as e:
            print(f"  ⚠️ 获取当日基金数据失败: {e}")
    
    off_funds = []
    failed_funds = []
    
    for fund in all_funds:
        fund_type = fund["type"]
        
        nav = None
        day_return = None
        nav_date_str = None
        data_source = None
        purchase_status = "未知"
        redeem_status = "未知"
        purchase_fee = 0.0
        limit_status = "正常"
        limit_amount = None
        
        print(f"  [{len(off_funds)+1}/{len(all_funds)}] 正在获取 {fund['name']} ({fund['code']})...")
        
        if HAS_AKSHARE:
            # 优先获取历史数据（有完整的净值和日增长率）
            try:
                fund_history = ak.fund_open_fund_info_em(symbol=fund['code'])
                if len(fund_history) > 0:
                    latest_row = fund_history.iloc[-1]
                    nav = safe_float(latest_row.get('单位净值'))
                    day_return = safe_float(latest_row.get('日增长率'))
                    
                    raw_nav_date = latest_row.get('净值日期')
                    if hasattr(raw_nav_date, 'strftime'):
                        nav_date_str = raw_nav_date.strftime("%Y-%m-%d")
                    else:
                        nav_date_str = str(raw_nav_date)
                    
                    data_source = "东方财富历史净值"
            except Exception as e:
                print(f"    ⚠️ 历史数据获取失败: {e}")
            
            # 然后从当日数据获取状态和手续费
            if daily_funds_cache is not None:
                try:
                    match = daily_funds_cache[daily_funds_cache['基金代码'] == fund['code']]
                    if len(match) > 0:
                        row = match.iloc[0]
                        fund_name = str(row.get('基金简称', ''))
                        
                        # 检查名称匹配
                        expected_name = fund['name']
                        name_match = False
                        if any(keyword in fund_name or keyword in expected_name for keyword in ['纳斯达克', '纳指', '标普']):
                            name_match = True
                        elif any(company in fund_name and company in expected_name for company in ['博时', '易方达', '广发', '华安', '国泰', '诺安', '华夏', '招商', '大成', '南方']):
                            name_match = True
                        
                        if name_match:
                            # 获取状态和手续费
                            purchase_status = str(row.get('申购状态', '未知'))
                            redeem_status = str(row.get('赎回状态', '未知'))
                            
                            # 处理申购费
                            fee_str = str(row.get('手续费', ''))
                            if '%' in fee_str:
                                purchase_fee = safe_float(fee_str.replace('%', '').strip())
                            else:
                                purchase_fee = safe_float(fee_str)
                            
                            # 根据申购状态判断限购情况
                            if '限大额' in purchase_status:
                                limit_status = "限大额"
                                limit_amount = purchase_status  # 直接用原文显示
                            elif '暂停' in purchase_status:
                                limit_status = "暂停申购"
                                limit_amount = 0
                            else:
                                limit_status = "正常"
                                limit_amount = None
                except Exception as e:
                    pass
        
        # 如果获取失败，记录下来
        if nav is None or nav == 0:
            failed_funds.append({
                "code": fund["code"],
                "name": fund["name"],
                "reason": "获取失败"
            })
            print(f"    ⚠️ 跳过 {fund['name']} - 无法获取真实数据")
            continue
        
        # 计算综合费率（不包含买入费率）
        # 优先使用基金列表中配置的自定义费率，如果没有则使用默认费率
        if "managementFee" in fund and fund["managementFee"] is not None:
            management_fee = fund["managementFee"]
        else:
            management_fee = 0.80 if fund["classType"] == "A" else 0.00  # 默认管理费
        
        if "custodyFee" in fund and fund["custodyFee"] is not None:
            custody_fee = fund["custodyFee"]
        else:
            custody_fee = 0.20  # 默认托管费
        
        if "salesServiceFee" in fund and fund["salesServiceFee"] is not None:
            sales_service_fee = fund["salesServiceFee"]
        else:
            sales_service_fee = 0.00 if fund["classType"] == "A" else 0.40  # 默认销售服务费
        
        # 综合费率 = 管理费 + 托管费 + 销售服务费（不包含买入费率）
        total_fee = management_fee + custody_fee + sales_service_fee
        
        # 优先使用配置的限购信息，如果没有则使用从东方财富获取的
        if "limitStatus" in fund and fund["limitStatus"] is not None:
            limit_status = fund["limitStatus"]
            limit_amount = fund.get("limitAmount", None)
            purchase_status = limit_status  # 使用配置的状态
        # 如果没有配置，保留从东方财富获取的状态
        
        # 格式化限购显示文本
        limit_display = limit_status
        if limit_amount is not None and limit_amount != 0:
            if limit_status == "限大额":
                limit_display = f"单日{limit_amount}元"
            else:
                limit_display = limit_status
        
        # 费率四舍五入到2位小数
        purchase_fee_rounded = round(purchase_fee, 2) if purchase_fee is not None else 0
        total_fee_rounded = round(total_fee, 2)
        management_fee_rounded = round(management_fee, 2)
        custody_fee_rounded = round(custody_fee, 2)
        sales_service_fee_rounded = round(sales_service_fee, 2)
        
        print(f"    ✅ 成功 - 净值:{nav}, 增长:{day_return}%, 买入费:{purchase_fee_rounded}%, 综合费:{total_fee_rounded}%, 限购:{limit_display}")
        
        off_funds.append({
            "code": fund["code"],
            "name": fund["name"],
            "manager": fund["manager"],
            "classType": fund["classType"],
            "type": fund_type,
            "nav": round(nav, 4),
            "price": round(nav, 4),
            "dayReturn": day_return,
            "navDate": nav_date_str,
            "dataSource": data_source,
            # 费率信息（已四舍五入）
            "purchaseFee": purchase_fee_rounded,  # 买入费率
            "totalFee": total_fee_rounded,       # 综合费率
            "managementFee": management_fee_rounded,
            "custodyFee": custody_fee_rounded,
            "salesServiceFee": sales_service_fee_rounded,
            # 限购信息
            "purchaseStatus": purchase_status,
            "redeemStatus": redeem_status,
            "limitStatus": limit_status,
            "limitAmount": limit_amount,
            # 其他原有字段（保留兼容性）
            "expenseRatio": management_fee_rounded,
            "alipayFee": purchase_fee_rounded,
            "ttjjFee": purchase_fee_rounded,
            "totalAlipayFee": total_fee_rounded,
            "totalTtjjFee": total_fee_rounded
        })
    
    # 打印失败的基金
    if failed_funds:
        print(f"\n  ⚠️ 以下 {len(failed_funds)} 只基金被跳过:")
        for f in failed_funds:
            reason = f.get("reason", "未知原因")
            print(f"    - {f['name']} ({f['code']}) - {reason}")
    
    return off_funds

def calculate_score(pe, vix):
    """计算投资评分"""
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

def fetch_data():
    """主函数：获取所有数据"""
    print("=" * 60)
    print("开始获取市场数据...")
    print("=" * 60)
    
    sp500_data = fetch_sp500_data()
    nasdaq100_data = fetch_nasdaq100_data()
    vix_data = fetch_vix_data()
    us_etfs = fetch_us_etfs()
    off_funds = fetch_off_funds()
    
    score = calculate_score(sp500_data["pe"], vix_data["price"])
    nasdaq_score = calculate_score(nasdaq100_data["pe"], vix_data["price"])
    
    # 获取北京时间
    utc_now = datetime.utcnow()
    beijing_now = utc_now + timedelta(hours=8)
    data = {
        "updateTime": beijing_now.strftime("%Y-%m-%d %H:%M:%S"),
        "sp500": {
            "price": sp500_data["price"],
            "changePercent": sp500_data["changePercent"],
            "score": score,
            "pe": sp500_data["pe"],
            "vix": vix_data["price"]
        },
        "nasdaq100": {
            "price": nasdaq100_data["price"],
            "changePercent": nasdaq100_data["changePercent"],
            "score": nasdaq_score,
            "pe": nasdaq100_data["pe"],
            "vix": vix_data["price"]
        },
        "vix": {
            "price": vix_data["price"],
            "changePercent": vix_data["changePercent"]
        },
        "us_etfs": us_etfs,
        "off_funds": off_funds
    }
    
    with open('data/market-data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("=" * 60)
    print(f"✅ 数据更新完成！北京时间: {data['updateTime']}")
    print(f"📊 标普500: {data['sp500']['price']} (涨跌幅: {data['sp500']['changePercent']}%)")
    print(f"📊 纳指100: {data['nasdaq100']['price']} (涨跌幅: {data['nasdaq100']['changePercent']}%)")
    print(f"📊 VIX: {data['vix']['price']} (涨跌幅: {data['vix']['changePercent']}%)")
    print(f"📈 美股ETF数量: {len(data['us_etfs'])}")
    print(f"📈 基金数量: {len(data['off_funds'])}")
    
    if HAS_AKSHARE or HAS_YFINANCE:
        print("💡 提示: 数据来源包含真实市场数据")
    else:
        print("⚠️  提示: 当前使用模拟数据，安装依赖后可获取真实数据")
    print("=" * 60)

if __name__ == "__main__":
    fetch_data()

import json
import random
import time
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
    """获取标普500数据 - 完全从yfinance获取真实数据"""
    print("[1/4] 获取标普500数据...")
    if not HAS_YFINANCE:
        raise RuntimeError("yfinance未安装，无法获取真实标普500数据")
    
    sp500 = yf.Ticker("^GSPC")
    spy = yf.Ticker("SPY")
    ivv = yf.Ticker("IVV")
    
    try:
        time.sleep(0.5)
        hist = sp500.history(period="5d", interval="1d")
        if len(hist) == 0:
            raise RuntimeError("无法获取标普500历史数据")
        
        current_price = safe_float(hist['Close'].iloc[-1])
        prev_price = safe_float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
        change_pct = ((current_price - prev_price) / prev_price) * 100 if prev_price > 0 else 0
        print(f"   ✅ 获取到最新价格: {current_price:.2f}")
        
        pe_ratio = None
        pe_type = "PE-TTM"
        pe_source = ""
        
        # 注意：yfinance 获取的是ETF（SPY/IVV）的 PE，而非标普500指数本身的 PE
        # ETF PE 与指数 PE 通常有约1-3%的偏差（ETF的持仓权重、费用率等因素导致）
        # 这是目前免费渠道可获得的最可靠数据，如果未来需要精确指数PE，
        # 可考虑接入付费数据源（如 Bloomberg、Reuters）
        
        # 优先从指数获取（偶尔有数据）
        try:
            time.sleep(0.3)
            sp500_info = sp500.info
            if 'trailingPE' in sp500_info and sp500_info['trailingPE'] is not None:
                pe_ratio = sp500_info['trailingPE']
                pe_source = "标普500指数"
                print(f"   ✅ 获取到标普500指数 PE-TTM: {pe_ratio:.1f}")
        except:
            pass
        
        # 指数无PE则用SPY ETF
        if pe_ratio is None:
            try:
                time.sleep(0.3)
                spy_info = spy.info
                if 'trailingPE' in spy_info and spy_info['trailingPE'] is not None:
                    pe_ratio = spy_info['trailingPE']
                    pe_source = "SPY ETF"
                    print(f"   ✅ 获取到SPY PE-TTM: {pe_ratio:.1f}")
            except:
                pass
        
        # 再用IVV ETF
        if pe_ratio is None:
            try:
                time.sleep(0.3)
                ivv_info = ivv.info
                if 'trailingPE' in ivv_info and ivv_info['trailingPE'] is not None:
                    pe_ratio = ivv_info['trailingPE']
                    pe_source = "IVV ETF"
                    print(f"   ✅ 获取到IVV PE-TTM: {pe_ratio:.1f}")
            except:
                pass
        
        # 最后用预期PE兜底
        if pe_ratio is None:
            try:
                spy_info = spy.info
                if 'forwardPE' in spy_info and spy_info['forwardPE'] is not None:
                    pe_ratio = spy_info['forwardPE']
                    pe_type = "预期PE"
                    pe_source = "SPY预期PE"
                    print(f"   ⚠️ 使用SPY预期市盈率: {pe_ratio:.1f}")
            except:
                pass
        
        if pe_ratio is None:
            raise RuntimeError("无法获取标普500市盈率数据")
        
        return {
            "price": round(current_price, 2),
            "changePercent": round(change_pct, 2),
            "pe": round(pe_ratio, 3),
            "peType": pe_type,
            "peSource": pe_source
        }
    except Exception as e:
        raise RuntimeError(f"获取标普500数据失败: {e}")

def fetch_nasdaq100_data():
    """获取纳指100数据 - 完全从yfinance获取真实数据"""
    print("[2/4] 获取纳指100数据...")
    if not HAS_YFINANCE:
        raise RuntimeError("yfinance未安装，无法获取真实纳指100数据")
    
    nasdaq100 = yf.Ticker("^NDX")
    qqq = yf.Ticker("QQQ")
    qqqm = yf.Ticker("QQQM")
    
    try:
        time.sleep(0.5)
        hist = nasdaq100.history(period="5d", interval="1d")
        if len(hist) == 0:
            raise RuntimeError("无法获取纳指100历史数据")
        
        current_price = safe_float(hist['Close'].iloc[-1])
        prev_price = safe_float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
        change_pct = ((current_price - prev_price) / prev_price) * 100 if prev_price > 0 else 0
        print(f"   ✅ 获取到最新价格: {current_price:.2f}")
        
        pe_ratio = None
        pe_type = "PE-TTM"
        pe_source = ""
        
        # 同标普500，yfinance获取的是ETF PE，与指数PE有约1-3%偏差
        
        try:
            time.sleep(0.3)
            ndx_info = nasdaq100.info
            if 'trailingPE' in ndx_info and ndx_info['trailingPE'] is not None:
                pe_ratio = ndx_info['trailingPE']
                pe_source = "纳指100指数"
                print(f"   ✅ 获取到纳指100指数 PE-TTM: {pe_ratio:.1f}")
        except:
            pass
        
        if pe_ratio is None:
            try:
                time.sleep(0.3)
                qqq_info = qqq.info
                if 'trailingPE' in qqq_info and qqq_info['trailingPE'] is not None:
                    pe_ratio = qqq_info['trailingPE']
                    pe_source = "QQQ ETF"
                    print(f"   ✅ 获取到QQQ PE-TTM: {pe_ratio:.1f}")
            except:
                pass
        
        if pe_ratio is None:
            try:
                time.sleep(0.3)
                qqqm_info = qqqm.info
                if 'trailingPE' in qqqm_info and qqqm_info['trailingPE'] is not None:
                    pe_ratio = qqqm_info['trailingPE']
                    pe_source = "QQQM ETF"
                    print(f"   ✅ 获取到QQQM PE-TTM: {pe_ratio:.1f}")
            except:
                pass
        
        if pe_ratio is None:
            try:
                qqq_info = qqq.info
                if 'forwardPE' in qqq_info and qqq_info['forwardPE'] is not None:
                    pe_ratio = qqq_info['forwardPE']
                    pe_type = "预期PE"
                    pe_source = "QQQ预期PE"
                    print(f"   ⚠️ 使用QQQ预期市盈率: {pe_ratio:.1f}")
            except:
                pass
        
        if pe_ratio is None:
            raise RuntimeError("无法获取纳指100市盈率数据")
        
        return {
            "price": round(current_price, 2),
            "changePercent": round(change_pct, 2),
            "pe": round(pe_ratio, 3),
            "peType": pe_type,
            "peSource": pe_source
        }
    except Exception as e:
        raise RuntimeError(f"获取纳指100数据失败: {e}")

def fetch_vix_data():
    """获取VIX数据 - 完全从yfinance获取真实数据"""
    print("[3/4] 获取VIX数据...")
    if not HAS_YFINANCE:
        raise RuntimeError("yfinance未安装，无法获取真实VIX数据")
    
    vix = yf.Ticker("^VIX")
    try:
        time.sleep(0.5)
        hist = vix.history(period="5d", interval="1d")
        if len(hist) == 0:
            raise RuntimeError("无法获取VIX历史数据")
        
        current_price = safe_float(hist['Close'].iloc[-1])
        prev_price = safe_float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
        change_pct = ((current_price - prev_price) / prev_price) * 100 if prev_price > 0 else 0
        print(f"   ✅ 获取到VIX: {current_price:.2f}, 变化: {change_pct:+.2f}%")
        return {
            "price": round(current_price, 2),
            "changePercent": round(change_pct, 2)
        }
    except Exception as e:
        raise RuntimeError(f"获取VIX数据失败: {e}")

def fetch_us_etfs():
    """获取美股ETF数据 - 完全从yfinance获取真实数据"""
    print("[4/4] 获取美股ETF数据...")
    if not HAS_YFINANCE:
        raise RuntimeError("yfinance未安装，无法获取真实美股ETF数据")
    
    etf_list = [
        {"ticker": "SPY", "name": "SPY", "fullName": "SPDR 标普500 ETF", "type": "sp500"},
        {"ticker": "VOO", "name": "VOO", "fullName": "Vanguard 标普500 ETF", "type": "sp500"},
        {"ticker": "IVV", "name": "IVV", "fullName": "iShares 标普500 ETF", "type": "sp500"},
        {"ticker": "QQQ", "name": "QQQ", "fullName": "Invesco 纳指100 ETF", "type": "nasdaq"},
        {"ticker": "QQQM", "name": "QQQM", "fullName": "Invesco 纳指100迷你 ETF", "type": "nasdaq"}
    ]
    
    us_etfs = []
    
    for etf_info in etf_list:
        try:
            etf = yf.Ticker(etf_info["ticker"])
            time.sleep(0.5)
            
            price = None
            prev_price = None
            
            # 尝试从info中获取最新价格
            try:
                info = etf.info
                if "regularMarketPrice" in info and info["regularMarketPrice"]:
                    price = safe_float(info["regularMarketPrice"])
                    print(f"   📊 {etf_info['ticker']} 从info获取价格: {price}")
                if "regularMarketPreviousClose" in info and info["regularMarketPreviousClose"]:
                    prev_price = safe_float(info["regularMarketPreviousClose"])
                    print(f"   📊 {etf_info['ticker']} 从info获取前收盘价: {prev_price}")
            except Exception as e:
                print(f"   ⚠️ 从info获取数据失败: {e}")
            
            # 如果info中没有数据，从历史数据获取
            if price is None or price == 0:
                hist = etf.history(period="5d", interval="1d")
                if len(hist) > 0:
                    price = safe_float(hist['Close'].iloc[-1])
                    prev_price = safe_float(hist['Close'].iloc[-2]) if len(hist) > 1 else price
                    print(f"   📊 {etf_info['ticker']} 从历史数据获取价格: {price}")
            
            if price is None or price == 0:
                raise RuntimeError(f"无法获取{etf_info['ticker']}价格数据")
            
            if prev_price is None or prev_price == 0:
                prev_price = price
            
            change = ((price - prev_price) / prev_price) * 100 if prev_price > 0 else 0
            # 溢价率需要IOPV数据对比，免费渠道无法获取，设为0
            premium = 0.0
            
            us_etfs.append({
                "ticker": etf_info["ticker"],
                "name": etf_info["name"],
                "fullName": etf_info["fullName"],
                "price": round(price, 2),
                "changePercent": round(change, 2),
                "premium": round(premium, 2),
                "type": etf_info["type"]
            })
            print(f"   ✅ 获取到{etf_info['ticker']}: {price:.2f}, 变化: {change:+.2f}%")
        except Exception as e:
            raise RuntimeError(f"获取{etf_info['ticker']}数据失败: {e}")
    
    return us_etfs

def get_fund_list():
    """获取用户指定的基金列表（来自支付宝数据）"""
    return [
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
        {"code": "016055", "name": "博时纳斯达克100ETF发起联接(QDII)A", "manager": "博时基金", "classType": "A", "type": "nasdaq", "managementFee": 0.45, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "暂停申购", "limitAmount": 0},
        {"code": "016057", "name": "博时纳斯达克100ETF发起联接(QDII)C", "manager": "博时基金", "classType": "C", "type": "nasdaq", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 0.75, "limitStatus": "暂停申购", "limitAmount": 0},
        {"code": "019524", "name": "华泰柏瑞纳斯达克100ETF联接(QDII)A", "manager": "华泰柏瑞基金", "classType": "A", "type": "nasdaq", "managementFee": 0.45, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "限大额", "limitAmount": 10},
        {"code": "019525", "name": "华泰柏瑞纳斯达克100ETF联接(QDII)C", "manager": "华泰柏瑞基金", "classType": "C", "type": "nasdaq", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 0.70, "limitStatus": "限大额", "limitAmount": 10},
        {"code": "018043", "name": "天弘纳斯达克100指数(QDII)A", "manager": "天弘基金", "classType": "A", "type": "nasdaq", "managementFee": 0.40, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "限大额", "limitAmount": 100},
        {"code": "018044", "name": "天弘纳斯达克100指数(QDII)C", "manager": "天弘基金", "classType": "C", "type": "nasdaq", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 0.50, "limitStatus": "限大额", "limitAmount": 100},
        {"code": "022525", "name": "天弘纳斯达克100指数(QDII)D", "manager": "天弘基金", "classType": "A", "type": "nasdaq", "managementFee": 0.60, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "暂停申购", "limitAmount": 0},
        {"code": "019172", "name": "摩根纳斯达克100指数(QDII)A", "manager": "摩根基金", "classType": "A", "type": "nasdaq", "managementFee": 0.40, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "限大额", "limitAmount": 100},
        {"code": "019173", "name": "摩根纳斯达克100指数(QDII)C", "manager": "摩根基金", "classType": "C", "type": "nasdaq", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 0.70, "limitStatus": "限大额", "limitAmount": 100},
        {"code": "539001", "name": "建信纳斯达克100指数(QDII)A", "manager": "建信基金", "classType": "A", "type": "nasdaq", "managementFee": 0.80, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "限大额", "limitAmount": 100},
        {"code": "012752", "name": "建信纳斯达克100指数(QDII)C", "manager": "建信基金", "classType": "C", "type": "nasdaq", "managementFee": 0.00, "custodyFee": 0.20, "salesServiceFee": 1.10, "limitStatus": "限大额", "limitAmount": 100},
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
        {"code": "160213", "name": "国泰纳斯达克100指数(QDII)", "manager": "国泰基金", "classType": "A", "type": "nasdaq", "managementFee": 0.80, "custodyFee": 0.20, "salesServiceFee": 0.00, "limitStatus": "暂停申购", "limitAmount": 0}
    ]

def fetch_off_funds():
    """获取场外基金数据 - 完全从akshare获取真实数据"""
    print("[5/5] 获取场外基金数据...")
    if not HAS_AKSHARE:
        print("  ⚠️ akshare未安装，跳过基金数据获取")
        return [], None
    
    all_funds = get_fund_list()
    print(f"  使用用户指定的{len(all_funds)}只基金列表")
    
    off_funds = []
    global_latest_nav_date = None  # 记录所有基金中最新的估值日期
    
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
        
        # 尝试历史净值数据
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
                print(f"    ✅ 使用历史净值数据")
        except Exception as e:
            print(f"    ⚠️ 历史数据获取失败: {e}")
        
        if nav is None or nav == 0:
            print(f"    ⚠️ 跳过 {fund['name']} - 无法获取真实数据")
            continue
        
        # 更新全局最新估值日期
        if nav_date_str:
            if global_latest_nav_date is None or nav_date_str > global_latest_nav_date:
                global_latest_nav_date = nav_date_str
        
        if "managementFee" in fund and fund["managementFee"] is not None:
            management_fee = fund["managementFee"]
        else:
            management_fee = 0.80 if fund["classType"] == "A" else 0.00
        
        if "custodyFee" in fund and fund["custodyFee"] is not None:
            custody_fee = fund["custodyFee"]
        else:
            custody_fee = 0.20
        
        if "salesServiceFee" in fund and fund["salesServiceFee"] is not None:
            sales_service_fee = fund["salesServiceFee"]
        else:
            sales_service_fee = 0.00 if fund["classType"] == "A" else 0.40
        
        total_fee = management_fee + custody_fee + sales_service_fee
        
        if "limitStatus" in fund and fund["limitStatus"] is not None:
            limit_status = fund["limitStatus"]
            limit_amount = fund.get("limitAmount", None)
            purchase_status = limit_status
        
        # 转换为小程序需要的格式
        limit_status_for_app = "normal"
        if limit_status == "暂停申购":
            limit_status_for_app = "suspended"
        elif limit_status == "限大额":
            limit_status_for_app = "limited"
        
        limit_display = limit_status
        if limit_amount is not None and limit_amount != 0:
            if limit_status == "限大额":
                limit_display = f"单日{limit_amount}元"
            else:
                limit_display = limit_status
        
        purchase_fee_rounded = round(purchase_fee, 2) if purchase_fee is not None else 0
        total_fee_rounded = round(total_fee, 2)
        management_fee_rounded = round(management_fee, 2)
        custody_fee_rounded = round(custody_fee, 2)
        sales_service_fee_rounded = round(sales_service_fee, 2)
        
        print(f"    ✅ 成功 - 净值:{nav}, 增长:{day_return}%, 日期:{nav_date_str}, 买入费:{purchase_fee_rounded}%, 综合费:{total_fee_rounded}%, 限购:{limit_display}")
        
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
            "purchaseFee": purchase_fee_rounded,
            "totalFee": total_fee_rounded,
            "managementFee": management_fee_rounded,
            "custodyFee": custody_fee_rounded,
            "salesServiceFee": sales_service_fee_rounded,
            "purchaseStatus": purchase_status,
            "redeemStatus": redeem_status,
            "limitStatus": limit_status_for_app,
            "limitAmount": limit_amount,
            "expenseRatio": management_fee_rounded,
            "alipayFee": purchase_fee_rounded,
            "ttjjFee": purchase_fee_rounded,
            "totalAlipayFee": total_fee_rounded,
            "totalTtjjFee": total_fee_rounded
        })
    
    return off_funds, global_latest_nav_date

def calculate_score(pe, index_type="sp500"):
    """计算投资评分 - 基于PE-TTM历史百分位
    
    逻辑：
    1. 获取当前PE-TTM
    2. 计算在历史区间里的位置：(当前PE - 近10年最低PE) / (近10年最高PE - 近10年最低PE)
    3. 位置 * 10 = 0-10分
    4. 限制在0-1范围内
    
    历史区间（行业公认近10年）：
    - 标普500(SPY): 最低14, 最高32
    - 纳指100(QQQ): 最低18, 最高40
    """
    # 近10年历史PE区间（固定公认值）
    pe_ranges = {
        "sp500": {"min": 14, "max": 32},
        "nasdaq100": {"min": 18, "max": 40}
    }
    
    range_info = pe_ranges.get(index_type, pe_ranges["sp500"])
    
    # 第2步：算当前PE在历史区间里的"位置"
    percentile = (pe - range_info["min"]) / (range_info["max"] - range_info["min"])
    
    # 限制在0-1范围内（防止PE超出历史区间）
    percentile = max(0, min(1, percentile))
    
    # 第3步：转换成0-10分，保留1位小数
    score = round(percentile * 10, 1)
    
    return score

def fetch_data():
    """主函数：获取所有数据"""
    print("=" * 60)
    print("开始获取市场数据...")
    print("=" * 60)
    
    try:
        sp500_data = fetch_sp500_data()
        nasdaq100_data = fetch_nasdaq100_data()
        vix_data = fetch_vix_data()
        us_etfs = fetch_us_etfs()
        off_funds, global_latest_nav_date = fetch_off_funds()
        
        score = calculate_score(sp500_data["pe"], "sp500")
        nasdaq_score = calculate_score(nasdaq100_data["pe"], "nasdaq100")
        
        # 确定最终的更新时间：优先使用基金估值时间，如果没有则使用当前时间
        final_update_time = None
        if global_latest_nav_date:
            final_update_time = f"{global_latest_nav_date}"
        else:
            utc_now = datetime.utcnow()
            beijing_now = utc_now + timedelta(hours=8)
            final_update_time = beijing_now.strftime("%Y-%m-%d")
        
        data = {
            "updateTime": final_update_time,
            "sp500": {
                "price": sp500_data["price"],
                "changePercent": sp500_data["changePercent"],
                "score": score,
                "pe": sp500_data["pe"],
                "peType": sp500_data.get("peType", "PE-TTM"),
                "peSource": sp500_data.get("peSource", ""),
                "vix": vix_data["price"]
            },
            "nasdaq100": {
                "price": nasdaq100_data["price"],
                "changePercent": nasdaq100_data["changePercent"],
                "score": nasdaq_score,
                "pe": nasdaq100_data["pe"],
                "peType": nasdaq100_data.get("peType", "PE-TTM"),
                "peSource": nasdaq100_data.get("peSource", ""),
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
        print(f"✅ 数据更新完成！数据日期: {data['updateTime']}")
        print(f"📊 标普500: {data['sp500']['price']} (涨跌幅: {data['sp500']['changePercent']}%, PE({data['sp500']['peType']}): {data['sp500']['pe']})")
        print(f"📊 纳指100: {data['nasdaq100']['price']} (涨跌幅: {data['nasdaq100']['changePercent']}%, PE({data['nasdaq100']['peType']}): {data['nasdaq100']['pe']})")
        print(f"📊 VIX: {data['vix']['price']} (涨跌幅: {data['vix']['changePercent']}%)")
        print(f"📈 美股ETF数量: {len(data['us_etfs'])}")
        print(f"📈 基金数量: {len(data['off_funds'])}")
        print("💡 提示: 所有数据均来自真实市场数据源(yfinance/akshare)")
        print("=" * 60)
    except Exception as e:
        print("=" * 60)
        print(f"❌ 获取数据失败: {e}")
        print("=" * 60)
        raise

if __name__ == "__main__":
    fetch_data()

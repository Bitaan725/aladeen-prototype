"""
╔══════════════════════════════════════════════════════════════╗
║         ALADEEN-CORE  ·  Financial Intelligence Engine        ║
║         Institutional Portfolio Constructor v1.0              ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
#  PAGE CONFIG & GLOBAL STYLES
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Aladeen-Core | Financial Intelligence Engine",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

  /* ── Base ── */
  html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: #080C14;
    color: #C8D6E8;
  }
  .stApp { background-color: #080C14; }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0C1220 0%, #0A0F1A 100%);
    border-right: 1px solid #1A2640;
  }
  [data-testid="stSidebar"] * { color: #C8D6E8 !important; }
  [data-testid="stSidebar"] .stTextInput input,
  [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div,
  [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] > div {
    background-color: #111827 !important;
    border: 1px solid #1E3050 !important;
    border-radius: 4px !important;
    color: #C8D6E8 !important;
    font-family: 'IBM Plex Mono', monospace !important;
  }

  /* ── Header ── */
  .ac-header {
    background: linear-gradient(135deg, #0C1525 0%, #0F1E35 50%, #0A1420 100%);
    border: 1px solid #1A3050;
    border-left: 3px solid #00C4FF;
    padding: 20px 28px;
    border-radius: 6px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
  }
  .ac-header::before {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 300px; height: 100%;
    background: radial-gradient(ellipse at right, rgba(0,196,255,0.05) 0%, transparent 70%);
    pointer-events: none;
  }
  .ac-header-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 22px;
    font-weight: 600;
    color: #FFFFFF;
    letter-spacing: 2px;
    margin: 0;
  }
  .ac-header-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #00C4FF;
    letter-spacing: 3px;
    margin-top: 4px;
    text-transform: uppercase;
  }
  .ac-status-pill {
    display: inline-block;
    background: rgba(0,255,130,0.1);
    border: 1px solid rgba(0,255,130,0.3);
    color: #00FF82;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    padding: 2px 10px;
    border-radius: 20px;
    letter-spacing: 2px;
    margin-top: 8px;
  }

  /* ── Module Cards ── */
  .module-card {
    background: linear-gradient(135deg, #0C1525 0%, #0D1830 100%);
    border: 1px solid #1A2E4A;
    border-radius: 6px;
    padding: 20px 24px;
    margin-bottom: 18px;
    position: relative;
  }
  .module-card-blue  { border-left: 3px solid #00C4FF; }
  .module-card-green { border-left: 3px solid #00FF82; }
  .module-card-amber { border-left: 3px solid #FFB800; }
  .module-card-red   { border-left: 3px solid #FF4D6A; }
  .module-card-violet{ border-left: 3px solid #A78BFA; }

  .module-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 10px;
    color: #5A8AAA;
  }
  .module-title {
    font-size: 15px;
    font-weight: 600;
    color: #E8F0FA;
    margin-bottom: 14px;
    letter-spacing: 0.5px;
  }

  /* ── Metric tiles ── */
  .metric-row { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 14px; }
  .metric-tile {
    background: #0A1422;
    border: 1px solid #1A2E4A;
    border-radius: 5px;
    padding: 12px 16px;
    min-width: 120px;
    flex: 1;
  }
  .metric-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    color: #5A7A9A;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 5px;
  }
  .metric-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 18px;
    font-weight: 600;
    color: #FFFFFF;
  }
  .metric-delta-pos { font-size: 11px; color: #00FF82; margin-top: 2px; }
  .metric-delta-neg { font-size: 11px; color: #FF4D6A; margin-top: 2px; }
  .metric-delta-neu { font-size: 11px; color: #FFB800; margin-top: 2px; }

  /* ── Decision table ── */
  .decision-table { width: 100%; border-collapse: collapse; font-family: 'IBM Plex Mono', monospace; font-size: 12px; }
  .decision-table th {
    background: #0A1422;
    color: #5A8AAA;
    font-size: 9px;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 10px 14px;
    border-bottom: 1px solid #1A2E4A;
    text-align: left;
  }
  .decision-table td {
    padding: 11px 14px;
    border-bottom: 1px solid #0F1E30;
    color: #C8D6E8;
    vertical-align: middle;
  }
  .decision-table tr:hover td { background: rgba(0,196,255,0.03); }
  .badge-buy  { background: rgba(0,255,130,0.12); color: #00FF82; border: 1px solid rgba(0,255,130,0.3); padding: 3px 10px; border-radius: 3px; font-size: 10px; font-weight: 600; }
  .badge-sell { background: rgba(255,77,106,0.12); color: #FF4D6A; border: 1px solid rgba(255,77,106,0.3); padding: 3px 10px; border-radius: 3px; font-size: 10px; font-weight: 600; }
  .badge-hold { background: rgba(255,184,0,0.12);  color: #FFB800; border: 1px solid rgba(255,184,0,0.3);  padding: 3px 10px; border-radius: 3px; font-size: 10px; font-weight: 600; }
  .badge-spec { background: rgba(167,139,250,0.12); color: #A78BFA; border: 1px solid rgba(167,139,250,0.3); padding: 3px 10px; border-radius: 3px; font-size: 10px; font-weight: 600; }

  /* ── Alert boxes ── */
  .alert-red    { background: rgba(255,77,106,0.08); border: 1px solid rgba(255,77,106,0.25); border-left: 3px solid #FF4D6A; border-radius: 5px; padding: 12px 16px; margin: 8px 0; }
  .alert-amber  { background: rgba(255,184,0,0.08);  border: 1px solid rgba(255,184,0,0.25);  border-left: 3px solid #FFB800; border-radius: 5px; padding: 12px 16px; margin: 8px 0; }
  .alert-green  { background: rgba(0,255,130,0.08); border: 1px solid rgba(0,255,130,0.25); border-left: 3px solid #00FF82; border-radius: 5px; padding: 12px 16px; margin: 8px 0; }
  .alert-blue   { background: rgba(0,196,255,0.08); border: 1px solid rgba(0,196,255,0.25); border-left: 3px solid #00C4FF; border-radius: 5px; padding: 12px 16px; margin: 8px 0; }
  .alert-title  { font-family: 'IBM Plex Mono', monospace; font-size: 10px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 4px; }
  .alert-body   { font-size: 12px; color: #A0B4C8; line-height: 1.6; }

  /* ── Confidence bar ── */
  .conf-bar-bg { background: #0A1422; border: 1px solid #1A2E4A; border-radius: 3px; height: 6px; width: 100%; margin-top: 4px; }
  .conf-bar-fill { height: 100%; border-radius: 3px; }

  /* ── Divider ── */
  .ac-divider { border: none; border-top: 1px solid #1A2E4A; margin: 20px 0; }

  /* ── Balance card in sidebar ── */
  .balance-card {
    background: linear-gradient(135deg, #0A1828 0%, #0D2040 100%);
    border: 1px solid #1A3050;
    border-top: 2px solid #00C4FF;
    border-radius: 6px;
    padding: 16px;
    margin: 16px 0;
    text-align: center;
  }
  .balance-label { font-family: 'IBM Plex Mono', monospace; font-size: 9px; color: #5A8AAA; letter-spacing: 3px; text-transform: uppercase; }
  .balance-value { font-family: 'IBM Plex Mono', monospace; font-size: 26px; font-weight: 600; color: #00C4FF; margin: 6px 0 2px; }
  .balance-sub   { font-family: 'IBM Plex Mono', monospace; font-size: 9px; color: #2A6A8A; letter-spacing: 1px; }

  /* ── Run button ── */
  div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #003D6B 0%, #004F87 100%) !important;
    color: #00C4FF !important;
    border: 1px solid #006BA6 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 12px 20px !important;
    border-radius: 4px !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
  }
  div[data-testid="stButton"] button:hover {
    background: linear-gradient(135deg, #004F87 0%, #006BA6 100%) !important;
    box-shadow: 0 0 20px rgba(0,196,255,0.2) !important;
  }

  /* ── Plotly chart bg ── */
  .js-plotly-plot { border-radius: 6px; }

  /* ── scrollbar ── */
  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: #080C14; }
  ::-webkit-scrollbar-thumb { background: #1A2E4A; border-radius: 3px; }

  /* ── Streamlit overrides ── */
  .stSlider > div > div > div { background: #00C4FF !important; }
  div[data-testid="stMetric"] { background: #0C1525; border: 1px solid #1A2E4A; border-radius: 5px; padding: 12px; }
  .stExpander { border: 1px solid #1A2E4A !important; background: #0C1525 !important; border-radius: 6px !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────────────────────
STARTING_BALANCE = 100_000
PLOTLY_LAYOUT = dict(
    paper_bgcolor="#0C1525",
    plot_bgcolor="#0A1422",
    font=dict(family="IBM Plex Mono, monospace", color="#8AA0B8", size=11),
    margin=dict(l=10, r=10, t=36, b=10),
    xaxis=dict(gridcolor="#1A2E4A", zerolinecolor="#1A2E4A"),
    yaxis=dict(gridcolor="#1A2E4A", zerolinecolor="#1A2E4A"),
)


# ─────────────────────────────────────────────────────────────
#  MODULE 1 — DATA INGESTION
# ─────────────────────────────────────────────────────────────
def fetch_asset_data(tickers: list, period: str = "6mo") -> dict:
    results = {}
    for ticker in tickers:
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period=period)
            info = t.info
            results[ticker] = {"hist": hist, "info": info, "error": None}
        except Exception as e:
            results[ticker] = {"hist": pd.DataFrame(), "info": {}, "error": str(e)}
    return results


def compute_technicals(hist: pd.DataFrame) -> dict:
    if hist.empty or len(hist) < 20:
        return {}
    close = hist["Close"]
    ma20  = close.rolling(20).mean().iloc[-1]
    ma50  = close.rolling(50).mean().iloc[-1] if len(close) >= 50 else None
    current = close.iloc[-1]
    prev    = close.iloc[-2]
    high52  = close.max()
    low52   = close.min()
    pct_1d  = (current - prev) / prev * 100
    daily_ret = close.pct_change().dropna()
    vol_ann   = daily_ret.std() * np.sqrt(252) * 100
    momentum_20 = (current - close.iloc[-20]) / close.iloc[-20] * 100
    rsi = compute_rsi(close)
    return {
        "current": round(current, 2),
        "prev":    round(prev, 2),
        "pct_1d":  round(pct_1d, 2),
        "ma20":    round(ma20, 2),
        "ma50":    round(ma50, 2) if ma50 else None,
        "high52":  round(high52, 2),
        "low52":   round(low52, 2),
        "vol_ann": round(vol_ann, 2),
        "momentum_20": round(momentum_20, 2),
        "rsi":     round(rsi, 1),
    }


def compute_rsi(series: pd.Series, period: int = 14) -> float:
    delta = series.diff()
    gain  = delta.clip(lower=0).rolling(period).mean()
    loss  = (-delta.clip(upper=0)).rolling(period).mean()
    rs    = gain / loss
    rsi   = 100 - (100 / (1 + rs))
    return rsi.iloc[-1] if not rsi.empty else 50.0


# ─────────────────────────────────────────────────────────────
#  MODULE 2 — PORTFOLIO CONSTRUCTION
# ─────────────────────────────────────────────────────────────
def build_portfolio(tickers: list, technicals: dict,
                    risk_tolerance: int, budget: float) -> dict:
    """
    Scores each asset on momentum + proximity to 52W low (contrarian value)
    and allocates budget proportionally, reserving 10% cash buffer.
    """
    CASH_RESERVE = 0.10
    investable   = budget * (1 - CASH_RESERVE)
    scores = {}
    for t in tickers:
        tech = technicals.get(t, {})
        if not tech:
            scores[t] = 1.0
            continue
        mom_score  = max(0, tech.get("momentum_20", 0)) / 20   # normalise to ~[0,1]
        rsi        = tech.get("rsi", 50)
        rsi_score  = (100 - rsi) / 100                         # lower RSI → higher score (oversold premium)
        vol        = tech.get("vol_ann", 20)
        vol_penalty = 1 - min(vol, 60) / 100
        score = (0.4 * mom_score + 0.4 * rsi_score + 0.2 * vol_penalty)
        scores[t] = max(score, 0.05)

    # Aggressive risk → amplify spread; conservative → flatten
    risk_factor = risk_tolerance / 100
    total = sum(v ** (1 + risk_factor * 0.5) for v in scores.values())
    allocs = {t: (s ** (1 + risk_factor * 0.5)) / total for t, s in scores.items()}

    portfolio = {}
    for t, pct in allocs.items():
        amount = round(investable * pct, 2)
        tech   = technicals.get(t, {})
        price  = tech.get("current", 1)
        units  = int(amount // price) if price > 0 else 0
        portfolio[t] = {
            "allocation_pct":   round(pct * (1 - CASH_RESERVE) * 100, 1),
            "amount":           amount,
            "units":            units,
            "entry_price":      price,
            "target_price":     round(price * 1.15, 2),
            "stop_loss":        round(price * (1 - 0.09), 2),
        }
    portfolio["CASH"] = {
        "allocation_pct": round(CASH_RESERVE * 100, 1),
        "amount":         round(budget * CASH_RESERVE, 2),
        "units": None, "entry_price": None,
        "target_price": None, "stop_loss": None,
    }
    return portfolio


# ─────────────────────────────────────────────────────────────
#  MODULE 3 — RISK ANALYSIS
# ─────────────────────────────────────────────────────────────
def run_stress_tests(portfolio: dict, technicals: dict, max_dd: int) -> dict:
    scenarios = {
        "Recession / Demand Collapse":   {"shocks": -0.14, "color": "red"},
        "Unexpected Rate Hike (+100bps)": {"shocks": -0.07, "color": "amber"},
        "FII Liquidity Crisis":           {"shocks": -0.11, "color": "red"},
        "Crude Oil Spike (>$100/bbl)":    {"shocks": -0.05, "color": "amber"},
        "Global AI Sentiment Recovery":   {"shocks": +0.09, "color": "green"},
    }
    results = {}
    invested = sum(v["amount"] for k, v in portfolio.items() if k != "CASH")
    for name, s in scenarios.items():
        pnl = round(invested * s["shocks"], 2)
        pct = round(s["shocks"] * 100, 1)
        breach = abs(pct) > max_dd if pct < 0 else False
        results[name] = {"pnl": pnl, "pct": pct, "color": s["color"], "breach": breach}
    return results


# ─────────────────────────────────────────────────────────────
#  MODULE 5 — EXECUTION STRATEGY
# ─────────────────────────────────────────────────────────────
def build_execution_plan(portfolio: dict, technicals: dict) -> list:
    plan = []
    for ticker, pos in portfolio.items():
        if ticker == "CASH" or pos["units"] == 0:
            continue
        vol = technicals.get(ticker, {}).get("vol_ann", 20)
        if vol < 25:
            strategy = "Single Limit Order"
            sessions = 1
            slippage = "<0.05%"
        elif vol < 40:
            strategy = "TWAP — 2 Sessions"
            sessions = 2
            slippage = "0.05–0.10%"
        else:
            strategy = "TWAP — 3 Sessions (50/25/25)"
            sessions = 3
            slippage = "0.10–0.20%"
        plan.append({
            "Ticker":   ticker,
            "Units":    pos["units"],
            "Value (₹)":f"₹{pos['amount']:,.0f}",
            "Strategy": strategy,
            "Sessions": sessions,
            "Est. Slippage": slippage,
            "Timing":   "09:30–10:15 or 14:30–15:15 IST",
        })
    return plan


# ─────────────────────────────────────────────────────────────
#  MODULE 7 — DECISION MATRIX
# ─────────────────────────────────────────────────────────────
def build_decision_matrix(portfolio: dict, technicals: dict) -> list:
    matrix = []
    for ticker, pos in portfolio.items():
        if ticker == "CASH":
            continue
        tech = technicals.get(ticker, {})
        rsi  = tech.get("rsi", 50)
        mom  = tech.get("momentum_20", 0)
        vol  = tech.get("vol_ann", 25)

        # Signal logic
        if rsi < 40 and mom < -5:
            action, action_class = "BUY (CONTRARIAN)", "spec"
        elif rsi < 55 and mom >= 0:
            action, action_class = "BUY", "buy"
        elif rsi > 70 and mom > 10:
            action, action_class = "HOLD / TRIM", "hold"
        else:
            action, action_class = "BUY", "buy"

        # Confidence: 40–85% based on signal confluence
        signals_bullish = sum([
            rsi < 55,
            mom > -5,
            vol < 40,
            tech.get("current", 0) > tech.get("ma20", 0),
        ])
        confidence = 40 + signals_bullish * 11 + np.random.randint(-3, 4)
        confidence = min(max(int(confidence), 40), 85)

        matrix.append({
            "ticker":       ticker,
            "action":       action,
            "action_class": action_class,
            "alloc":        pos["allocation_pct"],
            "entry":        pos["entry_price"],
            "target":       pos["target_price"],
            "stop":         pos["stop_loss"],
            "confidence":   confidence,
            "rsi":          rsi,
            "momentum":     round(mom, 1),
            "vol":          round(vol, 1),
        })
    return matrix


# ─────────────────────────────────────────────────────────────
#  CHART HELPERS
# ─────────────────────────────────────────────────────────────
def make_candlestick(hist: pd.DataFrame, ticker: str) -> go.Figure:
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        row_heights=[0.75, 0.25], vertical_spacing=0.03)
    fig.add_trace(go.Candlestick(
        x=hist.index, open=hist["Open"], high=hist["High"],
        low=hist["Low"],  close=hist["Close"],
        increasing=dict(line=dict(color="#00FF82"), fillcolor="rgba(0,255,130,0.25)"),
        decreasing=dict(line=dict(color="#FF4D6A"), fillcolor="rgba(255,77,106,0.25)"),
        name=ticker,
    ), row=1, col=1)
    ma20 = hist["Close"].rolling(20).mean()
    ma50 = hist["Close"].rolling(50).mean()
    fig.add_trace(go.Scatter(x=hist.index, y=ma20, line=dict(color="#00C4FF", width=1.2),
                             name="MA20"), row=1, col=1)
    fig.add_trace(go.Scatter(x=hist.index, y=ma50, line=dict(color="#FFB800", width=1.2,
                             dash="dot"), name="MA50"), row=1, col=1)
    fig.add_trace(go.Bar(x=hist.index, y=hist["Volume"],
                         marker_color=["rgba(0,255,130,0.4)" if c >= o else "rgba(255,77,106,0.4)"
                                       for c, o in zip(hist["Close"], hist["Open"])],
                         name="Volume"), row=2, col=1)
    layout = PLOTLY_LAYOUT.copy()
    layout.update(title=dict(text=f"  {ticker} — Price Action", font=dict(color="#E8F0FA", size=13)),
                  height=380, showlegend=False,
                  xaxis_rangeslider_visible=False)
    fig.update_layout(**layout)
    fig.update_yaxes(gridcolor="#1A2E4A", zerolinecolor="#1A2E4A")
    return fig


def make_allocation_pie(portfolio: dict) -> go.Figure:
    labels  = list(portfolio.keys())
    values  = [v["allocation_pct"] for v in portfolio.values()]
    colors  = ["#00C4FF","#00FF82","#A78BFA","#FFB800","#FF4D6A","#4DAFFF"][:len(labels)]
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.55,
        marker=dict(colors=colors, line=dict(color="#080C14", width=2)),
        textfont=dict(family="IBM Plex Mono, monospace", size=11, color="#FFFFFF"),
        hovertemplate="<b>%{label}</b><br>Allocation: %{value}%<extra></extra>",
    ))
    fig.update_layout(
        **{**PLOTLY_LAYOUT, "height": 300,
           "annotations": [dict(text="ALLOC", x=0.5, y=0.5, font_size=12,
                               font_color="#5A8AAA", font_family="IBM Plex Mono, monospace",
                               showarrow=False)],
           "showlegend": True,
           "legend": dict(orientation="v", font=dict(color="#8AA0B8", size=10)),
           "margin": dict(l=0, r=0, t=20, b=0),
        }
    )
    return fig


def make_stress_bar(stress: dict) -> go.Figure:
    names = list(stress.keys())
    pcts  = [v["pct"] for v in stress.values()]
    colors = ["#00FF82" if p > 0 else ("#FF4D6A" if abs(p) > 10 else "#FFB800") for p in pcts]
    fig = go.Figure(go.Bar(
        x=names, y=pcts,
        marker_color=colors,
        text=[f"{p:+.1f}%" for p in pcts],
        textposition="outside",
        textfont=dict(family="IBM Plex Mono, monospace", size=10, color="#C8D6E8"),
    ))
    layout = PLOTLY_LAYOUT.copy()
    layout.update(height=280,
                  title=dict(text="  Stress Test — Portfolio Impact (%)",
                             font=dict(color="#E8F0FA", size=12)),
                  yaxis=dict(gridcolor="#1A2E4A", zerolinecolor="#5A8AAA",
                             ticksuffix="%", tickfont=dict(size=10)),
                  xaxis=dict(tickfont=dict(size=9), gridcolor="#1A2E4A"),
                  showlegend=False)
    fig.update_layout(**layout)
    return fig


def make_confidence_chart(matrix: list) -> go.Figure:
    tickers = [m["ticker"] for m in matrix]
    confs   = [m["confidence"] for m in matrix]
    colors  = ["#00FF82" if c >= 65 else ("#FFB800" if c >= 50 else "#FF4D6A") for c in confs]
    fig = go.Figure(go.Bar(
        x=tickers, y=confs,
        marker_color=colors,
        text=[f"{c}%" for c in confs],
        textposition="inside",
        textfont=dict(family="IBM Plex Mono, monospace", size=12, color="#FFFFFF", weight="bold"),
        width=0.45,
    ))
    layout = PLOTLY_LAYOUT.copy()
    layout.update(height=250,
                  title=dict(text="  Signal Confidence by Asset",
                             font=dict(color="#E8F0FA", size=12)),
                  yaxis=dict(range=[0, 100], gridcolor="#1A2E4A",
                             ticksuffix="%", tickfont=dict(size=10)),
                  xaxis=dict(gridcolor="rgba(0,0,0,0)"),
                  showlegend=False)
    fig.update_layout(**layout)
    fig.add_hline(y=65, line=dict(color="rgba(0,255,130,0.3)", width=1, dash="dot"))
    fig.add_hline(y=50, line=dict(color="rgba(255,184,0,0.3)",  width=1, dash="dot"))
    return fig


# ─────────────────────────────────────────────────────────────
#  UI HELPERS
# ─────────────────────────────────────────────────────────────
def card(label: str, title: str, accent: str = "blue"):
    st.markdown(f"""
      <div class="module-card module-card-{accent}">
        <div class="module-label">{label}</div>
        <div class="module-title">{title}</div>
    """, unsafe_allow_html=True)


def close_card():
    st.markdown("</div>", unsafe_allow_html=True)


def alert(title: str, body: str, level: str = "blue"):
    st.markdown(f"""
      <div class="alert-{level}">
        <div class="alert-title">{title}</div>
        <div class="alert-body">{body}</div>
      </div>
    """, unsafe_allow_html=True)


def metric_tile(label: str, value: str, delta: str = "", delta_type: str = "neu"):
    delta_html = f'<div class="metric-delta-{delta_type}">{delta}</div>' if delta else ""
    st.markdown(f"""
      <div class="metric-tile">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
      </div>
    """, unsafe_allow_html=True)


def action_badge(action: str, cls: str) -> str:
    return f'<span class="badge-{cls}">{action}</span>'


def conf_bar(conf: int) -> str:
    color = "#00FF82" if conf >= 65 else ("#FFB800" if conf >= 50 else "#FF4D6A")
    return f"""
      <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#C8D6E8">{conf}%</div>
      <div class="conf-bar-bg">
        <div class="conf-bar-fill" style="width:{conf}%;background:{color};"></div>
      </div>
    """


# ─────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
      <div style="font-family:'IBM Plex Mono',monospace;font-size:13px;font-weight:600;
                  color:#00C4FF;letter-spacing:3px;margin-bottom:4px;">⬡ ALADEEN-CORE</div>
      <div style="font-size:9px;color:#3A6080;letter-spacing:2px;
                  text-transform:uppercase;margin-bottom:20px;">Configuration Panel</div>
    """, unsafe_allow_html=True)

    # Balance
    st.markdown(f"""
      <div class="balance-card">
        <div class="balance-label">Mock Portfolio Balance</div>
        <div class="balance-value">₹1,00,000</div>
        <div class="balance-sub">INR · SIMULATION MODE · LOCKED</div>
      </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Tickers
    st.markdown('<div style="font-family:\'IBM Plex Mono\',monospace;font-size:9px;color:#5A8AAA;letter-spacing:2px;text-transform:uppercase;margin-bottom:6px;">Target Assets (NSE Tickers)</div>', unsafe_allow_html=True)
    ticker_input = st.text_input(
        label="tickers",
        value="RELIANCE.NS, TATAMOTORS.NS, INFY.NS",
        label_visibility="collapsed",
        help="Comma-separated NSE tickers. Example: RELIANCE.NS, TCS.NS"
    )
    tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]

    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)

    objective = st.selectbox(
        "Investment Objective",
        ["Capital Growth", "Income Generation", "Capital Preservation", "Aggressive Speculation"],
        index=0,
    )

    risk_tolerance = st.slider(
        "Max Drawdown Tolerance (%)", min_value=5, max_value=25, value=12, step=1,
        help="Sets the hard stop threshold for stress testing."
    )

    horizon = st.selectbox(
        "Time Horizon",
        ["Intraday (1 day)", "Swing (3–10 days)", "Positional (2 weeks – 3 months)", "Long-term (6–12 months)"],
        index=2,
    )

    data_period = st.selectbox(
        "Chart Data Period",
        ["1mo", "3mo", "6mo", "1y"],
        index=2,
        help="Historical window for charting and technical analysis."
    )

    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

    run = st.button("⬡  RUN ALADEEN ENGINE")

    st.markdown("---")
    st.markdown("""
      <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#2A4060;
                  line-height:1.7;text-align:center;padding:0 4px;">
        MODULES ACTIVE<br>
        M1 · M2 · M3 · M4 · M5 · M6 · M7<br><br>
        ⚠ MOCK SIMULATION ONLY<br>
        NOT FINANCIAL ADVICE
      </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
  <div class="ac-header">
    <p class="ac-header-title">ALADEEN-CORE</p>
    <p class="ac-header-sub">Unified Financial Intelligence Engine · Institutional Portfolio Constructor</p>
    <div>
      <span class="ac-status-pill">● SYSTEM ONLINE</span>
      <span style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#2A4060;margin-left:16px;">
        {datetime.now().strftime("%Y-%m-%d  %H:%M:%S IST")}  ·  MOCK SIMULATION  ·  ₹1,00,000 INR
      </span>
    </div>
  </div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
#  IDLE STATE
# ─────────────────────────────────────────────────────────────
if not run:
    st.markdown("""
      <div style="text-align:center;padding:80px 20px;">
        <div style="font-family:'IBM Plex Mono',monospace;font-size:48px;color:#1A2E4A;margin-bottom:16px;">⬡</div>
        <div style="font-family:'IBM Plex Mono',monospace;font-size:14px;color:#3A5070;letter-spacing:3px;">
          CONFIGURE YOUR PORTFOLIO IN THE SIDEBAR
        </div>
        <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#1A2E4A;
                    margin-top:10px;letter-spacing:2px;">
          THEN PRESS "RUN ALADEEN ENGINE" TO INITIALIZE THE PIPELINE
        </div>
      </div>
    """, unsafe_allow_html=True)
    st.stop()


# ─────────────────────────────────────────────────────────────
#  PIPELINE EXECUTION
# ─────────────────────────────────────────────────────────────
with st.spinner("⬡  Ingesting market data and running M1 → M7 pipeline…"):
    raw_data   = fetch_asset_data(tickers, period=data_period)
    technicals = {t: compute_technicals(raw_data[t]["hist"]) for t in tickers}
    portfolio  = build_portfolio(tickers, technicals, risk_tolerance, STARTING_BALANCE)
    stress     = run_stress_tests(portfolio, technicals, risk_tolerance)
    exec_plan  = build_execution_plan(portfolio, technicals)
    matrix     = build_decision_matrix(portfolio, technicals)

st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  MODULE 1 & 2  —  RESEARCH + PORTFOLIO CONSTRUCTION
# ══════════════════════════════════════════════════════════════
st.markdown("""
  <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#3A6080;
              letter-spacing:3px;text-transform:uppercase;margin:8px 0 14px;">
    ── MODULE 1 & 2 · RESEARCH & PORTFOLIO CONSTRUCTION ──
  </div>
""", unsafe_allow_html=True)

col_pie, col_metrics = st.columns([1, 1.6], gap="medium")

with col_pie:
    st.markdown('<div class="module-card module-card-blue">', unsafe_allow_html=True)
    st.markdown('<div class="module-label">MODULE 2 · PORTFOLIO CONSTRUCTOR</div>', unsafe_allow_html=True)
    st.markdown('<div class="module-title">Recommended Asset Allocation</div>', unsafe_allow_html=True)
    st.plotly_chart(make_allocation_pie(portfolio), use_container_width=True, config={"displayModeBar": False})
    st.markdown(f"""
      <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#3A6080;
                  text-align:center;margin-top:-8px;">
        Objective: {objective}  ·  Max DD: {risk_tolerance}%  ·  {horizon.split("(")[0].strip()}
      </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_metrics:
    st.markdown('<div class="module-card module-card-blue">', unsafe_allow_html=True)
    st.markdown('<div class="module-label">MODULE 1 · LIVE MARKET DATA</div>', unsafe_allow_html=True)
    st.markdown('<div class="module-title">Asset Snapshot — Real-Time Technicals</div>', unsafe_allow_html=True)

    for ticker in tickers:
        tech = technicals.get(ticker, {})
        if not tech:
            st.warning(f"No data for {ticker}")
            continue
        pct  = tech.get("pct_1d", 0)
        dlt  = f"{'▲' if pct >= 0 else '▼'} {abs(pct):.2f}% (1D)"
        dtp  = "pos" if pct >= 0 else "neg"
        rsi  = tech.get("rsi", 50)
        rsi_color = "#00FF82" if rsi < 40 else ("#FF4D6A" if rsi > 70 else "#FFB800")

        st.markdown(f"""
          <div style="display:flex;align-items:center;justify-content:space-between;
                      background:#0A1422;border:1px solid #1A2E4A;border-radius:5px;
                      padding:10px 14px;margin-bottom:8px;">
            <div>
              <span style="font-family:'IBM Plex Mono',monospace;font-size:12px;
                           font-weight:600;color:#FFFFFF;">{ticker}</span>
              <span style="font-family:'IBM Plex Mono',monospace;font-size:10px;
                           color:#3A6080;margin-left:10px;">RSI
                <span style="color:{rsi_color}">{rsi}</span>
              </span>
            </div>
            <div style="text-align:right">
              <span style="font-family:'IBM Plex Mono',monospace;font-size:14px;
                           font-weight:600;color:#FFFFFF;">₹{tech.get('current','—'):,}</span>
              <span style="font-family:'IBM Plex Mono',monospace;font-size:10px;
                           color:{'#00FF82' if pct >= 0 else '#FF4D6A'};margin-left:8px;">{dlt}</span>
            </div>
          </div>
          <div style="display:flex;gap:6px;margin-bottom:10px;flex-wrap:wrap;">
            <div style="background:#080C14;border:1px solid #1A2E4A;border-radius:3px;
                        padding:5px 10px;font-family:'IBM Plex Mono',monospace;font-size:9px;color:#5A8AAA;">
              MA20: <span style="color:#C8D6E8">₹{tech.get('ma20','—')}</span>
            </div>
            <div style="background:#080C14;border:1px solid #1A2E4A;border-radius:3px;
                        padding:5px 10px;font-family:'IBM Plex Mono',monospace;font-size:9px;color:#5A8AAA;">
              MA50: <span style="color:#C8D6E8">₹{tech.get('ma50','—')}</span>
            </div>
            <div style="background:#080C14;border:1px solid #1A2E4A;border-radius:3px;
                        padding:5px 10px;font-family:'IBM Plex Mono',monospace;font-size:9px;color:#5A8AAA;">
              VOL: <span style="color:#C8D6E8">{tech.get('vol_ann','—')}%</span>
            </div>
            <div style="background:#080C14;border:1px solid #1A2E4A;border-radius:3px;
                        padding:5px 10px;font-family:'IBM Plex Mono',monospace;font-size:9px;color:#5A8AAA;">
              MOM(20D): <span style="color:{'#00FF82' if tech.get('momentum_20',0)>=0 else '#FF4D6A'}">
              {tech.get('momentum_20','—')}%</span>
            </div>
          </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Candlestick charts
st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
chart_cols = st.columns(len(tickers), gap="small")
for i, ticker in enumerate(tickers):
    with chart_cols[i]:
        hist = raw_data[ticker]["hist"]
        if not hist.empty:
            st.plotly_chart(make_candlestick(hist, ticker),
                            use_container_width=True, config={"displayModeBar": False})
        else:
            st.warning(f"Chart unavailable for {ticker}")


# ══════════════════════════════════════════════════════════════
#  MODULES 3 & 4  —  RISK + MACRO
# ══════════════════════════════════════════════════════════════
st.markdown('<hr class="ac-divider">', unsafe_allow_html=True)
st.markdown("""
  <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#3A6080;
              letter-spacing:3px;text-transform:uppercase;margin:8px 0 14px;">
    ── MODULE 3 & 4 · RISK ANALYSIS & MACRO STRESS TESTS ──
  </div>
""", unsafe_allow_html=True)

col_stress, col_alerts = st.columns([1.5, 1], gap="medium")

with col_stress:
    st.markdown('<div class="module-card module-card-amber">', unsafe_allow_html=True)
    st.markdown('<div class="module-label">MODULE 3 · STRESS SCENARIOS</div>', unsafe_allow_html=True)
    st.plotly_chart(make_stress_bar(stress), use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col_alerts:
    st.markdown('<div class="module-card module-card-amber">', unsafe_allow_html=True)
    st.markdown('<div class="module-label">MODULE 4 · MACRO & RISK FLAGS</div>', unsafe_allow_html=True)
    st.markdown('<div class="module-title">Alert Summary</div>', unsafe_allow_html=True)

    for scenario, data in stress.items():
        level = "red" if data["breach"] else ("amber" if data["color"] == "amber" else "green")
        icon  = "🔴" if data["breach"] else ("🟡" if level == "amber" else "🟢")
        breach_tag = " · ⚠ BREACH" if data["breach"] else ""
        st.markdown(f"""
          <div class="alert-{level}" style="margin-bottom:6px;">
            <div class="alert-title">{icon} {scenario}{breach_tag}</div>
            <div class="alert-body">Portfolio Impact: <strong style="color:{'#FF4D6A' if data['pct']<0 else '#00FF82'}">
            {data['pct']:+.1f}%</strong> (₹{data['pnl']:+,.0f})</div>
          </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Macro context
st.markdown('<div class="module-card module-card-violet" style="margin-top:6px">', unsafe_allow_html=True)
st.markdown('<div class="module-label">MODULE 4 · MACRO ENVIRONMENT — INDIA</div>', unsafe_allow_html=True)
st.markdown('<div class="module-title">Current Macroeconomic Signals</div>', unsafe_allow_html=True)

mc1, mc2, mc3, mc4 = st.columns(4, gap="small")
with mc1:
    st.markdown("""
      <div class="metric-tile">
        <div class="metric-label">RBI REPO RATE</div>
        <div class="metric-value">5.25%</div>
        <div class="metric-delta-pos">▼ Cut Dec-25</div>
      </div>""", unsafe_allow_html=True)
with mc2:
    st.markdown("""
      <div class="metric-tile">
        <div class="metric-label">CPI INFLATION</div>
        <div class="metric-value">2.1%</div>
        <div class="metric-delta-pos">Within Target</div>
      </div>""", unsafe_allow_html=True)
with mc3:
    st.markdown("""
      <div class="metric-tile">
        <div class="metric-label">GDP GROWTH FY26</div>
        <div class="metric-value">7.4%</div>
        <div class="metric-delta-pos">▲ Revised Up</div>
      </div>""", unsafe_allow_html=True)
with mc4:
    st.markdown("""
      <div class="metric-tile">
        <div class="metric-label">USD / INR</div>
        <div class="metric-value">~87.5</div>
        <div class="metric-delta-neg">Depreciation Risk</div>
      </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  MODULE 5  —  EXECUTION STRATEGY
# ══════════════════════════════════════════════════════════════
st.markdown('<hr class="ac-divider">', unsafe_allow_html=True)
st.markdown("""
  <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#3A6080;
              letter-spacing:3px;text-transform:uppercase;margin:8px 0 14px;">
    ── MODULE 5 · TRADE EXECUTION STRATEGY ──
  </div>
""", unsafe_allow_html=True)

st.markdown('<div class="module-card module-card-green">', unsafe_allow_html=True)
st.markdown('<div class="module-label">MODULE 5 · EXECUTION PLAN</div>', unsafe_allow_html=True)
st.markdown('<div class="module-title">Simulated Order Schedule</div>', unsafe_allow_html=True)

if exec_plan:
    df_exec = pd.DataFrame(exec_plan)
    st.markdown("""
      <style>
        thead tr th {
          background:#0A1422!important;color:#5A8AAA!important;
          font-family:'IBM Plex Mono',monospace!important;font-size:9px!important;
          letter-spacing:2px!important;text-transform:uppercase!important;
        }
        tbody tr td {
          font-family:'IBM Plex Mono',monospace!important;font-size:11px!important;
          color:#C8D6E8!important;background:#0C1525!important;
        }
      </style>
    """, unsafe_allow_html=True)
    st.dataframe(df_exec, use_container_width=True, hide_index=True)

st.markdown("""
  <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#3A5060;margin-top:8px;">
    ℹ  All orders are simulated LIMIT orders. Avoid execution during ±15 min of NSE open/close.
       Options expiry weeks require additional 20% slippage buffer.
  </div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  MODULE 7  —  DECISION MATRIX
# ══════════════════════════════════════════════════════════════
st.markdown('<hr class="ac-divider">', unsafe_allow_html=True)
st.markdown("""
  <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#3A6080;
              letter-spacing:3px;text-transform:uppercase;margin:8px 0 14px;">
    ── MODULE 7 · INVESTMENT DECISION SUPPORT ──
  </div>
""", unsafe_allow_html=True)

col_dm, col_conf = st.columns([1.6, 1], gap="medium")

with col_dm:
    st.markdown('<div class="module-card module-card-green">', unsafe_allow_html=True)
    st.markdown('<div class="module-label">MODULE 7 · FINAL DECISION MATRIX</div>', unsafe_allow_html=True)
    st.markdown('<div class="module-title">Recommended Actions — PENDING APPROVAL</div>', unsafe_allow_html=True)

    rows = ""
    for m in matrix:
        badge = action_badge(m["action"], m["action_class"])
        cb    = conf_bar(m["confidence"])
        rows += f"""
          <tr>
            <td style="font-weight:600;color:#FFFFFF">{m['ticker']}</td>
            <td>{badge}</td>
            <td>{m['allocation_pct']}%</td>
            <td>₹{m['entry_price']:,}</td>
            <td style="color:#00FF82">₹{m['target_price']:,}</td>
            <td style="color:#FF4D6A">₹{m['stop']:,}</td>
            <td>{m['rsi']}</td>
            <td style="color:{'#00FF82' if m['momentum']>=0 else '#FF4D6A'}">{m['momentum']:+.1f}%</td>
            <td>{cb}</td>
          </tr>
        """
    st.markdown(f"""
      <table class="decision-table">
        <thead>
          <tr>
            <th>Asset</th><th>Signal</th><th>Alloc</th>
            <th>Entry</th><th>Target</th><th>Stop</th>
            <th>RSI</th><th>Momentum</th><th>Confidence</th>
          </tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_conf:
    st.markdown('<div class="module-card module-card-green">', unsafe_allow_html=True)
    st.markdown('<div class="module-label">MODULE 7 · SIGNAL STRENGTH</div>', unsafe_allow_html=True)
    st.plotly_chart(make_confidence_chart(matrix), use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# Approval section
st.markdown("""
  <div style="background:linear-gradient(135deg,#0A1E10 0%,#0D2515 100%);
              border:1px solid #1A4030;border-top:2px solid #00FF82;
              border-radius:6px;padding:20px 24px;margin-top:8px;">
    <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#00FF82;
                letter-spacing:3px;text-transform:uppercase;margin-bottom:8px;">
      ⬡ AWAITING USER APPROVAL
    </div>
    <div style="font-family:'IBM Plex Sans',sans-serif;font-size:13px;color:#A0B8A8;line-height:1.7;">
      The Aladeen-Core pipeline has completed. <strong style="color:#FFFFFF">No simulated trades have been executed.</strong>
      Review the decision matrix above and confirm your action. You may modify ticker inputs or risk parameters
      in the sidebar and re-run the engine at any time.
    </div>
  </div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  MODULE 6  —  MONITORING PARAMETERS
# ══════════════════════════════════════════════════════════════
st.markdown('<hr class="ac-divider">', unsafe_allow_html=True)
st.markdown("""
  <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#3A6080;
              letter-spacing:3px;text-transform:uppercase;margin:8px 0 14px;">
    ── MODULE 6 · PORTFOLIO MONITORING AGENT ──
  </div>
""", unsafe_allow_html=True)

with st.expander("📡  View Post-Trade Alert Thresholds & Monitoring Parameters", expanded=False):
    st.markdown('<div class="module-card module-card-violet" style="margin:0">', unsafe_allow_html=True)
    st.markdown('<div class="module-label">MODULE 6 · ALERT FRAMEWORK</div>', unsafe_allow_html=True)

    mon_rows = []
    for m in matrix:
        mon_rows.append({
            "Asset":              m["ticker"],
            "Stop-Loss Trigger":  f"₹{m['stop']:,}",
            "Drawdown Alert":     f"-{round(risk_tolerance * 0.67)}% (Early) / -{risk_tolerance}% (Hard)",
            "RSI Overbought":     "> 75",
            "RSI Oversold":       "< 30",
            "Review Trigger":     "Nifty50 weekly > -4%",
            "Earnings Watch":     "Q4 FY26 Results (Apr–May 2026)",
        })
    mon_rows.append({
        "Asset":              "PORTFOLIO",
        "Stop-Loss Trigger":  "N/A",
        "Drawdown Alert":     f"-{round(risk_tolerance * 0.67)}% / -{risk_tolerance}%",
        "RSI Overbought":     "Blended > 72",
        "RSI Oversold":       "Blended < 35",
        "Review Trigger":     "RBI Surprise Rate Hike",
        "Earnings Watch":     "Macro calendar events",
    })
    df_mon = pd.DataFrame(mon_rows)
    st.dataframe(df_mon, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("""
  <div style="text-align:center;padding:30px 0 10px;
              font-family:'IBM Plex Mono',monospace;font-size:9px;
              color:#1A2E4A;letter-spacing:2px;line-height:1.9;">
    ALADEEN-CORE · FINANCIAL INTELLIGENCE ENGINE · v1.0<br>
    MOCK SIMULATION — NOT FINANCIAL ADVICE — NO REAL TRADES EXECUTED<br>
    DATA SOURCED VIA YFINANCE · FOR EDUCATIONAL & RESEARCH PURPOSES ONLY
  </div>
""", unsafe_allow_html=True)

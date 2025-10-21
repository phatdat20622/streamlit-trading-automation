# app.py
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Trading Automation Dashboard", layout="wide")

# --- Helper functions ---
@st.cache_data(ttl=60 * 60)
def fetch_data(ticker, period="3mo", interval="1d"):
    """Fetch real market data from Yahoo Finance."""
    data = yf.download(ticker, period=period, interval=interval, auto_adjust=False)
    data.reset_index(inplace=True)
    data.rename(columns={"Date": "date"}, inplace=True)
    return data


def calculate_indicators(df):
    """Add SMA, EMA, and RSI indicators."""
    df["SMA_14"] = df["Close"].rolling(window=14).mean()
    df["EMA_14"] = df["Close"].ewm(span=14, adjust=False).mean()

    delta = df["Close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=14, min_periods=14).mean()
    avg_loss = loss.rolling(window=14, min_periods=14).mean()

    rs = avg_gain / avg_loss
    df["RSI_14"] = 100 - (100 / (1 + rs))

    return df


def plot_candlestick(df, ticker):
    """Plot candlestick chart with SMA and EMA."""
    fig = go.Figure()
    fig.add_trace(
        go.Candlestick(
            x=df["date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Price",
        )
    )
    fig.add_trace(go.Scatter(x=df["date"], y=df["SMA_14"], line=dict(color="blue", width=1), name="SMA 14"))
    fig.add_trace(go.Scatter(x=df["date"], y=df["EMA_14"], line=dict(color="orange", width=1), name="EMA 14"))
    fig.update_layout(
        title=f"{ticker.upper()} — Candlestick Chart with SMA & EMA",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white",
        xaxis_rangeslider_visible=False,
        height=600
    )
    return fig


def plot_rsi(df):
    """Plot RSI indicator."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["date"], y=df["RSI_14"], line=dict(color="purple", width=2), name="RSI 14"))
    fig.add_hline(y=70, line_dash="dash", line_color="red")
    fig.add_hline(y=30, line_dash="dash", line_color="green")
    fig.update_layout(
        title="RSI (Relative Strength Index)",
        xaxis_title="Date",
        yaxis_title="RSI Value",
        template="plotly_white",
        height=250,
    )
    return fig


# --- Streamlit UI ---
st.title("📈 Trading Data Automation Dashboard")
st.markdown(
    "Fetch and analyze real market data using Yahoo Finance API. "
    "Includes SMA, EMA, and RSI indicators — built for data automation & trading analysis."
)

with st.sidebar:
    st.header("Settings")
    ticker = st.text_input("Ticker symbol", value="AAPL", help="Examples: AAPL, TSLA, BTC-USD, ^VNINDEX")
    period = st.selectbox("Data period", options=["1mo", "3mo", "6mo", "1y", "2y"], index=1)
    interval = st.selectbox("Interval", options=["1d", "1wk", "1h"], index=0)
    fetch_btn = st.button("Fetch & Analyze")

# 👇 Đây là phần nội dung chính (bên ngoài sidebar)
main_area = st.container()

with main_area:
    if fetch_btn:
        df = fetch_data(ticker, period=period, interval=interval)
        if df.empty:
            st.warning("No data found. Try another ticker or period.")
        else:
            df = calculate_indicators(df)

            col1, col2 = st.columns([3, 1])
            with col1:
                st.plotly_chart(plot_candlestick(df, ticker), use_container_width=True)
                st.plotly_chart(plot_rsi(df), use_container_width=True)
            with col2:
                st.subheader("Summary Statistics")
                st.write(df[["Close", "SMA_14", "EMA_14", "RSI_14"]].tail(10))

                latest_close = float(df["Close"].iloc[-1])
                rsi_val = float(df["RSI_14"].iloc[-1])
                sma_val = float(df["SMA_14"].iloc[-1])
                ema_val = float(df["EMA_14"].iloc[-1])

                st.metric("Latest Close", f"${latest_close:.2f}")
                st.metric("RSI (14)", f"{rsi_val:.2f}")
                st.metric("SMA (14)", f"{sma_val:.2f}")
                st.metric("EMA (14)", f"{ema_val:.2f}")

            st.download_button(
                "Download Cleaned CSV",
                data=df.to_csv(index=False),
                file_name=f"{ticker}_technical_analysis.csv",
                mime="text/csv",
            )
            st.success("Analysis complete ✅")
    else:
        st.info("Enter a ticker and click **Fetch & Analyze** to start.")


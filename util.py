import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Tech Stock Dashboard", layout="wide")


# 2. CACHED DATA LOADING
@st.cache_data
def load_and_process_data(file_paths):
    temp_list = []
    for file in file_paths:
        if os.path.exists(file):
            df = pd.read_csv(file)
            temp_list.append(df)

    all_data = pd.concat(temp_list, ignore_index=True)
    all_data['date'] = pd.to_datetime(all_data['date'])
    all_data = all_data.sort_values(['Name', 'date'])

    # Pre-calculate Moving Averages
    ma_day = [10, 20, 50]
    for ma in ma_day:
        all_data[f'MA_{ma}'] = all_data.groupby('Name')['close'].transform(lambda x: x.rolling(window=ma).mean())

    return all_data


# --- DATA SETUP ---
base_path = r'C:\Users\leona\PycharmProjects\Python Data Analysis Projects\AAProject sets - 2\SandP-stock-analysis\individual_stocks_5yr'
tickers = ['AAPL', 'AMZN', 'GOOG', 'MSFT']
files = [os.path.join(base_path, f"{t}_data.csv") for t in tickers]

all_data = load_and_process_data(files)

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Dashboard Settings")
st.sidebar.markdown("Filter your view and analysis parameters here.")
date_range = st.sidebar.date_input("Select Date Range",
                                   value=(all_data['date'].min(), all_data['date'].max()))

# --- MAIN UI ---
st.title("🚀 Tech Stock Performance Dashboard")
st.markdown("Detailed analysis of Apple, Amazon, Google, and Microsoft stock data.")

# 3. KPI SECTION (Metrics)
st.subheader("Current Market Snapshots")
cols = st.columns(len(tickers))
for i, ticker in enumerate(tickers):
    latest_price = all_data[all_data['Name'] == ticker]['close'].iloc[-1]
    prev_price = all_data[all_data['Name'] == ticker]['close'].iloc[-2]
    delta = ((latest_price - prev_price) / prev_price) * 100
    cols[i].metric(label=ticker, value=f"${latest_price:.2f}", delta=f"{delta:.2f}%")

st.divider()

# 4. ORGANIZED TABS
tab1, tab2, tab3 = st.tabs(["📊 Price Comparison", "📈 Technical Indicators", "📉 Daily Returns"])

with tab1:
    st.subheader("Cumulative Price Growth")
    fig_price = px.line(
        all_data, x="date", y="close", color="Name",
        title="Closing Prices Over Time",
        template="plotly_white"
    )
    fig_price.update_layout(hovermode="x unified")
    st.plotly_chart(fig_price, use_container_width=True)

with tab2:
    st.subheader("Moving Average Analysis")
    st.info(
        "Moving averages help smooth out price action by filtering out the 'noise' from random short-term price fluctuations.")

    # [Image of stock market technical indicators Moving Averages]

    # Reshape for MA visualization
    plot_columns = ['close', 'MA_10', 'MA_20', 'MA_50']
    df_long = pd.melt(all_data, id_vars=['date', 'Name'], value_vars=plot_columns,
                      var_name='Metric', value_name='Price')

    fig_ma = px.line(
        df_long, x='date', y='Price', color='Metric',
        facet_col='Name', facet_col_wrap=2,
        title="Price vs. Moving Averages (10, 20, 50 Day)",
        height=700
    )
    fig_ma.update_yaxes(matches=None)
    fig_ma.update_layout(hovermode="x unified")
    st.plotly_chart(fig_ma, use_container_width=True)

with tab3:
    st.subheader("Volatility & Daily Returns")
    all_data['Daily return(in %)'] = all_data.groupby('Name')['close'].pct_change() * 100

    # [Image of wide vs long data format transformation]

    fig_return = px.line(
        all_data, x='date', y='Daily return(in %)', color='Name',
        title="Daily Percentage Returns",
        labels={'Daily return(in %)': 'Return %'}
    )
    st.plotly_chart(fig_return, use_container_width=True)
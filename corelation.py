import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Tech Stock Dashboard", layout="wide")
st.title("📊 Tech Stock Performance & Correlation")


# --- DATA LOADING & ALIGNMENT ---
@st.cache_data
def load_and_align_data():
    base_path = r'C:\Users\leona\PycharmProjects\Python Data Analysis Projects\AAProject sets - 2\SandP-stock-analysis\individual_stocks_5yr'
    targets = ['AAPL', 'GOOG', 'MSFT', 'AMZN']

    # 1. Filter files
    all_files = os.listdir(base_path)
    company_files = [f for f in all_files if any(t in f for t in targets)]
    company_files.sort()

    # 2. Use a "Master" DataFrame to align by Date
    # We start with the first file to establish the date index
    first_df = pd.read_csv(os.path.join(base_path, company_files[0]))
    # We take only date and close, renaming close to the ticker name
    main_df = first_df[['date', 'close']].rename(columns={'close': company_files[0].split('_')[0]})
    main_df['date'] = pd.to_datetime(main_df['date'])

    # 3. Merge other files on 'date' to prevent "trimming" or misalignment
    for f in company_files[1:]:
        ticker = f.split('_')[0]
        temp_df = pd.read_csv(os.path.join(base_path, f))
        temp_df['date'] = pd.to_datetime(temp_df['date'])
        temp_df = temp_df[['date', 'close']].rename(columns={'close': ticker})

        # 'outer' join ensures we don't lose days that exist in one file but not another
        main_df = pd.merge(main_df, temp_df, on='date', how='outer')

    # 4. Calculate Daily Returns (% Change)
    tickers = [f.split('_')[0] for f in company_files]
    for ticker in tickers:
        main_df[f'{ticker}_pct_change'] = main_df[ticker].pct_change() * 100

    return main_df.sort_values('date'), tickers


# Load data
df, tickers = load_and_align_data()
pct_cols = [f'{t}_pct_change' for t in tickers]

# --- SIDEBAR INFO ---
st.sidebar.header("Dataset Statistics")
st.sidebar.write(f"Total Trading Days: {len(df)}")
st.sidebar.write(f"Date Range: {df['date'].min().date()} to {df['date'].max().date()}")

# --- VISUALIZATION 1: CORRELATION HEATMAP ---
st.subheader("1. Price Correlation Matrix")
st.markdown("This shows how closely the stock prices move together.")
fig1, ax1 = plt.subplots(figsize=(8, 4))
sns.heatmap(df[tickers].corr(), annot=True, cmap='RdYlGn', fmt=".2f", ax=ax1)
st.pyplot(fig1)

# --- VISUALIZATION 2: DAILY RETURNS ANALYSIS ---
st.subheader("2. Daily Returns Analysis (PairGrid)")
st.markdown("Analyzing the distribution of daily % changes and their relationships.")

# We drop the first row for the PairGrid because pct_change creates one NaN row
chart_data = df[pct_cols].dropna()

# Using the specific PairGrid structure you requested
g = sns.PairGrid(data=chart_data)
g.map_diag(sns.histplot, kde=True)
g.map_lower(sns.scatterplot, s=10, alpha=0.5)  # s=size, alpha=transparency for better visibility
g.map_upper(sns.kdeplot, cmap="Blues_d")

st.pyplot(g.fig)

# --- VISUALIZATION 3: RAW DATA ---
with st.expander("View Cleaned Data Table"):
    st.dataframe(df)
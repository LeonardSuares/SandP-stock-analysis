import streamlit as st
import pandas as pd
import plotly.express as px
import os


# 1. Define a function to load and prep data
@st.cache_data
def get_stock_data(folder_path, tickers):
    temp_list = []
    for ticker in tickers:
        file_path = os.path.join(folder_path, f"{ticker}_data.csv")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            temp_list.append(df)

    # Combine all into one DataFrame
    all_data = pd.concat(temp_list, ignore_index=True)
    all_data['date'] = pd.to_datetime(all_data['date'])

    # 2. CALCULATE DAILY RETURNS FOR ALL AT ONCE (No redundant code)
    # Group by 'Name' so the percent change doesn't jump between different stocks
    all_data['Daily return(in %)'] = (
            all_data.groupby('Name')['close']
            .pct_change() * 100
    )

    return all_data


# --- Main App ---
folder = r'C:\Users\leona\PycharmProjects\Python Data Analysis Projects\AAProject sets - 2\SandP-stock-analysis\individual_stocks_5yr'
tech_tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOG']

df = get_stock_data(folder, tech_tickers)

# 3. Visualization
st.title("Stock Daily Returns Analysis")

# Select a company to view (Interactive prompt)
selected_company = st.selectbox("Select Company to View Daily Returns", tech_tickers)

# Filter the processed data for the specific company
company_df = df[df['Name'] == selected_company]

fig = px.line(
    company_df,
    x='date',
    y='Daily return(in %)',
    title=f"Daily Returns: {selected_company}",
    labels={'Daily return(in %)': 'Return %', 'date': 'Date'}
)

st.plotly_chart(fig, use_container_width=True)
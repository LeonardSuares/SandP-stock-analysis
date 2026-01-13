import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import plotly.express as px
import glob

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

import  warnings
from warnings import filterwarnings
filterwarnings("ignore")

full_list = glob.glob(r'C:\Users\leona\PycharmProjects\Python Data Analysis Projects\AAProject sets - 2\SandP-stock-analysis\individual_stocks_5yr/*csv')

# print(*full_list, sep='\n')

company_list = [
    r'C:\Users\leona\PycharmProjects\Python Data Analysis Projects\AAProject sets - 2\SandP-stock-analysis\individual_stocks_5yr\AAPL_data.csv',
    r'C:\Users\leona\PycharmProjects\Python Data Analysis Projects\AAProject sets - 2\SandP-stock-analysis\individual_stocks_5yr\AMZN_data.csv',
    r'C:\Users\leona\PycharmProjects\Python Data Analysis Projects\AAProject sets - 2\SandP-stock-analysis\individual_stocks_5yr\GOOG_data.csv',
    r'C:\Users\leona\PycharmProjects\Python Data Analysis Projects\AAProject sets - 2\SandP-stock-analysis\individual_stocks_5yr\MSFT_data.csv'
]

temp_list = []

for file in company_list:
    current_df = pd.read_csv(file)
    # 2. Append the dataframe to the LIST (not a dataframe)
    temp_list.append(current_df)

# 3. Use pd.concat to merge them all at once
all_data = pd.concat(temp_list, ignore_index=True)

# Ensure data is sorted by date to prevent line tangling
all_data['date'] = pd.to_datetime(all_data['date'])
all_data = all_data.sort_values('date')

st.subheader("Interactive Stock Price Comparison")

# Create the Plotly figure
fig_plotly = px.line(
    all_data,
    x="date",
    y="close",
    color="Name",
    title="Tech Stock Prices (AAPL, AMZN, GOOG, MSFT)",
    labels={"close": "Closing Price ($)", "date": "Year"},
    template="plotly_white" # Gives it a clean, professional look
)

# Improve the layout (optional)
fig_plotly.update_layout(
    hovermode="x unified", # Shows all stock prices in one tooltip when hovering
    legend_title_text='Company'
)

# Display in Streamlit
st.plotly_chart(fig_plotly, use_container_width=True)
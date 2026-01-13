import streamlit as st
import pandas as pd
import plotly.express as px
import glob

# 1. Setup and Data Loading
full_list = glob.glob(r'C:\Users\leona\PycharmProjects\Python Data Analysis Projects\AAProject sets - 2\SandP-stock-analysis\individual_stocks_5yr/*csv')

company_list = [
    r'C:\Users\leona\PycharmProjects\Python Data Analysis Projects\AAProject sets - 2\SandP-stock-analysis\individual_stocks_5yr\AAPL_data.csv',
    r'C:\Users\leona\PycharmProjects\Python Data Analysis Projects\AAProject sets - 2\SandP-stock-analysis\individual_stocks_5yr\AMZN_data.csv',
    r'C:\Users\leona\PycharmProjects\Python Data Analysis Projects\AAProject sets - 2\SandP-stock-analysis\individual_stocks_5yr\GOOG_data.csv',
    r'C:\Users\leona\PycharmProjects\Python Data Analysis Projects\AAProject sets - 2\SandP-stock-analysis\individual_stocks_5yr\MSFT_data.csv'
]

temp_list = []
for file in company_list:
    current_df = pd.read_csv(file)
    temp_list.append(current_df)

all_data = pd.concat(temp_list, ignore_index=True)
all_data['date'] = pd.to_datetime(all_data['date'])

# 2. Correct Moving Average Calculation
# We use groupby('Name') so the rolling window resets for each stock
ma_day = [10, 20, 50]
for ma in ma_day:
    all_data[f'MA_{ma}'] = all_data.groupby('Name')['close'].transform(lambda x: x.rolling(window=ma).mean())

# 3. Reshape data for Plotly (Wide to Long)
# Plotly Express works best when all values to be plotted are in one column
plot_columns = ['close', 'MA_10', 'MA_20', 'MA_50']
df_long = pd.melt(
    all_data,
    id_vars=['date', 'Name'],
    value_vars=plot_columns,
    var_name='Metric',
    value_name='Price'
)



# 4. Create the Interactive Visual
st.title("Stock Analysis with Moving Averages")

fig = px.line(
    df_long,
    x='date',
    y='Price',
    color='Metric',      # Different lines for Close and MAs
    facet_col='Name',    # Create subplots based on Company Name
    facet_col_wrap=2,    # Wrap into a 2x2 grid
    title="Tech Stocks: Close vs Moving Averages",
    labels={'Price': 'Price ($)', 'date': 'Date'},
    height=800
)

# Improve UI: Synchronize axes and update legend
fig.update_yaxes(matches=None) # Allow each stock to have its own price scale
fig.update_layout(hovermode="x unified")

st.plotly_chart(fig, use_container_width=True)
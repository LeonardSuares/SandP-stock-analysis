import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt  # <--- Needed to show charts in PyCharm
import os

# --- DATA SETUP ---
base_path = r'C:\Users\leona\PycharmProjects\Python Data Analysis Projects\AAProject sets - 2\SandP-stock-analysis\individual_stocks_5yr'
all_files = os.listdir(base_path)

targets = ['AAPL', 'GOOG', 'MSFT', 'AMZN']
company_list = []

for file_name in all_files:
    if any(ticker in file_name for ticker in targets):
        company_list.append(file_name)

# Sort to ensure we know which index is which
company_list.sort()

# Loading data
appl = pd.read_csv(os.path.join(base_path, company_list[0]))
amzn = pd.read_csv(os.path.join(base_path, company_list[1]))
goog = pd.read_csv(os.path.join(base_path, company_list[2]))
msft = pd.read_csv(os.path.join(base_path, company_list[3]))

# Create DataFrame of closing prices
closing_price = pd.DataFrame()
closing_price['AAPL'] = appl['close']
closing_price['AMZN'] = amzn['close']
closing_price['GOOG'] = goog['close']
closing_price['MSFT'] = msft['close']

# --- 1. PAIRPLOT ---
sns.pairplot(closing_price)
plt.show()

# --- 2. CORRELATION HEATMAP ---
correlations = closing_price.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlations, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Stock Price Correlation Heatmap')
plt.show()
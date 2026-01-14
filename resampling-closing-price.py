import pandas as pd
import matplotlib.pyplot as plt
import os


def plot_stock_resampled(df, column='close'):
    """
    Resamples stock data by Day, Month, Quarter, and Year
    and displays them in a 2x2 grid.
    """
    # 1. Prepare the Resampling frequencies and Titles
    # 'D' = Day, 'M' = Month, 'Q' = Quarter, 'A' = Annual (Yearly)
    modes = [('D', 'Daily'), ('M', 'Monthly'), ('Q', 'Quarterly'), ('A', 'Yearly')]

    plt.figure(figsize=(16, 10))

    for i, (freq, title) in enumerate(modes, 1):
        plt.subplot(2, 2, i)

        # Resample and calculate the mean
        resampled_data = df[column].resample(freq).mean()

        # Plotting
        resampled_data.plot()
        plt.title(f"{title} Average {column.capitalize()} Price")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.ylabel('Price ($)')
        plt.xlabel('')  # Remove redundant x-labels for a cleaner look

    plt.tight_layout()  # Adjust spacing so titles don't overlap
    plt.show()


# --- MAIN EXECUTION ---
file_path = r'C:\Users\leona\PycharmProjects\Python Data Analysis Projects\AAProject sets - 2\SandP-stock-analysis\individual_stocks_5yr\AAPL_data.csv'

if os.path.exists(file_path):
    # Load data
    apple = pd.read_csv(file_path)

    # Pre-processing (Mandatory for resampling)
    apple['date'] = pd.to_datetime(apple['date'])
    apple.set_index('date', inplace=True)

    # Call the function
    plot_stock_resampled(apple, 'close')
else:
    print("File not found.")
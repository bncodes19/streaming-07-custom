import yfinance as yf
import pandas as pd

def get_stock_data(ticker, start_date, end_date):
    """
    Get historical stock data using yfinance module.
    """
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        return stock_data
    except Exception as e:
        print("Error occurred:", e)
        return None

def main():

    # Enter the stock for the project and the timeframe
    ticker = 'AMZN'
    start_date = '2023-01-01'
    end_date = '2023-12-31'

    # Run the custom function to pull the stock data
    amazon_stock_data = get_stock_data(ticker, start_date, end_date)

    # Clean the stock data by rounding columns to 2 decimal places
    rounded_amazon_stock_data = amazon_stock_data.round(decimals=2)

    # Write the final DF to a CSV
    rounded_amazon_stock_data.to_csv("stock_data.csv")

if __name__ == "__main__":
    main()
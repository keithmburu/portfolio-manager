import time
from datetime import datetime
import pandas as pd

dt = datetime(2023, 1, 1)
start_date = int(round(dt.timestamp()))

dt = datetime(2023, 3, 31)
end_date = int(round(dt.timestamp()))

stock = 'GOOG'

df = pd.read_csv(f"https://query1.finance.yahoo.com/v7/finance/download/{stock}?period1={start_date}&period2={end_date}&interval=1d&events=history&includeAdjustedClose=true",
    parse_dates = ['Date'], index_col='Date')

print(df)


################################################################
# sample sql query for insert stock data into the database
# INSERT INTO stock_data (stock_ticker, date, open_price, high_price, low_price, close_price, volume)
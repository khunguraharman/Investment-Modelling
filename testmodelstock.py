from urllib.request import urlopen
import json
import pandas as pd
import numpy as np
import yfinance as yf
import time
from datetime import date

# companies = ["AAPL", "MSFT", "IBM", "V", "MA", "GOOGL", "TSLA", "NVDA", "INTC", "AMD", "AMZN", "UBER", "LYFT"]
ticker = 'AAPL'

# pull quarterly financial data
qis_df = pd.read_pickle(ticker + '_qis.pkl')  # un-serialize data
bs_df = pd.read_pickle(ticker + '_bs.pkl')
cf_df = pd.read_pickle(ticker + '_cf.pkl')
last_row = qis_df.shape[0] - 1  # index of the last row obtained from a tuple

oldest = qis_df.loc[last_row, 'date']  # the oldest dated quarter
latest = qis_df.loc[0, 'date']  # the latest dated quarter

# get historical market data
company = yf.Ticker(ticker)  # get company info
history_df = company.history(interval='1d', start=oldest, end=latest)
history_df = history_df.reset_index()  # create indices
history_df = history_df.reindex(index=history_df.index[::-1])  # invert order of rows
history_df = history_df.reset_index(drop=True)  # re-create indices, starting from 0 without keeping old
history_df['Date'] = pd.to_datetime(history_df['Date'])
history_df['unix'] = history_df['Date'].astype('int64') / 10**9
# history_df.to_pickle(ticker + '_prices.pkl')


# ensure correct dates in data frames
quarter_dates = qis_df['unix'].astype('float64')  # most recent to oldest quarterly dates
history_df = pd.read_pickle(ticker + '_prices.pkl')  # un-serialize price history
oldest_quarter_date = quarter_dates.iloc[-1]
oldest_price_date = history_df['unix'].iloc[-1]
if oldest_quarter_date < oldest_price_date:  # price data does not go far back enough
    trim_date = quarter_dates.iloc[-2]  # won't need prices before this date
    trim_index = history_df['unix'].index(history_df['unix'] == trim_date)  # price index of older quarter date
    # history_df = history_df.drop(history_df.index[trim_index:-1])  # trim price df
    print(trim_date)
    print(trim_index)



# get moving average of closing prices
#second_last_quarter_limit = quarter_dates.shape[0] - 2  # set second oldest quarter as a limit
# # limit = quarter_dates.index[quarter_dates == quarter_dates.iloc[-2]][0]
# for quarter_end_date in quarter_dates:
#     quarter_end_index = quarter_dates.index[quarter_dates == quarter_end_date][0]  # index returns a list so pick 0th index of that list
#     if quarter_end_index < second_last_quarter_limit:  # want to stop at second last index
#         # end of quarter, want the price the day before financials are released
#         # start of quarter
#         quarter_start_index = quarter_end_index + 1  # quarter_dates goes from most recent to oldest
#         quarter_start_day = quarter_dates.iloc[quarter_start_index]  # will start at the quarter before the latest one
#
#         # price indices
#         price_end_index = history_df.index[history_df['Date'] == quarter_end_day][0]
#         print(price_end_index)
        # price_end_index = price_end_index[0] - 1  # day before results are released
        # price_start_index = history_df.index[history_df['Date'] == quarter_start_day]
        # price_start_index = price_start_index[0] + 1  # get price from the day after
        # print(price_start_index)
        # print(price_end_index)
#
#         # prices
#         #quarter_price_history = history_df.iloc[price_end_index:price_start_index]
#
#         # avg_price = quarter_price_history.mean()
#
#
#
# # end_of_q =
# # closing_avg =
#
#
#
# # # calculate useful ratios
# # price_df['marketCap'] = price_df['Close']*qis_df['Shares']
# # book_value = bs_df['Total assets'] - bs_df['Total liabilities']
# # price_book_ratio = price_df['marketCap']/book_value
# # print(price_book_ratio)
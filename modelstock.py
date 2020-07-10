from urllib.request import urlopen
import json
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date

# companies = ["AAPL", "MSFT", "IBM", "V", "MA", "GOOGL", "TSLA", "NVDA", "INTC", "AMD", "AMZN", "UBER", "LYFT"]
ticker = 'AAPL'

# pull quarterly financial data
qis_df = pd.read_pickle(ticker + '_qis.pkl')
bs_df = pd.read_pickle(ticker + '_bs.pkl')
cf_df = pd.read_pickle(ticker + '_cf.pkl')
last_row = bs_df.shape[0] - 1
oldest = qis_df.loc[last_row, 'date']  # only want prices between the financial periods
latest = qis_df.loc[0, 'date']

# get historical market data
# company = yf.Ticker(ticker)
# history_df = company.history(interval='1d', start=oldest, end=latest)
# history_df = history_df.reset_index()  # oldest to most recent
# history_df.to_pickle(ticker + '_prices.pkl')


# get moving average of closing prices
quarter_dates = qis_df['unix']  # most recent to oldest
print(quarter_dates)
history_df = pd.read_pickle(ticker + '_prices.pkl')
print(history_df['Date'])
limit = quarter_dates.index[quarter_dates == quarter_dates.iloc[-2]][0]
for quarter_date in quarter_dates:
    index = quarter_dates.index[quarter_dates == quarter_date][0]  #.index returns a list so pick 0th index of that list
    if index < limit:  # want to stop at second last index
        # end of quarter, want the price the day before financials are released
        quarter_end_day = quarter_date
        quarter_end_index = index

        # start of quarter
        quarter_start_index = index + 1
        quarter_start_day = quarter_dates.iloc[quarter_start_index]  # will start at the quarter before the latest one

        # price indices
        price_end_index = history_df.index[history_df['Date'] == quarter_end_day]
        print(price_end_index)
        # price_end_index = price_end_index[0] - 1  # day before results are released
        # price_start_index = history_df.index[history_df['Date'] == quarter_start_day]
        # price_start_index = price_start_index[0] + 1  # get price from the day after
        # print(price_start_index)
        # print(price_end_index)

        # prices
        #quarter_price_history = history_df.iloc[price_end_index:price_start_index]

        # avg_price = quarter_price_history.mean()



# end_of_q =
# closing_avg =



# # calculate useful ratios
# price_df['marketCap'] = price_df['Close']*qis_df['Shares']
# book_value = bs_df['Total assets'] - bs_df['Total liabilities']
# price_book_ratio = price_df['marketCap']/book_value
# print(price_book_ratio)
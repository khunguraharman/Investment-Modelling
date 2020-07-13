from urllib.request import urlopen
import json
import numpy as np
import yfinance as yf
import time
from datetime import date
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'


def stock_multiplier(stock_split):
    if stock_split == 0:
        stock_multiple = 1
    else:
        stock_multiple = stock_split
    return stock_multiple


def calc_mrktcap(closing_price, shares, correction):
    marketcap = closing_price*shares*correction
    return marketcap


# companies = ["AAPL", "MSFT", "IBM", "V", "MA", "GOOGL", "TSLA", "NVDA", "INTC", "AMD", "AMZN", "UBER", "LYFT"]
ticker = 'AAPL'

# pull quarterly financial data
qis_df = pd.read_pickle(ticker + '_qis.pkl')  # un-serialize data
bs_df = pd.read_pickle(ticker + '_bs.pkl')
cf_df = pd.read_pickle(ticker + '_cf.pkl')
qis_df['fillingDate'] = pd.to_datetime(qis_df['fillingDate'])
bs_df['fillingDate'] = pd.to_datetime(bs_df['fillingDate'])
cf_df['fillingDate'] = pd.to_datetime(cf_df['fillingDate'])

oldest = qis_df['date'].iloc[-1]
latest = qis_df['date'].iloc[0]  # the latest dated quarter

# get historical market data
company = yf.Ticker(ticker)  # get company info
history_df = company.history(interval='1d', start=oldest, end=latest)
history_df = history_df.reset_index()  # create indices
history_df = history_df.reindex(index=history_df.index[::-1])  # invert order of rows
history_df = history_df.reset_index(drop=True)  # re-create indices, starting from 0 without keeping old
history_df['Date'] = pd.to_datetime(history_df['Date'])
history_df['unix'] = history_df['Date'].astype('int64') / 10**9
#history_df.to_pickle(ticker + '_prices.pkl')

# ensure correct dates in data frames
quarter_dates = qis_df['unix_q'].astype('float64')  # most recent to oldest quarterly dates
history_df = pd.read_pickle(ticker + '_prices.pkl')  # un-serialize price history
quarter_trim_index = -1
oldest_quarter_date = quarter_dates.iloc[quarter_trim_index]-86400  # time for last trading day before quarter end
oldest_price_date = history_df['unix'].iloc[quarter_trim_index]


while oldest_quarter_date < oldest_price_date:  # price data does not go far back enough
    quarter_trim_index = quarter_trim_index - 1  # want a more recent quarter
    oldest_quarter_date = quarter_dates.iloc[quarter_trim_index]-86400  # need oldest quarter to be more recent

if quarter_trim_index < -1:  # trim financial data if oldest quarter is not recent enough
    quarter_trim_index = quarter_trim_index + 1
    qis_df = qis_df[:len(quarter_dates) + quarter_trim_index]
    bs_df = bs_df[:len(quarter_dates) + quarter_trim_index]
    cf_df = cf_df[:len(quarter_dates) + quarter_trim_index]

qis_df['Avg. MrktCap'] = qis_df['date']
# earnings_releases = qis_df['unix_filling']
# sp_dates = history_df['unix'].values.tolist()
# k = 1
print[qis_df]
# test = history_df[3:8]
# test['Correction'] = test['Stock Splits'].map(stock_multiplier)
# print(test['Correction'])

# for earnings_release in earnings_releases:
#     starting_date = earnings_releases.iloc[k]  # the earnings release date of previous quarter
#     end_date = earnings_release  # release date of next quarter's earnings
#     start_index = sp_dates.index(starting_date)
#     end_index = sp_dates.index(end_date)
#     shares_start_of_quarter = qis_df['weightedAverageShsOutDil'].iloc[k]  # number of shares is previous quarter
#     trading_days = history_df[end_index:start_index+1]  # data frame of relevant pricing data
#     trading_days['Market Cap Correction'] = trading_days['Stock Splits'].map(stock_multiplier)  # new column for stock split corrections
#     trading_days['Closing Market Cap'] = trading_days['Close'].mul(shares_start_of_quarter*trading_days['Market Cap Correction'])
#     # average = trading_days['Closing Market Cap'].mean(axis=1)
#     print(trading_days['Closing Market Cap'])
#     k = k+1


# # drop pricing data before oldest fillingDate
# start_price_Data = qis_df['unix_filling'].iloc[-1]
# price_trim_index = history_df['unix'].values.tolist()
# price_trim_index = price_trim_index.index(start_price_Data)
# history_df = history_df[:price_trim_index+1]
#
# # focus on pricing data between fillings
# end_of_price_period = qis_df['unix_filling'].iloc[-2]
# end_of_price_index = history_df['unix'].values.tolist()
# end_of_price_index = end_of_price_index.index(end_of_price_period)
# Price_data = history_df[end_of_price_index:]







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
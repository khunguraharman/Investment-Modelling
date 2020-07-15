from datetime import date
import yfinance as yf
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'


def stock_multiplier(stock_split):
    if stock_split == 0:
        stock_multiple = 1
    else:
        stock_multiple = stock_split
    return stock_multiple


# companies = ["AAPL", "MSFT", "IBM", "V", "MA", "GOOGL", "TSLA", "NVDA", "INTC", "AMD", "AMZN", "UBER", "LYFT"]
ticker = 'AAPL'

# pull quarterly financial data
qis_df = pd.read_pickle(ticker + '_qis.pkl')  # un-serialize data
bs_df = pd.read_pickle(ticker + '_bs.pkl')
cf_df = pd.read_pickle(ticker + '_cf.pkl')

# ensure correct dates in data frames
unix_qis = pd.to_datetime(qis_df['fillingDate']).astype('int64') / 10**9
unix_bs = pd.to_datetime(bs_df['fillingDate']).astype('int64') / 10**9
unix_cf = pd.to_datetime(cf_df['fillingDate']).astype('int64') / 10**9
quarter_trim_index = -1
oldest_qis = unix_qis.iloc[quarter_trim_index]  # time for last trading day before quarter end
oldest_bs = unix_bs.iloc[quarter_trim_index]  # time for last trading day before quarter end
oldest_cf = unix_cf.iloc[quarter_trim_index]  # time for last trading day before quarter end

oldest = {"bs": oldest_bs, "cf": oldest_cf, "qis": oldest_qis}
limiting_doc = max(oldest)
limit = oldest.get(max(oldest))
if limiting_doc == 'qis':
    quarters = len(qis_df['date'])  # most recent to oldest quarterly dates
elif limiting_doc == 'cf':
    quarters = len(cf_df['date'])
else:
    quarters = len(bs_df['date'])

# get historical market data
oldest = qis_df['fillingDate'].iloc[-1]
latest = date.today()  # the latest dated quarter
company = yf.Ticker(ticker)  # get company info
history_df = company.history(interval='1d', start=oldest, end=latest)
history_df = history_df.reset_index()  # create indices
history_df = history_df.reindex(index=history_df.index[::-1])  # invert order of rows
history_df = history_df.reset_index(drop=True)  # re-create indices, starting from 0 without keeping old
history_df.to_pickle(ticker + '_prices.pkl')
history_df = pd.read_pickle(ticker + '_prices.pkl')  # un-serialize price history
unix_pd = history_df['Date'].astype('int64') / 10**9
oldest_pdata = unix_pd.iloc[quarter_trim_index]  # already datetime64

while limit < oldest_pdata:  # price data does not go far back enough
    quarter_trim_index = quarter_trim_index - 1  # want a more recent quarter
    limit = unix_qis.iloc[quarter_trim_index]  # need oldest quarter to be more recent

if quarter_trim_index < -1:  # trim financial data if oldest quarter is not recent enough
    quarter_trim_index = quarter_trim_index + 1
    qis_df = qis_df[:quarters + quarter_trim_index]
    bs_df = bs_df[:quarters + quarter_trim_index]
    cf_df = cf_df[:quarters + quarter_trim_index]


earnings_releases = qis_df['fillingDate'].values.tolist()
trading_days = history_df['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
trading_days = trading_days.values.tolist()
k = 1
k_max = len(earnings_releases)
prices = history_df.drop(['Date', 'Volume', 'Dividends', 'Stock Splits'], axis=1)
trading_evaluation = prices[:quarters + quarter_trim_index]
trading_evaluation.iloc[0] = np.nan * trading_evaluation.shape[1]  # no data for most recent quarter
capital_exchange = history_df.drop(['Open', 'High', 'Low', 'Close'], axis=1)
capital_exchange['Stock Multiple'] = capital_exchange['Stock Splits'].map(stock_multiplier)  # adjust for stock splits
#capital_exchange.loc[:, 'Dividends Paid'] = capital_exchange.loc[:, 'Dividends'].mul(5 * capital_exchange['Stock Multiple'], axis=0)
# DATE = capital_exchange.loc[lambda x: x['Date'] == '8-9-2019']

for earnings_release in earnings_releases:
    if k+2 <= k_max:
        starting_date = earnings_releases[k]  # the earnings release date of previous quarter
        end_date = earnings_release  # release date of next quarter's earnings
        start_index = trading_days.index(starting_date)
        end_index = trading_days.index(end_date)
        shares_start_of_quarter = qis_df['weightedAverageShsOutDil'].iloc[k]  # number of shares is previous quarter
        price_range = prices[end_index:start_index+1]  # data frame of relevant pricing data
        capital_range = capital_exchange[end_index:start_index+1]  # data frame of relevant volume and dividend data
        market_caps = price_range.mul(shares_start_of_quarter*capital_range['Stock Multiple'], axis=0)
        price_averages = pd.DataFrame(market_caps.mean(axis=0)).T.values.tolist()  # returns a list of lists
        trading_evaluation.iloc[k] = price_averages[0]  # need [0] because averages is a list of lists
        capital_range.loc[:, 'Dividends Paid'] = capital_range.loc[:, 'Dividends'].mul(shares_start_of_quarter * capital_range['Stock Multiple'], axis=0)

        k = k+1

    else:
        break


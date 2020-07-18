from urllib.request import urlopen
import json
import pandas as pd
import numpy as np
from datetime import date
import yfinance as yf
import pickle
import datetime as dt
# pd.options.mode.chained_assignment = None  # default='warn'


def get_jsonparsed_data(url):  # recieve content of the URL, parse is as JSON and return a dictionary
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)


def stock_multiplier(stock_split):
    if stock_split == 0:
        stock_multiple = 1
    else:
        stock_multiple = stock_split
    return stock_multiple


companies = ["AAPL"]  # "MSFT", "IBM", "V", "MA", "GOOGL", "TSLA", "NVDA", "INTC", "AMD", "AMZN", "UBER", "LYFT"]
pickle.dump(companies, open("save.p", "wb"))
refresh = False

for ticker in companies:
    if refresh:
        qis_url = 'https://financialmodelingprep.com/api/v3/income-statement/' + \
                  ticker + '?period=quarter&apikey=c8cd456174e73a2fc87b2ec7bb4744f6'
        qis_dict = get_jsonparsed_data(qis_url)  # dictionary of quarterly incomes statements
        qis_df = pd.DataFrame(data=qis_dict)
        qis_df = qis_df.drop(['symbol', 'acceptedDate', 'period', 'link', 'finalLink'], axis=1)
        cols = qis_df.columns.drop(['date', 'fillingDate'])  # pick every column except for date
        qis_df[cols] = qis_df[cols].apply(pd.to_numeric, errors='coerce')

        bs_url = 'https://financialmodelingprep.com/api/v3/balance-sheet-statement/' + \
                 ticker + '?period=quarter&apikey=c8cd456174e73a2fc87b2ec7bb4744f6'
        bs_dict = get_jsonparsed_data(bs_url)  # dictionary of balance sheet
        bs_df = pd.DataFrame(data=bs_dict)
        bs_df = bs_df.drop(['symbol', 'acceptedDate', 'period', 'link', 'finalLink'], axis=1)
        cols = bs_df.columns.drop(['date', 'fillingDate'])  # pick every column except for date
        bs_df[cols] = bs_df[cols].apply(pd.to_numeric, errors='coerce')

        cf_url = 'https://financialmodelingprep.com/api/v3/cash-flow-statement/' + \
                 ticker + '?period=quarter&apikey=c8cd456174e73a2fc87b2ec7bb4744f6'
        cf_dict = get_jsonparsed_data(cf_url)  # dictionary of cash flow
        cf_df = pd.DataFrame(data=cf_dict)
        cf_df = cf_df.drop(['symbol', 'acceptedDate', 'period', 'link', 'finalLink'], axis=1)
        cols = cf_df.columns.drop(['date', 'fillingDate'])  # pick every column except for date
        cf_df[cols] = cf_df[cols].apply(pd.to_numeric, errors='coerce')
    else:
        qis_df = pd.read_pickle(ticker + '_qis.pkl')  # load financial data
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
        oldest_pdate = qis_df['fillingDate'].iloc[-1]
    elif limiting_doc == 'cf':
        quarters = len(cf_df['date'])
        oldest_pdate = cf_df['fillingDate'].iloc[-1]
    else:
        quarters = len(bs_df['date'])
        oldest_pdate = bs_df['fillingDate'].iloc[-1]

    # get historical market data
    oldest_pdate = qis_df['fillingDate'].iloc[-1]
    latest = date.today()  # the latest dated quarter
    company = yf.Ticker(ticker)  # get company info
    history_df = company.history(interval='1d', start=oldest_pdate, end=latest)
    history_df = history_df.reset_index()  # create indices
    history_df = history_df.reindex(index=history_df.index[::-1])  # invert order of rows
    history_df = history_df.reset_index(drop=True)  # re-create indices, starting from 0 without keeping old
    unix_pd = history_df['Date'].astype('int64') / 10**9
    oldest_pdata = unix_pd.iloc[quarter_trim_index]  # already datetime64

    if not oldest_qis == oldest_bs == oldest_cf:  # trim financial data if oldest quarter is not recent enough
        quarter_trim_index = quarter_trim_index + 1
        qis_df = qis_df[:quarters + quarter_trim_index]
        bs_df = bs_df[:quarters + quarter_trim_index]
        cf_df = cf_df[:quarters + quarter_trim_index]

    earnings_releases = qis_df['fillingDate'].values.tolist()

    trading_days = history_df['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    trading_days = trading_days.values.tolist()
    k = 1
    k_max = len(earnings_releases)-1  # max index
    prices = history_df.copy().drop(['Date', 'Volume', 'Stock Splits', 'Dividends'], axis=1)
    avg_prices = prices.copy()[:quarters]
    trading_evaluation = prices.copy()[:quarters]
    capital_exchange = history_df.copy().drop(['Open', 'High', 'Low', 'Close'], axis=1)
    capital_exchange['Stock Multiple'] = capital_exchange['Stock Splits'].map(stock_multiplier)  # adjust for stock
    # splits
    AvgVolume_TotalDividends = capital_exchange.copy()[:quarters + quarter_trim_index]
    AvgVolume_TotalDividends = AvgVolume_TotalDividends.drop(['Date', 'Stock Multiple', 'Stock Splits'], axis=1)

    while k <= k_max:
        starting_date = earnings_releases[k]  # the earnings release date of previous quarter
        end_date = earnings_releases[k-1]  # release date of next quarter's earnings
        start_index = trading_days.index(starting_date)
        end_index = trading_days.index(end_date)
        shares_start_of_quarter = qis_df['weightedAverageShsOutDil'].iloc[k]  # number of shares is previous quarter
        price_range = prices.copy()[end_index:start_index+1]
        avg_prices.iloc[k] = pd.DataFrame(price_range.mean(axis=0)).T.values.tolist()[0]  # data frame of relevant
        # pricing data
        capital_range = capital_exchange.copy()[end_index:start_index+1]  # data frame of relevant volume and
        # dividend data
        market_caps = price_range.copy().mul(shares_start_of_quarter*capital_range['Stock Multiple'], axis=0)
        trading_evaluation.iloc[k] = pd.DataFrame(market_caps.mean(axis=0)).T.values.tolist()[0]  # returns a
        # list of lists
        capital_range.loc[:, 'Dividends Paid'] = capital_range.loc[:, 'Dividends'].mul(
            shares_start_of_quarter * capital_range['Stock Multiple'], axis=0)
        AvgVolume_TotalDividends.loc[k, 'Volume'] = capital_range.loc[:, 'Volume'].mean(axis=0)
        AvgVolume_TotalDividends.loc[k, 'Dividends'] = capital_range.loc[:, 'Dividends Paid'].sum()
        k = k+1

    avg_prices.iloc[0] = np.nan * avg_prices.shape[1]
    trading_evaluation.iloc[0] = np.nan * trading_evaluation.shape[1]  # no data for most recent quarter
    AvgVolume_TotalDividends.iloc[0] = np.nan * AvgVolume_TotalDividends.shape[1]  # no data for most recent quarter
    AvgVolume_TotalDividends.loc[:, 'date'] = qis_df['date']
    trading_evaluation.loc[:, 'date'] = qis_df['date']
    qis_df.to_pickle(ticker + '_qis.pkl')
    bs_df.to_pickle(ticker + '_bs.pkl')
    cf_df.to_pickle(ticker + '_cf.pkl')
    avg_prices.to_pickle(ticker + 'avgprices.pkl')
    AvgVolume_TotalDividends.to_pickle(ticker + '_VolumeDividends.pkl')
    trading_evaluation.to_pickle(ticker + '_mrktcaps.pkl')

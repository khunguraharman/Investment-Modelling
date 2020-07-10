from urllib.request import urlopen
import json
import pandas as pd
import numpy as np
import datetime as dt


def get_jsonparsed_data(url):  # recieve content of the URL, parse is as JSON and return a dictionary
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)


companies = ["AAPL"]  #, "MSFT", "IBM", "V", "MA", "GOOGL", "TSLA", "NVDA", "INTC", "AMD", "AMZN", "UBER", "LYFT"]

for ticker in companies:
    qis_url = 'https://financialmodelingprep.com/api/v3/income-statement/' + ticker + '?period=quarter&apikey=c8cd456174e73a2fc87b2ec7bb4744f6'
    qis_dict = get_jsonparsed_data(qis_url)  # dictionary of quarterly incomes statements
    qis_df = pd.DataFrame(data=qis_dict)
    qis_df = qis_df.drop(['symbol', 'acceptedDate', 'period', 'link', 'finalLink'], axis=1)
    qis_df['date'] = pd.to_datetime(qis_df['date'])
    qis_df['unix_q'] = qis_df['date'].astype('int64') / 10**9
    qis_df['fillingDate'] = pd.to_datetime(qis_df['fillingDate'])
    qis_df['unix_filling'] = qis_df['fillingDate'].astype('int64') / 10**9
    cols = qis_df.columns.drop('date')   # pick every column except for date
    qis_df[cols] = qis_df[cols].apply(pd.to_numeric, errors='coerce')
    qis_df.to_pickle(ticker + '_qis.pkl')

    bs_url = 'https://financialmodelingprep.com/api/v3/balance-sheet-statement/' + ticker + '?period=quarter&apikey=c8cd456174e73a2fc87b2ec7bb4744f6'
    bs_dict = get_jsonparsed_data(bs_url)  # dictionary of balance sheet
    bs_df = pd.DataFrame(data=bs_dict)
    bs_df = bs_df.drop(['symbol', 'acceptedDate', 'period', 'link', 'finalLink'], axis=1)
    bs_df['date'] = pd.to_datetime(bs_df['date'])
    bs_df['unix_q'] = bs_df['date'].astype('int64') / 10**9
    bs_df['fillingDate'] = pd.to_datetime(qis_df['fillingDate'])
    bs_df['unix_filling'] = qis_df['fillingDate'].astype('int64') / 10 ** 9
    cols = bs_df.columns.drop('date')   # pick every column except for date
    bs_df[cols] = bs_df[cols].apply(pd.to_numeric, errors='coerce')
    bs_df.to_pickle(ticker + '_bs.pkl')

    cf_url = 'https://financialmodelingprep.com/api/v3/cash-flow-statement/' + ticker + '?period=quarter&apikey=c8cd456174e73a2fc87b2ec7bb4744f6'
    cf_dict = get_jsonparsed_data(cf_url)  # dictionary of cash flow
    cf_df = pd.DataFrame(data=cf_dict)
    cf_df = cf_df.drop(['symbol', 'acceptedDate', 'period', 'link', 'finalLink'], axis=1)
    cf_df['date'] = pd.to_datetime(cf_df['date'])
    cf_df['unix_q'] = cf_df['date'].astype('int64') / 10**9
    cf_df['fillingDate'] = pd.to_datetime(qis_df['fillingDate'])
    cf_df['unix_filling'] = cf_df['fillingDate'].astype('int64') / 10 ** 9
    cols = cf_df.columns.drop('date')   # pick every column except for date
    cf_df[cols] = cf_df[cols].apply(pd.to_numeric, errors='coerce')
    cf_df.to_pickle(ticker + '_cf.pkl')



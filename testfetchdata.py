from urllib.request import urlopen
import json
import pandas as pd
import datetime as dt


def get_jsonparsed_data(url):  # receive content of the URL, parse is as JSON and return a dictionary
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)


ticker = 'AAPL'

qis_url = 'https://financialmodelingprep.com/api/v3/income-statement/' + ticker + '?period=quarter&apikey=70124da85f91e1ce31693de7f16ae1f4'
qis_dict = get_jsonparsed_data(qis_url)  # dictionary of quarterly incomes statements

qis_df = pd.DataFrame(data=qis_dict)
qis_df = qis_df.drop(['symbol', 'fillingDate', 'acceptedDate', 'period', 'link', 'finalLink'], axis=1)
qis_df['date'] = pd.to_datetime(qis_df['date'])
qis_df['unix'] = qis_df['date'].astype('int64') / 10**9
#qis_df['unix'] = qis_df['unix'].floordiv(10**9)
cols = qis_df.columns.drop('date')   # pick every column except for date
qis_df[cols] = qis_df[cols].apply(pd.to_numeric, errors='coerce')
#qis_df.to_pickle(ticker + '_qis.pkl')
print(qis_df['date'].head())
print(qis_df['unix'].head())

# qis_df = pd.read_pickle(ticker + '_qis.pkl')
# bs_df = pd.read_pickle(ticker + '_bs.pkl')
# cf_df = pd.read_pickle(ticker + '_cf.pkl')
#
# bs_df['date'] = pd.to_datetime(bs_df['date'])
# cols = bs_df.columns.drop('date')  # pick every column except for date
# bs_df[cols] = bs_df[cols].apply(pd.to_numeric, errors='coerce')
# bs_df['Total assets'] = pd.to_numeric(bs_df['Total assets'])
# bs_df['Total liabilities'] = pd.to_numeric(bs_df['Total liabilities'])
# book_value = bs_df['Total assets'] - bs_df['Total liabilities']





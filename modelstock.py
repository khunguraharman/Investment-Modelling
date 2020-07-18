from datetime import date
import tensorflow as tf
import pandas as pd
import numpy as np
import pickle


def int_to_str(old):
    new = str(old)
    return new


pd.options.mode.chained_assignment = None  # default='warn'

companies = pickle.load(open("save.p", "rb"))

for ticker in companies:
    # Every feature normalized by market cap
    qis_df = pd.read_pickle(ticker + '_qis.pkl')  # load financial data
    features1 = qis_df.copy().loc[:, ['revenue', 'grossProfit', 'operatingIncome', 'incomeTaxExpense', 'netIncome']]
    cf_df = pd.read_pickle(ticker + '_cf.pkl')
    cols = cf_df.loc[:, ['commonStockIssued', 'commonStockRepurchased', 'dividendsPaid', 'freeCashFlow']].columns
    features1[cols] = cf_df.loc[:, ['commonStockIssued', 'commonStockRepurchased', 'dividendsPaid', 'freeCashFlow']]

    # Every feature already normalized
    bs_df = pd.read_pickle(ticker + '_bs.pkl')
    features2 = bs_df.loc[:, 'totalCurrentAssets'].div(bs_df.loc[:, 'totalCurrentLiabilities'],
                                                       axis=0).to_frame(name='Current Ratio')
    test1 = bs_df.loc[:, 'totalCurrentAssets'].sub(bs_df.loc[:, 'inventory'], axis=0)
    test1 = test1.sub(bs_df.loc[:, 'netReceivables'], axis=0)
    features2.loc[:, 'Quick Ratio'] = test1.div(bs_df.loc[:, 'totalCurrentLiabilities'], axis=0)
    features2.loc[:, 'Cash Ratio'] = bs_df.loc[:, 'cashAndCashEquivalents'].div(bs_df.loc[:, 'totalCurrentLiabilities'],
                                                                                axis=0)
    features2.loc[:, 'debt_equity'] = bs_df.loc[:, 'totalLiabilities'].div(bs_df.loc[:, 'totalStockholdersEquity'],
                                                                           axis=0)
    # Normalize volume
    features3 = pd.read_pickle(ticker + '_VolumeDividends.pkl').drop(['Dividends', 'date'], axis=1)

    # Normalize with market cap
    features = [features1, features2, features3]
    features = pd.concat(features, axis=1)
    features.to_pickle(ticker + '_features.pkl')



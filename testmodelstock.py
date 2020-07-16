from datetime import date
import tensorflow as tf
import pandas as pd
import numpy as np
import pickle

pd.options.mode.chained_assignment = None  # default='warn'

companies = pickle.load(open("save.p", "rb"))

for ticker in companies:
    qis_df = pd.read_pickle(ticker + '_qis.pkl')  # load financial data
    features1 = qis_df.loc[:, ['revenue', 'grossProfit', 'operatingIncome', 'incomeTaxExpense', 'netIncome']]
    bs_df = pd.read_pickle(ticker + '_bs.pkl')
    features1.loc[:, 'Current Ratio'] = bs_df.loc[:, 'totalCurrentAssets'].div(bs_df.loc[:, 'totalCurrentLiabilities'],
                                                                               axis=0)
    test1 = bs_df.loc[:, 'totalCurrentAssets'].sub(bs_df.loc[:, 'inventory'], axis=0)
    test1 = test1.sub(bs_df.loc[:, 'netReceivables'], axis=0)
    features1.loc[:, 'Quick Ratio'] = test1.div(bs_df.loc[:, 'totalCurrentLiabilities'], axis=0)
    features1.loc[:, 'Cash Ratio'] = bs_df.loc[:, 'cashAndCashEquivalents'].div(bs_df.loc[:, 'totalCurrentLiabilities'],
                                                                                axis=0)
    features1.loc[:, 'debt_equity'] = bs_df.loc[:, 'totalLiabilities'].div(bs_df.loc[:, 'totalStockholdersEquity'],
                                                                           axis=0)

    #print(features1.loc[:, ['Current Ratio', 'Quick Ratio', 'Cash Ratio', 'debt_equity']])

    cf_df = pd.read_pickle(ticker + '_cf.pkl')
    features2 = cf_df.loc[:, ['netCashProvidedByOperatingActivities', 'netCashUsedForInvestingActivites',
                              'commonStockIssued', 'commonStockRepurchased', 'dividendsPaid']]
    print(cf_df.loc[:, ['netCashProvidedByOperatingActivities']])
    AvgVolume_TotalDividends = pd.read_pickle(ticker + '_VolumeDividends.pkl')
    trading_evaluation = pd.read_pickle(ticker + '_mrktcaps.pkl')

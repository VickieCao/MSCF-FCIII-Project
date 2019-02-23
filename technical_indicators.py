import numpy as np
import pandas as pd
import pandas_datareader as web
from stock_pool_selection import stockpool_select
from Gtrends_change import *


# input: ticker list, can customize N, start, end date
# output: a list of scores 

def technical_ROC(Tickers, N=5, start='2019-02-01', end='2019-02-23'):
    stock_data = web.get_data_yahoo(Tickers, start, end)
    close = stock_data['Close']
    ROC = (close.iloc[-1] - close.iloc[-1-N])/close.iloc[-1-N] * 100
    ROC_score = [1 if ROC[i] < 0 else 0 for i in range(len(ROC))]
    return ROC_score

def technical_MFI(Tickers, N=10, start='2019-02-01', end='2019-02-23'):
    stock_data = web.get_data_yahoo(Tickers, start, end)
    n = len(Tickers)
    date = stock_data.index
    pmf = np.zeros(n)
    nmf = np.zeros(n)
    for i in range(N,0,-1):
        df = pd.DataFrame(stock_data.loc[date[-i]])
        df = df.unstack(level=0)
        df.columns = df.columns.droplevel() 
        tp = (df['Close']+df['High']+df['Low'])/3
        rmf = tp * df['Volume']
        
        df2 = pd.DataFrame(stock_data.loc[date[-i-1]])
        df2 = df2.unstack(level=0)
        df2.columns = df2.columns.droplevel()
        tp2 = (df2['Close']+df2['High']+df2['Low'])/3
        rmf2 = tp2 * df2['Volume']
        pmf += rmf * (rmf > rmf2)
        nmf += rmf * (rmf < rmf2)
    mr = pmf/nmf # money ratio
    MFI = 100 - 100/(1+mr)
    MFI_score = [1 if MFI[i] < 40 else 0 for i in range(len(MFI))]
    return MFI_score

def technical_ARBR(Tickers, N=14, start='2019-02-01', end='2019-02-23'):
    stock_data = web.get_data_yahoo(Tickers, start, end)
    n = len(Tickers)
    date = stock_data.index
    AR = np.zeros(n)
    BR = np.zeros(n)
    for i in range(N, 0, -1):
        df = pd.DataFrame(stock_data.loc[date[-i]])
        df = df.unstack(level=0)
        df.columns = df.columns.droplevel() 
        AR += (df['High']-df['Open'])/(df['Open']-df['Low'])
        
        df2 = pd.DataFrame(stock_data.loc[date[-i-1]]) 
        df2 = df2.unstack(level=0)
        df2.columns = df2.columns.droplevel()
        BR += (df['High']-df2['Close'])/(df2['Close']-df['Low'])

    ARBR_score = [1 if np.logical_and(BR[i]<AR[i], BR[i]<30) else 0 for i in range(len(AR))]
    return ARBR_score

# Encapsulation later

def get_score(Tickers, start='2019-02-01', end='2019-02-23'):
    stock_data = web.get_data_yahoo(Tickers, start=start, end=end)
    date = stock_data.index
    df = pd.DataFrame(stock_data.loc[date[-1]])
    df = df.unstack(level=0)
    df.columns = df.columns.droplevel() 
    df['ROC_score'] = technical_ROC(Tickers)
    df['MFI_score'] = technical_MFI(Tickers)
    df['ARBR_score'] = technical_ARBR(Tickers)
    df['Gtrends_score'] = Gtrends_change(Tickers)
    return df

earnings_surprise = pd.read_csv("D:/Daily Tasks/CMU MSCF/Mini 3/Financial Computing III/Group Project/Data/earnings_surprise.csv")
sentdex = pd.read_csv("D:/Daily Tasks/CMU MSCF/Mini 3/Financial Computing III/Group Project/Data/sentdex.csv")
stockpool_Tickers = stockpool_select(earnings_surprise, sentdex)


score = get_score(stockpool_Tickers)
score.to_csv("stock_score.csv")

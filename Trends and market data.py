#Download data from google trends and Yahoo Finance
from earningsurprise_crawl import earningsurprise_crawl
from sentiment_crawl import sentiment_crawl

import numpy as np
import pandas as pd
#Get tickers - union of earningsurprise and sentiment
sentdex=sentiment_crawl()
earnings_surprise=earningsurprise_crawl()

sentdex=sentdex[sentdex['Sentiment']=='very good']
earnings_surprise['%Surprise']=earnings_surprise['%Surprise'].astype(float)
earnings_surprise.sort_values(by='%Surprise',ascending=False,inplace=True)
earnings_surprise=earnings_surprise.iloc[0:100]
#earnings_surprise=earnings_surprise[earnings_surprise['%Surprise'].astype(float)>0]
sentdex.drop(0,inplace=True)
Ticker_1=list(sentdex['Ticker'])
Ticker_2=list(earnings_surprise['Ticker'])
Tickers=list(set(Ticker_1).union(set(Ticker_2)))


#download Yahoo Finance data
import pandas_datareader as web
'''
remove_list=[]
stock_data={}
for ticker in Tickers:
    try:
        stock_data[ticker]=web.get_data_yahoo(ticker,start='2018-01-01',end='2018-02-08')
    except:
        print(ticker,'failed!')
        remove_list.append(ticker)

stock_data=pd.concat(stock_data.values(), axis=1, keys=stock_data.keys())
stock_data.to_csv('stockdata.csv')
'''
remove_list=['MHFI','NILE','LGF.A','SONO','DPS','MON','COL','CBG','ARG','GAS','TYC','CVC','MJN','PCP','EMC','JDSU','SPOT']
for item in remove_list:
    Tickers.remove(item)

#Download google trends

from pytrends.request import TrendReq
pytrends = TrendReq(hl='en-US',tz=360)
import time
from random import randint

Gtrends=pd.DataFrame([])
for ticker in Tickers:
    try:
        pytrends.build_payload(ticker, cat=0, timeframe='today 1-m', geo='', gprop='')
        interest_over_time_df = pytrends.interest_over_time()
        time.sleep(randint(5, 10))
        Gtrends=pd.concat([Gtrends,interest_over_time_df[ticker]],axis=1)
    except:
        print("This ticker",ticker,"failed!")

Gtrends.to_csv('Google_trends.csv')

# stock_data['return']=np.log(stock_data['Adj Close']/stock_data['Adj Close'].shift(1))
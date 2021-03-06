# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 11:21:20 2019

@author: ThinkPad
"""
import pandas as pd

#stock pool selection
def stockpool_select(earnings_surprise,sentdex):
    #earnings_surprise processing
    earnings_surprise['%Surprise']=earnings_surprise['%Surprise'].astype(float)
    earnings_surprise.sort_values(by='%Surprise',ascending=False,inplace=True)
    earnings_surprise = earnings_surprise[['Ticker','EPS','%Surprise']]  
    
    #sentdex processing
    sentdex.drop(0,inplace=True)
    sentdex = sentdex[['Ticker','Sentiment','Rising or Falling']]
    
    #selection
    sentdex_select = sentdex[(sentdex['Sentiment']=='very good') | (sentdex['Sentiment']=='good')]
    sentdex_select = sentdex_select[sentdex_select['Rising or Falling'] == 'up']
    ES_select = earnings_surprise[(earnings_surprise['EPS']>0) & (earnings_surprise['%Surprise']>0)]
    sentdex_ticker=set(sentdex_select['Ticker'])
    ES_ticker=set(ES_select['Ticker'])
    stockpool_Tickers=list(sentdex_ticker & ES_ticker)
    return stockpool_Tickers

if __name__ == '__main__': 
    earnings_surprise = pd.read_csv("D:/cmu/mini3/FC III/group project/earnings_surprise.csv")
    sentdex = pd.read_csv("D:/cmu/mini3/FC III/group project/sentdex.csv")
    stockpool_Tickers = stockpool_select(earnings_surprise,sentdex)


'''
#Download google trends
from pytrends.request import TrendReq
pytrends = TrendReq(hl='en-US',tz=360)
Gtrends=pd.DataFrame([])
for ticker in stockpool_Tickers:
    kwlist=[ticker]
    try:
        pytrends.build_payload(kwlist, cat=0, timeframe='2019-02-07 2019-02-21', geo='', gprop='')
        interest_over_time_df = pytrends.interest_over_time()
        Gtrends=pd.concat([Gtrends,interest_over_time_df[ticker]],axis=1)
    except:
        print("This ticker",kwlist,"failed!")

Gtrends.to_csv('Google_trends.csv')
'''
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 18:00:59 2019

@author: ThinkPad
"""

from earningsurprise_crawl import earningsurprise_crawl
from sentiment_crawl import sentiment_crawl
import pandas as pd

#earnings_surprise
earnings_surprise = earningsurprise_crawl()
earnings_surprise['%Surprise']=earnings_surprise['%Surprise'].astype(float)
earnings_surprise.sort_values(by='%Surprise',ascending=False,inplace=True)
earnings_surprise_cleaned = earnings_surprise.iloc[0:100]
earnings_surprise_cleaned = earnings_surprise_cleaned[['Ticker','%Surprise']]  

#sentdex
sentdex = sentiment_crawl()
sentdex.drop(0,inplace=True)
sentdex_cleaned = sentdex[sentdex['Sentiment']=='very good']
sentdex_cleaned = sentdex_cleaned[['Ticker','Rising or Falling']]

#stock price
from datetime import datetime, timedelta
stockprice = pd.read_csv("stockdata.csv")
stockprice_cleaned = pd.read_csv("stockdata.csv")
for i in range(len(stockprice['Date'])):
    stockprice_cleaned['Date'][i] = str(datetime.strptime(stockprice_cleaned['Date'][i], "%Y-%m-%d")-timedelta(days=1))[:10]

#google trends
google_trends = pd.read_csv("Google_trends.csv")

##combine to a single sheet
#combine sentdex and suprise
temp = earnings_surprise_cleaned.merge(sentdex_cleaned, how='outer')

#combine google_trends,stockprice_cleaned
stock_data_all = {}
for i in range(1,stockprice_cleaned.shape[1]):
    stock = stockprice_cleaned.columns[i]
    try:
        df={'%Surprise': list(temp[temp['Ticker']==stock]['%Surprise'])*5,
        'Rising or Falling':list(temp[temp['Ticker']==stock]['Rising or Falling'])*5,
        'google_trends':list(google_trends[stock]),
        'Adj price':list(stockprice_cleaned[stock])}
        df = pd.DataFrame(df)
        stock_data_all[stock]=df 
    except:
        pass
stock_data_all=pd.concat(stock_data_all.values(), axis=1, keys=stock_data_all.keys())
stock_data_all.insert(loc=0, column='Date', value=list(stockprice_cleaned.Date))

#export to excel worksheets
write = pd.ExcelWriter('Data_all.xlsx')
earnings_surprise.to_excel(write,sheet_name='earnings_surprise_raw',index=False,encoding='utf_8_sig')
earnings_surprise_cleaned.to_excel(write,sheet_name='earnings_surprise_cleaned',index=False,encoding='utf_8_sig')
sentdex.to_excel(write,sheet_name='sentdex_raw',index=False,encoding='utf_8_sig')
sentdex_cleaned.to_excel(write,sheet_name='sentdex_cleaned',index=False,encoding='utf_8_sig')
stockprice.to_excel(write,sheet_name='stockprice_raw',index=False,encoding='utf_8_sig')
stockprice_cleaned.to_excel(write,sheet_name='stockprice_cleaned',index=False,encoding='utf_8_sig')
google_trends.to_excel(write,sheet_name='google_trends_raw',index=False,encoding='utf_8_sig')
google_trends.to_excel(write,sheet_name='google_trends_cleaned',index=False,encoding='utf_8_sig')
stock_data_all.to_excel(write,sheet_name='stock_data_all',encoding='utf_8_sig')

write.save()

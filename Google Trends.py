import pandas as pd
def Gtrends_change(Tickers):
    '''
    :param Tickers: a list of target tickers
    :return: series of buy/sell
    '''
    Gtrends=pd.read_csv('Google_trends.csv')
    Gtrends=Gtrends[['date']+Tickers]
    this_week_av=Gtrends[Tickers].iloc[7:].mean()
    last_week_av=Gtrends[Tickers].iloc[0:7].mean()
    res=this_week_av-last_week_av
    res.loc[res>0]=1
    res.loc[res<=0]=-1
    return res
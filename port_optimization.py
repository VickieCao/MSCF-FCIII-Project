
import math as m
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas_datareader as web
import time
from datetime import date
from datetime import timedelta

def port_optimization():
    
    # Obtain selected stock list
    stock_list = pd.read_csv("E:/2019/2019Spring/Mini3/Financial Comp III/Group Project Files/stock_score.csv")
    stock_list = pd.DataFrame(stock_list)
    stock_list['Score'] = np.sum(stock_list.iloc[:,7:],axis=1)
    
    # Sort selected stock according to scores
    stock_list_df = stock_list.sort_values('Score',ascending=False)

    # User input preference
    no_of_stock = int(input("How many stocks would you like to invest in? "))
    max_vol = float(input("How much risk can you tolerate? "))
    inv_horizon = int(input("Investment horizon (in days): "))
    
    # Obtain market data of selected stock
    today = date.today()
    start_date = today - timedelta(days=inv_horizon)
    tick = stock_list_df['Symbols'][:no_of_stock]
    tick_raw = web.get_data_yahoo(tick,
                                 start=str(start_date), end=str(today))
    tick_AdjClose = tick_raw['Adj Close']
    ticklogret = np.log(tick_AdjClose / tick_AdjClose.shift(1))
    
    # Get rid of all 0.0 or NaN rows
    logret_lr = ticklogret[(ticklogret.T != 0.0).any()]    # keep any row with any non-0.0 column value
    logret_lr = logret_lr[logret_lr.T.notnull().all()]       # keep any row with all non-NaN column values
    
    # Create random portfolios
    weights = np.random.rand(20000, no_of_stock)
    weights = weights/weights.sum(axis=1, keepdims=True)
    pflogret = np.matmul(logret_lr.values, weights.T)
    pfmean_an_lr = np.mean(pflogret, axis=0)*logret_lr.shape[0]
    pf_an_std = np.std(pflogret, axis=0)*m.sqrt(logret_lr.shape[0])
    
    # Calculate performance for portfolios with acceptable risk
    accept_pf_ret = pfmean_an_lr[np.where(pf_an_std<=max_vol)]
    accept_pf_std = pf_an_std[np.where(pf_an_std<=max_vol)]
        
    # Identify the portfolio with minimum risk
    min_std_ind = np.argmin(accept_pf_std)
    min_std_weight = weights[min_std_ind, :]
    min_std = np.min(accept_pf_std)
    min_std_meanlr = accept_pf_ret[min_std_ind]
    print('\nPortfolio with Minimum risk:')
    print('Selected Stock: ', np.array(tick))
    print('Weights: ', min_std_weight)
    print('Expected return: ', min_std_meanlr)
    print('Standard deviation: ', min_std)
    
    # Select portfolios with higher returns than minimum risk
    effi_pf_ret = accept_pf_ret[np.where(accept_pf_ret>=min_std_meanlr)]
    effi_pf_std = accept_pf_std[np.where(accept_pf_ret>=min_std_meanlr)]
    effi_pf_sharp = (effi_pf_ret-0.0242267)/effi_pf_std
    
    # Get portfolios on efficient frontier
    # with largest Sharpe ratio for each level of expected return
    round_ret = np.floor(effi_pf_ret/0.001)*0.001
    effi_pf = np.array((effi_pf_ret, effi_pf_std, effi_pf_sharp, round_ret)).T
    effi_pf = pd.DataFrame(effi_pf)
    effi_pf.columns = ['Return', 'Stdev', 'Sharp', 'Round Return']
    group_max_idx = effi_pf.groupby(['Round Return'])['Sharp'].transform(max) == effi_pf['Sharp']
    pf_max_sharp = effi_pf[group_max_idx]
    
    # Identify the portfolio with maximum Sharpe ratio
    max_sharpe_ind = np.argmax(effi_pf_sharp)
    max_sharpe_weight = weights[max_sharpe_ind, :]
    max_sharpe = np.max(effi_pf_sharp)
    max_sharpe_meanlr = effi_pf_ret[max_sharpe_ind]
    max_sharpe_stdlr = effi_pf_std[max_sharpe_ind]
    print('\nPortfolio with Maximum Sharpe ratio:')
    print('Selected Stock: ', np.array(tick))
    print('Weights: ', max_sharpe_weight)
    print('Expected return: ', max_sharpe_meanlr)
    print('Standard deviation: ', max_sharpe_stdlr)
    print('Sharpe ratio: ', max_sharpe)
    
    # Plot portfolio
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(accept_pf_std, accept_pf_ret, s=1, c='grey')
    ax.scatter(pf_max_sharp['Stdev'], pf_max_sharp['Return'], s=2, c='blue')
    ax.scatter(min_std, min_std_meanlr, s=20, c='red')
    ax.scatter(max_sharpe_stdlr, max_sharpe_meanlr, s=20, c='magenta')
    ax.legend(['Possible', 'Efficient', 'Minimum Risk', 'Maximum Sharpe'])
    plt.grid()
    plt.xlabel('Annualized Standard Deviation')
    plt.ylabel('Annualized Expected Return')
    plt.show()
    
    # Plot individual stocks
    plot_yn = input("Show performance of individual stocks (Y/N): ")
    if plot_yn == 'Y':
        # Get full performance of the stock
        tick_raw_full = web.get_data_yahoo(tick,
                                start=str(start_date-timedelta(days=30)), 
                                end=str(today))
        tick_AdjClose_full = tick_raw_full['Adj Close']
        
        tick_AdjClose = tick_AdjClose[(tick_AdjClose.T != 0.0).any()]    # keep any row with any non-0.0 column value
        tick_AdjClose = tick_AdjClose[tick_AdjClose.T.notnull().all()]       # keep any row with all non-NaN column values
        tick_AdjClose_full = tick_AdjClose_full[(tick_AdjClose_full.T != 0.0).any()]    # keep any row with any non-0.0 column value
        tick_AdjClose_full = tick_AdjClose_full[tick_AdjClose_full.T.notnull().all()]       # keep any row with all non-NaN column values
        
        # Plot stock performance and moving average
        fig2, axs = plt.subplots(no_of_stock,1,figsize=(16,9),sharex=True)
        for i in range(no_of_stock):
            axs[i].grid()
            # plot individual stock performance
            axs[i].plot(tick_AdjClose.index,tick_AdjClose.iloc[:,i],c='blue')
            # calculate 10-day and 20-day moving average
            close = tick_AdjClose_full.iloc[:,i]
            length = len(tick_AdjClose)
            short_rolling = close.rolling(window=10).mean()
            long_rolling = close.rolling(window=20).mean()
            # plot moving average
            axs[i].plot(tick_AdjClose.index,short_rolling.iloc[-length:],c='red')
            axs[i].plot(tick_AdjClose.index,long_rolling.iloc[-length:],c='grey')
            axs[i].legend([tick.iloc[i], '10 days MA', '20 days MA'],loc=2)
            axs[i].set_title(tick.iloc[i])
        plt.show()

if __name__ == '__main__':
    port_optimization()
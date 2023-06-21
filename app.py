#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime
import streamlit as st
import numpy as np



def show(start_day,end_day,top_num,amount):
    past_perf = []

    sym_data = pd.DataFrame({'Symbol': ['ADANIENT', 'ADANIPORTS', 'APOLLOHOSP', 'ASIANPAINT', 'AXISBANK',
                             'BAJAJ-AUTO', 'BAJFINANCE', 'BAJAJFINSV', 'BPCL', 'BHARTIARTL',
                             'BRITANNIA', 'CIPLA', 'COALINDIA', 'DIVISLAB', 'DRREDDY',
                             'EICHERMOT', 'GRASIM', 'HCLTECH', 'HDFCBANK', 'HDFCLIFE',
                             'HEROMOTOCO', 'HINDALCO', 'HINDUNILVR', 'HDFC', 'ICICIBANK', 'ITC',
                             'INDUSINDBK', 'INFY', 'JSWSTEEL', 'KOTAKBANK', 'LT', 'M&M',
                             'MARUTI', 'NTPC', 'NESTLEIND', 'ONGC', 'POWERGRID', 'RELIANCE',
                             'SBILIFE', 'SBIN', 'SUNPHARMA', 'TCS', 'TATACONSUM', 'TATAMOTORS',
                             'TATASTEEL', 'TECHM', 'TITAN', 'UPL', 'ULTRACEMCO', 'WIPRO']})
    #print(sym_data.head())
    cost_to_invest = amount/top_num

    start_day = start_day +" 00:00:00+05:30"
    end_day = end_day + " 00:00:00+05:30"
    x=0
    for company in sym_data["Symbol"]:
        his_data = yf.Ticker(company + ".NS")
        data = his_data.history(period = "max")
        arr = np.arange(0, len(data.index))
        data["SR_No"] = arr
        #print(data)
        indx = data["SR_No"][start_day]
        #print(start)
        end = data["SR_No"][end_day]
        x = end - indx
        #print(x)
        perf = ((data["Close"][indx-1] - data["Close"][indx-101])/data["Close"][indx-101])*100
        past_perf.append(perf)

    sym_data["past_perf"] = past_perf
    top_n_perf = []

    top_n_stock = sym_data.nlargest(top_num, ["past_perf"])

    st.write("Top Stocks", top_n_stock["Symbol"]) 

    for company in top_n_stock["Symbol"]:
        his_data = yf.Ticker(company + ".NS")
        data = his_data.history(period = "max")
        arr = np.arange(0, len(data.index))
        data["SR_No"] = arr
        k= 0
        start = data["SR_No"][start_day]
        end = data["SR_No"][end_day]
        initial = cost_to_invest
        top_perf = []
        for i in range(start-1,end-1):
            now = ((data["Close"][i+1] - data["Close"][i])/data["Close"][i])*initial
            #print(now)
            top_perf.append(now + initial)
            initial = now + initial
            k += 1
        top_n_perf.append(top_perf)

    ans = len(top_n_perf[0])*[0]
    for i in range(len(top_n_perf[0])):
        for j in range(len(top_n_perf)):
            ans[i] += top_n_perf[j][i]


    #print(top_n_perf)
    nifty_50 = yf.Ticker("^NSEI")
    nifty_50_data = nifty_50.history(start = "2020-10-01")

    nifty_50_data['Returns'] = nifty_50_data['Close'].pct_change()

    # Calculate equity curve with daily updates
    equity_curve = pd.DataFrame()
    #equity_curve['Date'] = data['Date']
    equity_curve['Equity'] = (1 + nifty_50_data['Returns']).cumprod() *amount 

    # Print the equity curve
    #print(equity_curve)



    #equity_curve = data[['Date', 'Equity']]
    equity_curve['Equity'].fillna(method='ffill', inplace=True)
    equity_curve['Equity'].fillna(method='bfill', inplace=True)
    # Plot the equity curve
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(np.arange(0,len(equity_curve['Equity'])), equity_curve['Equity'])
    ax.plot(np.arange(0,len(ans)), ans)
    ax.set_title('Equity Curve')
    ax.set_xlabel('Date')
    ax.set_ylabel('Total Value')


    st.pyplot(fig)



    def calculate_cagr(prices):
        initial_price = prices[0]
        print(initial_price)
        final_price = prices[-1]
        print(final_price)
        num_years = len(prices) / 252  # Assuming 252 trading days in a year
        print(num_years)
        cagr = (final_price / initial_price) ** (1 / num_years) - 1
        return cagr * 100

    def calculate_volatility(prices):
        returns = np.diff(prices) / prices[:-1]
        volatility = np.std(returns) * np.sqrt(252)  # Assuming 252 trading days in a year
        return volatility * 100

    def calculate_sharpe_ratio(prices):
        returns = np.diff(prices) / prices[:-1]
        sharpe_ratio = (np.mean(returns)/np.std(returns))* np.sqrt(252)
        return sharpe_ratio



    cagr_1 = calculate_cagr(ans)
    volatility_1 = calculate_volatility(ans)
    sharpe_ratio_1 = calculate_sharpe_ratio(ans)

    cagr_2 = calculate_cagr(equity_curve['Equity'])
    volatility_2 = calculate_volatility(equity_curve['Equity'])
    sharpe_ratio_2 = calculate_sharpe_ratio(equity_curve['Equity'])

    # Create a DataFrame with the performance data
    data = {
        'Index': ['CAGR (%)','Volatility (%)','Sharpe Ratio'],
        'Nifty 50': [cagr_2, volatility_2, sharpe_ratio_2],
        'Sample Strategy' : [cagr_1, volatility_1, sharpe_ratio_1]
    }
    df = pd.DataFrame(data)

    # Display the table
    st.table(df)



start_day = st.text_input("Enter Start Day")
end_day = st.text_input("Enter End Day")

# Integer inputs
top_num = st.number_input("Enter Number Top Stocks", step=1)
amount = st.number_input("Enter Amount", step=1)

if st.button("Multiply"):
    show(start_day,end_day,top_num,amount)
    
    


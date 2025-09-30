from os import write

import yfinance as yf
import os
import json as j

from setuptools.command.saveopts import saveopts

import action_handler

#set the tickers you want the bot to watch
tickers = ["CMCSA"]
start_date = "2000-01-01"
end_date = "2024-12-31"

start_cash = 50
#download the data
data = yf.download(tickers, start_date, end_date)
data.fillna(0)

portfolio = {'stocks': {}, 'cash': start_cash}
dict(portfolio)
for ticker in tickers:
    portfolio['stocks'][ticker] = [0,0]

def get_value(portfolio):
    cash = portfolio['cash']
    stocks_value = 0
    for ticker in portfolio['stocks']:
        stocks_value += portfolio['stocks'][ticker][1]
    total = cash + stocks_value
    return total

def get_real(portfolio,data,day_id):
    cash = portfolio['cash']
    stocks_value = 0
    for ticker in portfolio['stocks']:
        stocks_value += portfolio['stocks'][ticker][0]* list(data['Close'][ticker])[day_id]
    real = cash + stocks_value
    return real

def stock_market(data,tickers,portfolio,portfolio_value=None,porfolio_real=None,day_id=0):
    length_data = len(list(data['Close'][tickers[0]]))
    start_cash = portfolio['cash']
    if portfolio_value is None:
        portfolio_value = [start_cash, start_cash]
    if porfolio_real is None:
        portfolio_real = [start_cash, start_cash]
    for i in range(day_id,length_data):
        if i == 0:
            continue
        else:
            cmcsa_high = list(data['High']['CMCSA'])[i-1],
            cmcsa_low = list(data['Low']['CMCSA'])[i-1],
            cmcsa_close = list(data['Close']['CMCSA'])[i-1],
            cmcsa_open = list(data['Open']['CMCSA'])[i],
            #ups_high = list(data['High']['UPS'])[i-1],
            #ups_low = list(data['Low']['UPS'])[i-1],
            #ups_close = list(data['Close']['UPS'])[i-1],
            #ups_open = list(data['Open']['UPS'])[i]

            day_data = {'cmcsa_high': cmcsa_high, 'cmcsa_low':cmcsa_low, 'cmcsa_close':cmcsa_close, 'cmcsa_open':cmcsa_open,
                        #'ups_high':ups_high, 'ups_low':ups_low, 'ups_close':ups_close, 'ups_open':ups_open
                        }

            print(day_data)
            print(portfolio)
            action = 'cmcsa' #input('Which stock would you like to trade?  ')
            bs=input('Buy or Sell?  ')
            portfolio = action_handler.action_handler(action.upper(),bs, portfolio,data,i,tickers)
            if i == 1:
                portfolio_value[1] = get_value(portfolio)
                portfolio_real[1] = get_real(portfolio,data,i)
            else:
                portfolio_value.append(get_value(portfolio))
                portfolio_real.append(get_real(portfolio,data,i))
            cookie=portfolio_real[i]/portfolio_real[i-1]
            print(f'You get {cookie-1}% of a cookie')
            with open('save.json','w')  as f:
                write = [portfolio,day_id,portfolio_value,portfolio_real]
                j.dump(write, f)


if os.path.exists('save.json') == False:
    stock_market(data,tickers,portfolio)
else:
    with open('save.json','r') as f:
        portfolio,day_id,portfolio_value,portfolio_real = j.load(f)
    stock_market(data, tickers, portfolio, portfolio_value,portfolio_real,day_id)
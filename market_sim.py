import random
import math

def randfloat(a,b,c):
    scale = a-b
    add = scale*c
    value = add+b
    return float(format(value,'.2f'))

def buy_request(portfolio, ticker, data, day_id):
    cash = portfolio['cash']
    #the buy_amt is the amount the agent is requesting to buy
    #we are going to randomize a prize based on the data, and then fufil the order if its possible
    high = list(data['High'][ticker])[day_id]
    low = list(data['Low'][ticker])[day_id]
    buy_price = randfloat(high,low,random.random())
    if buy_price <= cash:
        cash -= buy_price
        portfolio['cash'] = float(format(cash,'.2f'))
        portfolio['stocks'][ticker][0] += 1
        portfolio['stocks'][ticker][1] += buy_price
        portfolio['stocks'][ticker][1] = float(format(portfolio['stocks'][ticker][1],'.2f'))
        return portfolio
    else:
        return portfolio

def sell_request(portfolio, ticker, data, day_id):
    cash = portfolio['cash']
    high = list(data['High'][ticker])[day_id]
    low = list(data['Low'][ticker])[day_id]
    sell_price = randfloat(high,low,random.random())
    if 1 <= portfolio['stocks'][ticker][0]:
        portfolio['cash'] += float(format(sell_price, '.2f'))

        portfolio['stocks'][ticker][1] -= float(format((portfolio['stocks'][ticker][1] / portfolio['stocks'][ticker][0]),'.2f'))
        portfolio['stocks'][ticker][0] -= 1
        return portfolio
    else:
        return portfolio
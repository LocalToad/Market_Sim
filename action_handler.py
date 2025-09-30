import math
import market_sim

def max_buy(ticker,cash,data,day_id):
    open = list(data['Open'][ticker])[day_id]
    buy = cash/open
    buy = math.floor(buy)
    return buy


def action_handler(action, bs, portfolio, stock_data, day_id, tickers):
    if bs.lower() == 'buy':
        portfolio = market_sim.buy_request(portfolio,action,stock_data,day_id)

    if bs.lower() == 'sell':
        portfolio = market_sim.sell_request(portfolio,action,stock_data,day_id)

    if portfolio['stocks']['CMCSA'][0] == 0:
        portfolio['stocks']['CMCSA'][1] = 0
    return portfolio
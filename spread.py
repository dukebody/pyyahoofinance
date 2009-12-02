#!/usr/bin/python

import utils
from stockmarket import Stock, Market

sap_tickers = utils.get_tickers() # Standard & Poor's tickers
stocks = utils.get_stocks_from_tickerslist(sap_tickers)
dates = utils.get_dates(stocks[0].ticker) 
market = Market(stocks)

spread = []
market_performance = []
dates_shown = []
STEP = 30

for i in range(STEP, len(stocks[0].values)-STEP, STEP):
    previous = i - STEP
    now = i
    next = i + STEP
    strong_stocks = [s for s in stocks 
                     if s.getOffensive(previous, now) >= 100 and s.getDefensive(previous, now) <= 100]
    weak_stocks = [s for s in stocks 
                   if s.getOffensive(previous, now) <= 100 and s.getDefensive(previous, now) >= 100]
 
    mean_strong_performance = utils.mean([s.getPerformance(now, next) for s in strong_stocks])
    mean_weak_performance = utils.mean([s.getPerformance(now, next) for s in weak_stocks])
    spread.append(mean_strong_performance - mean_weak_performance)
    market_performance.append(market.getPerformance(previous, now)) # to look for correlations with the spread
    dates_shown.append(dates[now]) # dates to be shown in the X axis

# format the data properly and save it in a file
columns = (['dates'] + dates_shown, 
           ['spread'] + utils.stringify(spread), 
           ['market'] + utils.stringify(market_performance))
rows = zip(*columns)
out = open('spread.txt', 'w')
for row in rows:
    out.write(' '.join(row))
    out.write('\n')
out.close()

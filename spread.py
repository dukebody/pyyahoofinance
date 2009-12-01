#!/usr/bin/python

import utils
from stockmarket import Stock, Market

sap_tickers = utils.get_tickers() # Standard & Poor's tickers
closes = utils.get_closes_from_tickerslist(sap_tickers)
valid_tickers = closes.keys()
dates = utils.get_dates(valid_tickers[0])
stocks = [Stock(ticker, closes[ticker]) for ticker in valid_tickers]
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
    market_performance.append(market.getPerformance(previous, now))
    dates_shown.append(dates[now])


columns = (['dates'] + dates_shown, 
           ['spread'] + utils.stringify(spread), 
           ['market'] + utils.stringify(market_performance))
rows = zip(*columns)
out = open('spread.txt', 'w')
for row in rows:
    out.write(' '.join(row))
    out.write('\n')
out.close()

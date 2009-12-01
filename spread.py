#!/usr/bin/python

import utils
from stockmarket import Stock, Market

sap_tickers = utils.get_tickers() # Standard & Poor's tickers
closes = utils.get_closes_from_tickerslist(sap_tickers)
valid_tickers = closes.keys()
stocks = [Stock(ticker, closes[ticker]) for ticker in valid_tickers]
market = Market(stocks)

spread = []
market_performance = []
STEP = 30

for i in range(STEP, len(stocks[0].values)-STEP, STEP):
    start = i
    end = i+STEP
    strong_stocks = [s for s in stocks 
                     if s.getOffensive(start, end) >= 100 and s.getDefensive(start, end) <= 100]
    weak_stocks = [s for s in stocks 
                   if s.getOffensive(start, end) <= 100 and s.getDefensive(start, end) >= 100]
 
    mean_strong_performance = utils.mean([s.getPerformance(start+STEP, end+STEP) for s in strong_stocks])
    mean_weak_performance = utils.mean([s.getPerformance(start+STEP, end+STEP) for s in weak_stocks])
    spread.append(mean_strong_performance - mean_weak_performance)
    market_performance.append(market.getPerformance(start, end))


columns = (utils.stringify(spread), utils.stringify(market_performance))
rows = zip(*columns)
out = open('spread.txt', 'w')
for row in rows:
    out.write(' '.join(row))
    out.write('\n')
out.close()

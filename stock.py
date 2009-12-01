#!/usr/bin/python

import utils

class Stock:
    def __init__(self, ticker, values):
        """values -> list of values of the stock."""
        self.ticker = ticker
        self.values = values
        self.returns = self._getReturns()
        self.market = None

    def _getReturns(self):
        return [0] + [(self.values[i-1] - self.values[i])/self.values[i-1]*100 for i in range(1, len(self.values))]

    def getOffensive(self, start_day, end_day):
        stock_returns = self.returns[start_day:end_day]
        market_returns = self.market.returns[start_day:end_day]
        offensive_benchmark = self.market.getOffensiveBenchmark(start_day, end_day)
        stock_offensive_overperforms = [stock_returns[i]/offensive_benchmark*100 for i in range(0, len(stock_returns)) if market_returns[i] >= 0]
        return utils.mean(stock_offensive_overperforms)

    def getDefensive(self, start_day, end_day):
        stock_returns = self.returns[start_day:end_day]
        market_returns = self.market.returns[start_day:end_day]
        defensive_benchmark = self.market.getDefensiveBenchmark(start_day, end_day)
        stock_defensive_overperforms = [stock_returns[i]/defensive_benchmark*100 for i in range(0, len(stock_returns)) if market_returns[i] <= 0]
        return utils.mean(stock_defensive_overperforms)

        

class Market:
    def __init__(self, stocks):
        self.stocks = stocks
        for s in stocks:
            s.market = self
        self.values = self._getValues()
        self.returns = self._getReturns()
        
    def _getValues(self):
        stocks_values = [s.values for s in self.stocks]
        return utils.point_mean(stocks_values)

    def _getReturns(self):
        return [0] + [(self.values[i-1] - self.values[i])/self.values[i-1]*100 for i in range(1, len(self.values))]  

    def getOffensiveBenchmark(self, start_day, end_day):
        market_returns = self.returns[start_day:end_day]
        offensive_returns = [r for r in market_returns if r>=0]
        offensive_benchmark = utils.mean(offensive_returns)
        return offensive_benchmark

    def getDefensiveBenchmark(self, start_day, end_day):
        market_returns = self.returns[start_day:end_day]
        defensive_returns = [r for r in market_returns if r>=0]
        defensive_benchmark = utils.mean(defensive_returns)
        return defensive_benchmark


sap_tickers = utils.get_tickers() # Standard & Poor's tickers
closes = utils.get_closes_from_tickerslist(sap_tickers)
valid_tickers = closes.keys()
stocks = [Stock(ticker, closes[ticker]) for ticker in valid_tickers]
market = Market(stocks)


columns = [[s.ticker] + [str(s.getOffensive(1,22))] for s in market.stocks]

start = 1
end = 50
rows = [(str(s.getOffensive(start, end)), str(s.getDefensive(start, end))) for s in market.stocks]
out = open('results.txt', 'w')
for row in rows:
    out.write(' '.join(row))
    out.write('\n')
out.close()

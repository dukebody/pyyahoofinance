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
        stock_offensive_overperforms = [(s_return - m_return)/m_return*100 for s_return in stock_returns for m_return in market_returns if m_return >= 0]
        return utils.mean(stock_offensive_overperforms)
        

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


sap_tickers = utils.get_tickers() # Standard & Poor's tickers
closes = utils.get_closes_from_tickerslist(sap_tickers)
valid_tickers = closes.keys()
stocks = [Stock(ticker, closes[ticker]) for ticker in valid_tickers]
market = Market(stocks)

columns = [[s.ticker] + [str(s.getOffensive(1,22))] for s in market.stocks]

rows = zip(*columns)
out = open('results.txt', 'w')
for row in rows:
    out.write(' '.join(row))
    out.write('\n')
out.close()

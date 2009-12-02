import utils

class Stock:
    def __init__(self, ticker, values):
        self.ticker = ticker
        self.values = values
        self.returns = self._getReturns()
        self.market = None

    def _getReturns(self):
        """Calculate the historical returns as the relative difference
        percentage between the values in subsequent days. The first
        return is set arbitrarily to 0 because there's no previous
        value to compare with."""
        return [0] + [(self.values[i] - self.values[i-1])/self.values[i-1]*100 for i in range(1, len(self.values))]

    def getPerformance(self, start_day, end_day):
        """Calculate the average performance along a given period as
        the product of the daily returns for this period."""
        selected_returns = self.returns[start_day:end_day]
        performances = [r/100+1 for r in selected_returns]
        return (utils.contract(performances)-1)*100

    def getOffensive(self, start_day, end_day):
        """The offensive score of a stock for a given period is the
        mean of the stocks returns compared to the offensive
        benchmark, taking into account only the days when the market
        was raising."""
        stock_returns = self.returns[start_day:end_day]
        market_returns = self.market.returns[start_day:end_day]
        offensive_benchmark = self.market.getOffensiveBenchmark(start_day, end_day)
        stock_offensive_overperforms = [stock_returns[i]/offensive_benchmark*100 for i in range(0, len(stock_returns)) if market_returns[i] >= 0]
        return utils.mean(stock_offensive_overperforms)

    def getDefensive(self, start_day, end_day):
        """The defensive score of a stock for a given period is the
        mean of the stocks returns compared to the defensive
        benchmark, taking into account only the days when the market
        was going down."""
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
        """The daily values for the market are calculated as the mean
        of the daily values of all stocks in the market."""
        stocks_values = [s.values for s in self.stocks]
        return utils.point_mean(stocks_values)

    def _getReturns(self):
        """Calculate the historical returns as the relative difference
        percentage between the market values in subsequent days. The
        first return is set arbitrarily to 0 because there's no
        previous value to compare with."""
        return [0] + [(self.values[i] - self.values[i-1])/self.values[i-1]*100 for i in range(1, len(self.values))]  

    def getOffensiveBenchmark(self, start_day, end_day):
        """The offensive benchmark of the market for a given period is
        calculated as the mean of the market returns, taking into
        account only the days where the market was raising."""
        market_returns = self.returns[start_day:end_day]
        offensive_returns = [r for r in market_returns if r>=0]
        offensive_benchmark = utils.mean(offensive_returns)
        return offensive_benchmark

    def getDefensiveBenchmark(self, start_day, end_day):
        """The defensive benchmark of the market for a given period is
        calculated as the mean of the market returns, taking into
        account only the days where the market was going down."""
        market_returns = self.returns[start_day:end_day]
        defensive_returns = [r for r in market_returns if r<=0]
        defensive_benchmark = utils.mean(defensive_returns)
        return defensive_benchmark

    def getPerformance(self, start_day, end_day):
        """The performance of the market for a given period is
        calculated as the mean of the performances of all stocks in
        the market along the mentioned period."""
        stocks_performances = [s.getPerformance(start_day, end_day) for s in self.stocks]
        return utils.mean(stocks_performances)

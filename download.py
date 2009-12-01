#!/usr/bin/python

import utils
import urllib2

utils.download_sap_tickers()
sap_tickers = utils.get_tickers()

for ticker in sap_tickers:
    try:
        utils.download_historical_daily_data(ticker, 2000, 2009)
    except urllib2.HTTPError:
        print 'data not found for ticker: %s' % ticker

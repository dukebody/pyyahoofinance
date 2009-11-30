#!/usr/bin/python

import utils
import urllib2

sap_tickers = utils.get_tickers()
sap_tickers += [utils.INDEX]

for ticker in sap_tickers:
    try:
        utils.download_historical_daily_data(ticker)
    except urllib2.HTTPError:
        print 'data not found for ticker: %s' % ticker

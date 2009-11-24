#!/usr/bin/python

from utils import *
import urllib2

sap_tickers = get_tickers()[:90] # Standard & Poor's tickers
sap_tickers += [INDEX] # add the index itself too
closes = {}
for ticker in sap_tickers:
    try:
        c = get_closes(ticker)
        closes[ticker] = stringify(c)
    except (urllib2.HTTPError, ValueError): # data for the ticker not found or incomplete
        print "data not found or incomplete for ticker: %s" % ticker

valid_tickers = closes.keys()
columns = [[ticker] + closes[ticker] for ticker in valid_tickers]

rows = zip(*columns)
out = open('results.txt', 'w')
for row in rows:
    out.write(' '.join(row))
    out.write('\n')
out.close()

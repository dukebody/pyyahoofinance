#!/usr/bin/python

from utils import *
import urllib2

sap_tickers = get_tickers()[80:90] # Standard & Poor's tickers
sap_tickers += [INDEX] # add the index itself too

closes = get_closes_from_tickerslist(sap_tickers)

valid_tickers = closes.keys()
columns = [[ticker] + stringify(closes[ticker]) for ticker in valid_tickers]

rows = zip(*columns)
out = open('results.txt', 'w')
for row in rows:
    out.write(' '.join(row))
    out.write('\n')
out.close()

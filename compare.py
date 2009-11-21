#!/usr/bin/python

from utils import *
import urllib2


tickers = get_tickers()
closes = {}
notfound = []

for ticker in tickers:
    try:
        closes[ticker] = get_closes(ticker)
    except urllib2.HTTPError: # closes for given ticker unavailable
        print "data not found for ticker: %s" % ticker
        notfound.append(ticker)


for ticker in notfound:
    tickers.remove(ticker)

index_closes = get_closes(INDEX)

incomplete = []
for ticker in tickers:
    if len(closes[ticker]) != len(index_closes):
        print "incomplete data for ticker: %s" % ticker
        incomplete.append(ticker)
        del closes[ticker]

for ticker in incomplete:
    tickers.remove(ticker)

closes_list = [closes[ticker] for ticker in tickers]
mean_point_acceleration = get_mean_point_accelerations(closes_list, index_closes)


columns = [['index'] + stringify(index_closes)[2:], ['accel'] + stringify(mean_point_acceleration)]
rows = zip(*columns)
out = open('spread.txt', 'w')
for row in rows:
    out.write(' '.join(row))
    out.write('\n')
out.close()


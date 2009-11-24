#!/usr/bin/python

from utils import *
import urllib2


sap_tickers = get_tickers()[80:90]

closes = get_closes_from_tickerslist(sap_tickers)
index_closes = get_closes(INDEX)

valid_tickers = closes.keys()

closes_list = [closes[ticker] for ticker in valid_tickers]
mean_point_acceleration = get_mean_point_accelerations(closes_list, index_closes)


columns = [['index'] + stringify(index_closes)[2:], ['accel'] + stringify(mean_point_acceleration)]
rows = zip(*columns)
out = open('spread.txt', 'w')
for row in rows:
    out.write(' '.join(row))
    out.write('\n')
out.close()


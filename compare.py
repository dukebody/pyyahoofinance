#!/usr/bin/python

from utils import *


tickers = get_tickers()
closes = {}
for ticker in tickers:
    closes[ticker] = get_closes(ticker)
index_closes = get_closes(INDEX)

closes_list = [closes[ticker] for ticker in tickers]
mean_point_acceleration = get_mean_point_accelerations(closes_list, index_closes)


columns = [['index'] + stringify(index_closes)[2:], ['accel'] + stringify(mean_point_acceleration)]
rows = zip(*columns)
out = open('spread.txt', 'w')
for row in rows:
    out.write(' '.join(row))
    out.write('\n')
out.close()


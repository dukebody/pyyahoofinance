#!/usr/bin/python

from utils import *

tickers = get_tickers()[:5]
tickers += [INDEX]
closes = {}
for ticker in tickers:
    closes[ticker] = [str(close) for close in get_closes(ticker)]


columns = [[ticker] + closes[ticker] for ticker in closes.keys()]

rows = zip(*columns)
out = open('results.txt', 'w')
for row in rows:
    out.write(' '.join(row))
    out.write('\n')
out.close()

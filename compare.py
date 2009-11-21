#!/usr/bin/python

from utils import *


tickers = get_tickers()[:5]
closes = {}
for ticker in tickers:
    closes[ticker] = get_closes(ticker)
index_closes = get_closes(INDEX)

closes_list = [closes[ticker] for ticker in tickers]
mean_point_acceleration = get_mean_point_accelerations(closes_list, index_closes)

print mean_point_acceleration

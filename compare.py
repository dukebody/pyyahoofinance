#!/usr/bin/python

from utils import *


tickers = get_tickers()[:5]
closes = {}
for ticker in tickers:
    closes[ticker] = get_closes(ticker)
index_closes = get_closes(INDEX)

acceleration = {}
for ticker in tickers:
    acceleration[ticker] = get_acceleration(closes[ticker], index_closes)


print acceleration


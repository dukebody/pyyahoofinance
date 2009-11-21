import urllib2

CLOSE_COLUMN = 4 # the index of the column containing the close value
TICKER_COLUMN = 0 # the index of the column containing the ticker name
INDEX = '%5EGSPC' # ticker of the index

def get_tickers():
    """Get the Standard & Poor stock tickers."""
    tickers = []
    for n in range(0, 50, 50):
        url = urllib2.urlopen("http://download.finance.yahoo.com/d/quotes.csv?s=@%5EGSPC&f=sl1d1t1c1ohgv&e=.csv&h=PAGE".replace('PAGE', str(n)))
        data = url.read()
        stocks = data.split('\r\n')
        for stock in stocks:
            try:
                ticker = stock.split(',')[TICKER_COLUMN]
                ticker = ticker.replace('"', '') # remove surrounding quotes
                if ticker: # not empty ticker
                    tickers.append(ticker)
            except IndexError: # empty row
                pass

    return tickers


def get_closes(ticker):
    """Return the closing values for the stocks with the ticker
    provided as a list, in the form {'ticker':[value1, value2, ...]}.
    """

    print "getting data from ticker: %s" % ticker
    url = urllib2.urlopen("http://ichart.finance.yahoo.com/table.csv?s=%s&a=00&b=1&c=2000&d=00&e=1&f=2009&g=m&ignore=.csv" % ticker)

    history = url.read()

    measures = history.split('\n')
    measures = measures[1:-1] # the last row is empty and the first
                              # one contains the labels

    closes = [float(measure.split(',')[CLOSE_COLUMN]) for measure in measures]

    return closes


def get_diffs(closes):
    """Return the velocity of the provided closes."""
    period = len(closes)
    diffs = [(closes[i] - closes[i-1])/closes[i]*100 for i in range(1, period)]
    return diffs

def get_deviations(closes, reference_closes):
    """Return the deviations of the given diffs from the given reference."""
    assert len(closes) == len(reference_closes)
    diffs = get_diffs(closes)
    reference_diffs = get_diffs(reference_closes)
    period = len(diffs)
    deviation = [diffs[i] - reference_diffs[i] for i in range(0, period)]
    return deviation

def get_acceleration(closes, reference_closes):
    """Return the acceleration of the given closes."""
    assert len(closes) == len(reference_closes)
    period = len(closes)
    deviation = get_deviations(closes, reference_closes)
    acceleration = [deviation[i] - deviation[i-1] for i in range(1, period-1)]
    return acceleration

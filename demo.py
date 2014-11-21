try:
    # py3
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode
except ImportError:
    # py2
    from urllib2 import Request, urlopen
    from urllib import urlencode
    
    
    
def _request(symbol, stat):
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
    req = Request(url)
    resp = urlopen(req)
    content = resp.read().decode().strip()
    return content
    
def get_quote(symbol):
    ids = 'yl1'
    values = _request(symbol, ids).split(',')
    dividend_yield = values[0]
    spot = values[1]
    print float(dividend_yield) / 2
    print float(spot) / 2
    
a = get_quote('aapl')
print a
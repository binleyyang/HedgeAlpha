from urllib import urlopen
import json

g_bid_call = []
g_ask_call = []
g_mid_call = []
g_strike = []

def googleQuote(ticker):
    url = 'http://www.google.com/finance/option_chain?q=%s&output=json'% ticker
    doc = urlopen(url)
    content = doc.read()
    a = fix_json(content)
    #print a
    quote = json.loads(a)
    print "\n=============================GIVE ME SOME SPACE===============================\n"
    #print quote
    
    puts = quote['puts']
    calls = quote['calls']
    print "PUTS:      ", puts
    print "CALLS:     ", calls
    
    for b in calls:
        if b['b'] == '-' or b['a'] == '-':
            pass
        else:
            g_bid_call.append(float(b['b']))
            g_ask_call.append(float(b['a']))
            g_strike.append(float(b['strike']))
            bid = float(b['b'])
            ask = float(b['a'])
            mid = (bid + ask) / 2
            g_mid_call.append(mid)
    return quote
    
def fix_json(k):
    q=['cid','cp','s','cs','vol','expiry','underlying_id','underlying_price',
     'p','c','oi','e','b','strike','a','name','puts','calls','expirations',
     'y','m','d']
 
    for i in q:
        try:    
            k=k.replace('{%s:'%i,'{"%s":'%i)
            k=k.replace(',%s:'%i,',"%s":'%i)
        except: pass
 
    return k
if __name__ == "__main__":
    ticker = 'spy'
    googleQuote(ticker)

    print g_bid_call
    print g_ask_call
    print g_mid_call
    #print googleQuote(ticker)
    
    
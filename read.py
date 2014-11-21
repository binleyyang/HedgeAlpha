import urllib2
import requests
import json
 
 
def get_opt_quote(ticker_symbol):
    chain = []
    url = 'http://www.google.com/finance/option_chain?q=%s&output=json' % (ticker_symbol)
    lines = urllib2.urlopen(url).read()
    k = fix_json(lines)
 
    opts = eval(k)
    exp = opts['expirations']
    for expiry in exp:
        y = expiry['y']
        m = expiry['m']
        d = expiry['d']
 
        url = 'http://www.google.com/finance/option_chain?q=%s&output=json&expy=%s&expm=%s&expd=%s'%(ticker_symbol,y,m,d)
        lines = fix_json(urllib2.urlopen(url).read())
         
        chain.append(eval(lines))
 
    return chain

 
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
 
quote = get_opt_quote('spy')
print quote
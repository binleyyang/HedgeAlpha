from urllib import urlopen
import json
 
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
    
    for b in puts:
        print b['strike']
        
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
    #print googleQuote(ticker)
    
    
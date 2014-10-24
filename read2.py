from urllib import urlopen
import json
 
def googleQuote(ticker):
    url = 'http://www.google.com/finance/option_chain?q=%s&output=json'% ticker
    doc = urlopen(url)
    content = fix_json(doc.read())
    quote = json.loads(content)
    json_string = json.dumps(content,sort_keys=True,indent=2)
    #print json_string
    parent = quote["expiry"]
    for item in parent:
        print item[0]
    #quote = float(content[0][0])
    return parent
    
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
    print googleQuote(ticker)
    
    
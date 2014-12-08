import datetime
import math
import urllib2
import array

urlToVisit = "http://ichart.finance.yahoo.com/table.csv?s="
start = datetime.date(2014, 11, 7)
end = datetime.date.today()
q = float()
spot = float()
HVol = float()

adjclose = [] 
date = []
opent = []
high = []
low = []
close = []
volume = []
expirys = []
logreturns = []
variancecalcs = [] 

try:
    # py3
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode
except ImportError:
    # py2
    from urllib2 import Request, urlopen
    from urllib import urlencode


def option_price_call_american_binomial(S, K, r, sigma, t, steps): 
    """American Option (Call) using binomial approximations
    Converted to Python from "Financial Numerical Recipes in C" by:
    Bernt Arne Odegaard
    http://finance.bi.no/~bernt/gcc_prog/index.html
    @param S: spot (underlying) price
    @param K: strike (exercise) price,
    @param r: interest rate
    @param sigma: volatility 
    @param t: time to maturity 
    @param steps: Number of steps in binomial tree
    @return: Option price
    """
    R = math.exp(r*(t/steps))       
    Rinv = 1.0/R                 
    u = math.exp(sigma*math.sqrt(t/steps)) 
    d = 1.0/u
    p_up = (R-d)/(u-d)
    p_down = 1.0-p_up
    prices = array.array('d', (0 for i in range(0,steps+1))) # price of underlying
    prices[0] = S*pow(d, steps) # fill in the endnodes.
    uu = u*u
    
    for i in xrange(1, steps+1):
        prices[i] = uu*prices[i-1]
 
    call_values = array.array('d', (0 for i in range(0,steps+1))) # value of corresponding call
    for i in xrange(0, steps+1):
        call_values[i] = max(0.0, (prices[i]-K)) # call payoffs at maturity

    for step in xrange(steps-1, -1, -1):
        for i in xrange(0, step+1):
            call_values[i] = (p_up*call_values[i+1]+p_down*call_values[i])*Rinv
            prices[i] = d*prices[i+1]
            call_values[i] = max(call_values[i],prices[i]-K) # check for exercise
    return call_values[0]


def option_price_put_american_binomial(S, K, r, sigma, t, steps):
    """American Option (Put) using binomial approximations
    Converted to Python from "Financial Numerical Recipes in C" by:
    Bernt Arne Odegaard
    http://finance.bi.no/~bernt/gcc_prog/index.html
    @param S: spot (underlying) price
    @param K: strike (exercise) price,
    @param r: interest rate
    @param sigma: volatility 
    @param t: time to maturity 
    @param steps: Number of steps in binomial tree
    @return: Option price
    """ 
    R = math.exp(r*(t/steps)) # interest rate for each step
    Rinv = 1.0/R # inverse of interest rate
    u = math.exp(sigma*math.sqrt(t/steps)) # up movement
    uu = u*u
    d = 1.0/u
    p_up = (R-d)/(u-d)
    p_down = 1.0-p_up
    prices = array.array('d', (0 for i in range(0,steps+1))) # price of underlying
    prices[0] = S*pow(d, steps) 
    
    for i in xrange(1, steps+1):
        prices[i] = uu*prices[i-1]

    put_values = array.array('d', (0 for i in range(0,steps+1))) # value of corresponding put

    for i in xrange(0, steps+1):
        put_values[i] = max(0.0, (K-prices[i])) # put payoffs at maturity

    for step in xrange(steps-1, -1, -1):
        for i in xrange(0, step+1):
            put_values[i] = (p_up*put_values[i+1]+p_down*put_values[i])*Rinv
            prices[i] = d*prices[i+1]
            put_values[i] = max(put_values[i],(K-prices[i])) # check for exercise
    return put_values[0]

def option_price_call_american_discrete_dividends_binomial(S, K, r, sigma, t, steps, dividend_times, dividend_amounts):
    """American Option (Call) for dividends with specific (discrete) dollar amounts 
    using binomial approximations
    Converted to Python from "Financial Numerical Recipes in C" by:
    Bernt Arne Odegaard
    http://finance.bi.no/~bernt/gcc_prog/index.html
    @param S: spot (underlying) price
    @param K: strike (exercise) price,
    @param r: interest rate
    @param sigma: volatility 
    @param t: time to maturity 
    @param steps: Number of steps in binomial tree
    @param dividend_times: Array of dividend times. (Ex: [0.25, 0.75] for 1/4 and 3/4 of a year)
    @param dividend_amounts: Array of dividend amounts for the 'dividend_times'
    @return: Option price
    """
    no_dividends = len(dividend_times)
    if (no_dividends==0): 
        return option_price_call_american_binomial(S,K,r,sigma,t,steps) # just do regular
    steps_before_dividend = (int)(dividend_times[0]/t*steps)
    R = math.exp(r*(t/steps))
    Rinv = 1.0/R
    u = math.exp(sigma*math.sqrt(t/steps))
    d = 1.0/u
    pUp = (R-d)/(u-d)
    pDown = 1.0 - pUp
    dividend_amount = dividend_amounts[0]
    tmp_dividend_times = array.array('d', (0 for i in range(0,no_dividends-1))) # temporaries with 
    tmp_dividend_amounts = array.array('d', (0 for i in range(0,no_dividends-1))) # one less dividend 
    for i in xrange(0, no_dividends-1):
        tmp_dividend_amounts[i] = dividend_amounts[i+1]
        tmp_dividend_times[i]   = dividend_times[i+1] - dividend_times[0]
     
    prices = array.array('d', (0 for i in range(0,steps_before_dividend+1)))
    call_values = array.array('d', (0 for i in range(0,steps_before_dividend+1)))
    prices[0] = S*pow(d, steps_before_dividend)
    
    for i in xrange(1, steps_before_dividend+1):
        prices[i] = u*u*prices[i-1]

    for i in xrange(0, steps_before_dividend+1):
        value_alive = option_price_call_american_discrete_dividends_binomial(prices[i]-dividend_amount,K, r, sigma,
                                     t-dividend_times[0], # time after first dividend
                                     steps-steps_before_dividend, 
                                     tmp_dividend_times,
                                     tmp_dividend_amounts)
        call_values[i] = max(value_alive,(prices[i]-K)) # compare to exercising now

    for step in xrange(steps_before_dividend-1, -1, -1):
        for i in xrange(0, step+1):
            prices[i] = d*prices[i+1]
            call_values[i] = (pDown*call_values[i]+pUp*call_values[i+1])*Rinv
            call_values[i] = max(call_values[i], prices[i]-K)

    return call_values[0]


def option_price_put_american_discrete_dividends_binomial(S, K, r, sigma, t, steps, dividend_times, dividend_amounts): 
    """American Option (Put) for dividends with specific (discrete) dollar amounts 
    using binomial approximations.
    Converted to Python from "Financial Numerical Recipes in C" by:
    Bernt Arne Odegaard
    http://finance.bi.no/~bernt/gcc_prog/index.html
    @param S: spot (underlying) price
    @param K: strike (exercise) price,
    @param r: interest rate
    @param sigma: volatility 
    @param t: time to maturity 
    @param steps: Number of steps in binomial tree
    @param dividend_times: Array of dividend times. (Ex: [0.25, 0.75] for 1/4 and 3/4 of a year)
    @param dividend_amounts: Array of dividend amounts for the 'dividend_times'
    @return: Option price
    """
    
    # given an amount of dividend, the binomial tree does not recombine, have to 
    # start a new tree at each ex-dividend date.
    # do this recursively, at each ex dividend date, at each step, put the 
    # binomial formula starting at that point to calculate the value of the live
    # option, and compare that to the value of exercising now.

    no_dividends = len(dividend_times)
    if (no_dividends == 0): # just take the regular binomial 
        return option_price_put_american_binomial(S,K,r,sigma,t,steps)
    steps_before_dividend = (int)(dividend_times[0]/t*steps);
   
    R = math.exp(r*(t/steps))
    Rinv = 1.0/R
    u = math.exp(sigma*math.sqrt(t/steps))
    uu= u*u
    d = 1.0/u
    pUp = (R-d)/(u-d)
    pDown = 1.0 - pUp
    dividend_amount = dividend_amounts[0]
    
    tmp_dividend_times = array.array('d', (0 for i in range(0,no_dividends-1))) # temporaries with 
    tmp_dividend_amounts = array.array('d', (0 for i in range(0,no_dividends-1))) # one less dividend 
    for i in xrange(0, no_dividends-1): 
        tmp_dividend_amounts[i] = dividend_amounts[i+1]
        tmp_dividend_times[i]= dividend_times[i+1] - dividend_times[0]

    prices = array.array('d', (0 for i in range(0,steps_before_dividend+1)))
    put_values = array.array('d', (0 for i in range(0,steps_before_dividend+1)))
    prices[0] = S*pow(d, steps_before_dividend)
    
    for i in xrange(1, steps_before_dividend+1):
        prices[i] = uu*prices[i-1]
        
    for i in xrange(0, steps_before_dividend+1):
        value_alive = option_price_put_american_discrete_dividends_binomial(
                    prices[i]-dividend_amount, K, r, sigma, 
                    t-dividend_times[0], # time after first dividend
                    steps-steps_before_dividend, 
                    tmp_dividend_times, tmp_dividend_amounts)  
        # what is the value of keeping the option alive?  Found recursively, 
        # with one less dividend, the stock price is current value 
        # less the dividend.
        put_values[i] = max(value_alive,(K-prices[i])) # compare to exercising now

    for step in xrange(steps_before_dividend-1, -1, -1):
        for i in xrange(0, step+1):
            prices[i] = d*prices[i+1]
            put_values[i] = (pDown*put_values[i]+pUp*put_values[i+1])*Rinv
            put_values[i] = max(put_values[i], K-prices[i]) # check for exercise
            
    return put_values[0]


def option_price_call_american_proportional_dividends_binomial(S, K, r, sigma, 
                            time, no_steps, dividend_times, dividend_yields):
    """American Option (Call) with proportional dividend payments 
    using binomial approximations.
    Converted to Python from "Financial Numerical Recipes in C" by:
    Bernt Arne Odegaard
    http://finance.bi.no/~bernt/gcc_prog/index.html
    @param S: spot (underlying) price
    @param K: strike (exercise) price,
    @param r: interest rate
    @param sigma: volatility 
    @param time: time to maturity 
    @param no_steps: Number of steps in binomial tree
    @param dividend_times: Array of dividend times. (Ex: [0.25, 0.75] for 1/4 and 3/4 of a year)
    @param dividend_yields: Array of dividend yields for the 'dividend_times'
    @return: Option price
    """
    # note that the last dividend date should be before the expiry date, problems if dividend at terminal node
    no_dividends=len(dividend_times)
    if (no_dividends == 0):
        return option_price_call_american_binomial(S,K,r,sigma,time,no_steps) # price w/o dividends

    delta_t = time/no_steps
    R = exp(r*delta_t)
    Rinv = 1.0/R
    u = exp(sigma*math.sqrt(delta_t))
    uu= u*u
    d = 1.0/u
    pUp = (R-d)/(u-d)
    pDown = 1.0 - pUp
    dividend_steps = array.array('d', (0 for i in range(0,no_dividends))) # when dividends are paid
    
    for i in xrange(0, no_dividends): 
        dividend_steps[i] = (int)(dividend_times[i]/time*no_steps)
    
    prices = array.array('d', (0 for i in range(0,no_steps+1)))
    call_prices = array.array('d', (0 for i in range(0,no_steps+1)))
    prices[0] = S*pow(d, no_steps)# adjust downward terminal prices by dividends
    
    for i in xrange(0, no_dividends):
        prices[0]*=(1.0-dividend_yields[i])

    for i in xrange(1, no_steps+1):
        prices[i] = uu*prices[i-1]
 
    for i in xrange(1, no_steps+1):
        call_prices[i] = max(0.0, (prices[i]-K))

    for step in xrange(no_steps-1, -1, -1):
        for i in xrange(0, no_dividends): # check whether dividend paid      
            if (step==dividend_steps[i]): 
                for j in xrange(0, step+2):
                    prices[j]*=(1.0/(1.0-dividend_yields[i]))
        for i in xrange(0, step+1):            
            call_prices[i] = (pDown*call_prices[i]+pUp*call_prices[i+1])*Rinv
            prices[i] = d*prices[i+1]
            call_prices[i] = max(call_prices[i], prices[i]-K) #check for exercise

    return call_prices[0]


def option_price_put_american_proportional_dividends_binomial(S, K, r, sigma, 
                            time, no_steps, dividend_times, dividend_yields):
    """American Option (Put) with proportional dividend payments 
    using binomial approximations.
    Converted to Python from "Financial Numerical Recipes in C" by:
    Bernt Arne Odegaard
    http://finance.bi.no/~bernt/gcc_prog/index.html
    @param S: spot (underlying) price
    @param K: strike (exercise) price,
    @param r: interest rate
    @param sigma: volatility 
    @param time: time to maturity 
    @param no_steps: Number of steps in binomial tree
    @param dividend_times: Array of dividend times. (Ex: [0.25, 0.75] for 1/4 and 3/4 of a year)
    @param dividend_yields: Array of dividend yields for the 'dividend_times'
    @return: Option price
    """
    
    # when one assume a dividend yield, the binomial tree recombines 
    # note that the last dividend date should be before the expiry date
    no_dividends=len(dividend_times);
    if (no_dividends == 0): # just take the regular binomial 
        return option_price_put_american_binomial(S,K,r,sigma,time,no_steps)
    
    R = exp(r*(time/no_steps))
    Rinv = 1.0/R
    u = exp(sigma*math.sqrt(time/no_steps))
    uu= u*u
    d = 1.0/u
    pUp   = (R-d)/(u-d)
    pDown = 1.0 - pUp
    dividend_steps = array.array('d', (0 for i in range(0,no_dividends))) # when dividends are paid
    
    for i in xrange(0, no_dividends):
        dividend_steps[i] = (int)(dividend_times[i]/time*no_steps);

    prices = array.array('d', (0 for i in range(0,no_steps+1)))
    put_prices = array.array('d', (0 for i in range(0,no_steps+1)))
    prices[0] = S*pow(d, no_steps);
    
    for i in xrange(0, no_dividends):
        prices[0]*=(1.0-dividend_yields[i])

    for i in xrange(1, no_steps+1):
        prices[i] = uu*prices[i-1] #terminal tree nodes

    for i in xrange(1, no_steps+1):
        put_prices[i] = max(0.0, (K-prices[i]))

    for step in xrange(no_steps-1, -1, -1):
        for i in xrange(0, no_dividends): # check whether dividend paid
            if (step==dividend_steps[i]):
                for j in xrange(0, step+2):
                    prices[j]*=(1.0/(1.0-dividend_yields[i]))
        for i in xrange(0, step+1): 
            prices[i] = d*prices[i+1]
            put_prices[i] = (pDown*put_prices[i]+pUp*put_prices[i+1])*Rinv
            put_prices[i] = max(put_prices[i], K-prices[i]) # check for exercise

    return put_prices[0]

def pullData(stock):
    try: 
        print "Currently pulling", stock
        stockUrl = makeUrl(stock, start, end)
        stockFile = []
        try:
            sourceCode = urllib2.urlopen(stockUrl).read()
            splitSource = sourceCode.split('\n')
            
            for eachLine in splitSource:
                splitLine = eachLine.split(',')
                if len(splitLine) == 7:
                    if 'values' not in eachLine:
                        stockFile.append(eachLine)
        except Exception, e:
            print str(e), 'failed to organize pulled data'
    except Exception, e:
        print str(e), 'failed to pull stock historical data'
        
    try:
        for line in stockFile:
            s = line.split(',')

            if s[0] == 'Date' or s[1] == 'Open' or s[2] == 'High' or s[3] == 'Low' or s[4] == 'Close' or s[5] == 'Volume' or s[6] == 'Adj Close':
                pass
            else:
                date_obj = datetime.datetime.strptime(s[0], '%Y-%m-%d').date()
                date.append(date_obj)
                opent.append(s[1])
                high.append(s[2])
                low.append(s[3])
                close.append(s[4])
                low.append(s[5])
                adjclose.append(s[6])
    except Exception, e:
        print str(e), 'error'
    logreturn(adjclose)
    variancecalc(logreturns)
    annualvol(stdev(varianceaverage(variancecalcs)))

def logreturn(adjclose):
    i = 0
    while i < len(adjclose) - 1:
        x = math.log(float(adjclose[i])/float(adjclose[i+1]))
        global logreturns
        logreturns.append(x)
        i += 1
        print 'fuck'
        
def averagelog(logreturns):
    sum = 0
    counter = 0
    i = 0
    while i < len(logreturns) - 1:
        y = logreturns[i]
        sum += y
        counter += 1
        i += 1
    x = sum / counter
    return x
    
def variancecalc(logreturns):
    i = 0
    avg = averagelog(logreturns)
    while i < len(logreturns) - 1:
        y = logreturns[i]
        yprime = y - avg
        global variancecalcs
        variancecalcs.append(math.pow(yprime, 2))
        i += 1

def varianceaverage(variancecalc):
    sum = 0
    counter = 0
    i = 0
    while i < len(variancecalc) - 1:
        y = variancecalc[i]
        sum += y
        counter += 1
        i += 1
    #counter should be n-1 to get an unbiased estimate
    x = sum / (len(variancecalc) - 1)
    #print "**********************************"
    #print "VarAvrg:", x
    return x


def stdev(varianceAvrg):
    return math.sqrt(varianceAvrg)


def annualvol(stdev):
    annualvol = math.sqrt(252) * stdev
    global HVol 
    HVol = annualvol
    # #this should add historial vols by month in sequence
    # return annualvol
    
def annualvol2(stdev):
    return math.sqrt(daysToMaturityPrime) * stdev


def makeUrl(stock, start, end):
    a = start
    b = end
    dateUrl = '%s&a=%d&b=%d&c=%d&d=%d&e=%d&f=%d&g=d&ignore=.csv'% (stock, a.month-1, a.day, a.year, b.month-1, b.day, b.year)
    return urlToVisit+dateUrl

def get_quote(symbol):
    ids = 'yl1'
    values = _request(symbol, ids).split(',')
    global q
    global spot

    q = float(values[0]) / 100 
    spot = float(values[1])

def _request(symbol, stat):
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
    req = Request(url)
    resp = urlopen(req)
    content = resp.read().decode().strip()
    return content

while True:
    stock = raw_input('Stock to pull: >>')
    get_quote(stock)
    pullData(stock)
    #march 20 2015 put option 
    print spot
    print HVol
    print(option_price_put_american_binomial(spot, 125.00, 0.0016, HVol, 102, 25))
    # spotVar = raw_input:('spotPrice :? >>')
    # strikeVar = raw_input('strikePrice :? >>')
    # dayVar = raw_input:('dayToExpiry :? >>')

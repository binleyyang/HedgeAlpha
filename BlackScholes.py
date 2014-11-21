import math

logreturns = []
variancecalcs = [] 
annualvolprime = float()
annualvolprime1 = []
pi = 3.14159265358979 

daysToMaturityPrime = float()
rate = .0015
q = float()
spot = float()
#strike = float()
#realOptionPrice = float()

puts_impliedvols = []
calls_impliedvols = []
months = []

adjclose = [] 
date = []
opent = []
high = []
low = []
close = []
volume = []

def timeToMaturity(year, month, day):
    maturityDate = datetime.date(year, month, day)
    difference = maturityDate - end
    global daysToMaturityPrime
    daysToMaturityPrime = (difference.total_seconds() / (3600 * 24))
    return daysToMaturityPrime
        
def OptionPrice(spot, strike, NbExp, vol, rate, q, optionType):
    # v = float()
    d1 = float()
    d2 = float()
    Nd1 = float()
    Nd2 = float()
    T = float()
        
    if NbExp < 0:
        return 0
    T = NbExp / 365
    if NbExp == 0:
        if optionType == "c":
            print "TESTTESTTESTTEST", long((math.max(spot - strike, 0)))
            return float((math.max(spot - strike, 0)))
        else:
            print "TESTTESTTESTTEST", long((math.max(spot - strike, 0)))
            return float((math.max(strike - spot, 0)))
    
    d1 = ((math.log(spot / strike)) + (rate - q + (vol * vol) / 2) * T) / (vol * math.sqrt(T))
    d2 = d1 - vol * math.sqrt(T)
    Nd1 = cdnf(d1)
    Nd2 = cdnf(d2)
    if optionType == "c":
        # call option
        return float((spot * math.exp(-q * T) * Nd1 - strike * math.exp(-rate * T) * Nd2))
    else:
        # put option
        return float((-spot * math.exp(-q * T) * (1 - Nd1) + strike * math.exp(-rate * T) * (1 - Nd2)))
  
def greeks(spot, strike, NbExp, vol, rate, q, optionType):
    dS = float()
    dv = float()
    dr = float()
    dt = float()
    delta = float()
    gamma = float()
    vega = float()
    theta = float()
    rho = float()
    dS = 0.01
    # 0.01 point move in spot
    dv = 0.0001
    # 0.01% move in vol
    dt = 1
    # 1 day
    dr = 0.0001
    # 1bps move
    if NbExp < 0:
        # print "TESTTESTTESTTEST";
        return 0
    #x = float((cls.OptionPrice(spot + dS, strike, NbExp, vol, rate, q, optionType)))
    #x2 = float(cls.OptionPrice(spot - dS, strike, NbExp, vol, rate, q, optionType))
    # print x;
    # print x2;
    # print dS;
    # print (x-x2)/(2*dS);
    delta = float(((OptionPrice(spot + dS, strike, NbExp, vol, rate, q, optionType) - OptionPrice(spot - dS, strike, NbExp, vol, rate, q, optionType)) / (2 * dS)))
    gamma = float(((OptionPrice(spot + dS, strike, NbExp, vol, rate, q, optionType) - 2 * OptionPrice(spot, strike, NbExp, vol, rate, q, optionType) + OptionPrice(spot - dS, strike, NbExp, vol, rate, q, optionType)) / (dS * dS)))
    vega = float(((OptionPrice(spot, strike, NbExp, vol + dv, rate, q, optionType) - OptionPrice(spot, strike, NbExp, vol - dv, rate, q, optionType)) / (2 * dv) / 100))
    rho = float(((OptionPrice(spot, strike, NbExp, vol, rate + dr, q, optionType) - OptionPrice(spot, strike, NbExp, vol, rate - dr, q, optionType)) / (2 * dr) / 1000))
    if NbExp == 0:
        # print "TESTTESTTESTTEST";
        theta = 0
    else:
        theta = float(((OptionPrice(spot, strike, NbExp - dt, vol, rate, q, optionType) - OptionPrice(spot, strike, NbExp + dt, vol, rate, q, optionType)) / (2 * dt)))
    print "delta: ", delta
    print "gamma: ", gamma
    print "vega:  ", vega
    print "rho>:  ", rho
    print "theta: ", theta
    return 0
                 
def cdnf(x):
    neg = 1 if (x < 0) else 0
    if neg == 1:
        x *= -1
    k = (1 / (1 + 0.2316419 * x))
    y = ((((1.330274429 * k - 1.821255978) * k + 1.781477937) * k - 0.356563782) * k + 0.319381530) * k
    y = 1.0 - 0.398942280401 * math.exp(-0.5 * x * x) * y
    return (1 - neg) * y + neg * (1 - y)
        
def logreturn(adjclose):
    i = 0
    while i < len(adjclose) - 1:
        x = math.log(float(adjclose[i])/float(adjclose[i+1]))
        global logreturns
        logreturns.append(x)
        i += 1
        
def averagelog(logreturns):
    print len(logreturns)
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
    global annualvolprime 
    annualvolprime = annualvol
    #this should add historial vols by month in sequence
    annualvolprime1.append(annualvol)
    return annualvol
    
def annualvol2(stdev):
    return math.sqrt(daysToMaturityPrime) * stdev
    
def calls_annualvolimplied(modelOption, realOption, strike, optionType):
        volimplied = stdev(varianceaverage(variancecalcs))
        calls_annualvolimplied = 0
        real = realOption
        model = modelOption
        if real == model:
            calls_annualvolimplied = annualvol2(volimplied)
        elif real > model:
            while (real > model):
                volimplied += 0.00001
                model = OptionPrice(spot, strike, daysToMaturityPrime, annualvol2(volimplied), rate, q, optionType)
                calls_annualvolimplied = annualvol2(volimplied)
                #print 'real > model', calls_annualvolimplied
                if calls_annualvolimplied < 0:
                    print 'ERROR: OUT OF THE MONEY'
                    break
        else:
            while (real < model):
                volimplied -= 0.00001
                model = OptionPrice(spot, strike, daysToMaturityPrime, annualvol2(volimplied), rate, q, optionType)
                calls_annualvolimplied = annualvol2(volimplied)
                #print 'real < model', calls_annualvolimplied
                if calls_annualvolimplied < 0:
                    print 'ERROR: OUT OF THE MONEY'
                    break
              
        calls_impliedvols.append(calls_annualvolimplied)
        return calls_annualvolimplied

def puts_annualvolimplied(modelOption, realOption, strike, optionType):
        volimplied = stdev(varianceaverage(variancecalcs))
        puts_annualvolimplied = 0
        real = realOption
        model = modelOption
        if real == model:
            puts_annualvolimplied = annualvol2(volimplied)
        elif real > model:
            while (real > model):
                volimplied += 0.00001
                model = OptionPrice(spot, strike, daysToMaturityPrime, annualvol2(volimplied), rate, q, optionType)
                puts_annualvolimplied = annualvol2(volimplied)
                #print 'real > model', calls_annualvolimplied
                if puts_annualvolimplied < 0:
                    print 'ERROR: OUT OF THE MONEY'
                    break
        else:
            while (real < model):
                volimplied -= 0.00001
                model = OptionPrice(spot, strike, daysToMaturityPrime, annualvol2(volimplied), rate, q, optionType)
                puts_annualvolimplied = annualvol2(volimplied)
                #print 'real < model', calls_annualvolimplied
                if puts_annualvolimplied < 0:
                    print 'ERROR: OUT OF THE MONEY'
                    break
             
        puts_impliedvols.append(puts_annualvolimplied)
        return puts_annualvolimplied
        
def run(adjclose):
    logreturn(adjclose)
    variancecalc(logreturns)
    annualvol(stdev(varianceaverage(variancecalcs)))
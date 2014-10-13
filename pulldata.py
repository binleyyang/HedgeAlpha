import urllib2
import datetime
import math
import numpy as np
import matplotlib.pyplot as plt

logreturns = []
variancecalcs = [] 
annualvolprime = float()
annualvolprime1 = []
pi = 3.14159265358979 

daysToMaturityPrime = float()
rate = float()
q = float()
spot = float()
strike = float()
realOptionPrice = float()

impliedvols = []
months = []

adjclose = [] 
date = []
opent = []
high = []
low = []
close = []
volume = []

urlToVisit = "http://ichart.finance.yahoo.com/table.csv?s="
start = datetime.date(2014, 1, 1)
end = datetime.date.today()

def makeUrl(stock, start, end):
    a = start
    b = end
    dateUrl = '%s&a=%d&b=%d&c=%d&d=%d&e=%d&f=%d&g=d&ignore=.csv'% (stock, a.month-1, a.day, a.year, b.month-1, b.day, b.year)
    return urlToVisit+dateUrl

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
        
    index = 0
    adjclose_1 = [] 
    adjclose_2 = []
    adjclose_3 = []
    adjclose_4 = []
    adjclose_5 = []
    adjclose_6 = []
    adjclose_7 = []
    adjclose_8 = []
    adjclose_9 = []
    adjclose_10 = []
    adjclose_11 = []
    adjclose_12 = []
    
    #sort adjclose data by months
    while index < len(date):        
        if date[index].month == 1:
            adjclose_1.append(adjclose[index])
        if date[index].month == 2:
            adjclose_2.append(adjclose[index])
        if date[index].month == 3:
            adjclose_3.append(adjclose[index])
        if date[index].month == 4:
            adjclose_4.append(adjclose[index])
        if date[index].month == 5:
            adjclose_5.append(adjclose[index])
        if date[index].month == 6:
            adjclose_6.append(adjclose[index])
        if date[index].month == 7:
            adjclose_7.append(adjclose[index])
        if date[index].month == 8:
            adjclose_8.append(adjclose[index])
        if date[index].month == 9:
            adjclose_9.append(adjclose[index])
        if date[index].month == 10:
            adjclose_10.append(adjclose[index])
        if date[index].month == 11:
            adjclose_11.append(adjclose[index])
        if date[index].month == 12:
            adjclose_12.append(adjclose[index])
        index += 1
    
    print '\n----------------------------Volatilites for options with', daysToMaturityPrime, 'days to maturity----------------------------'
    if len(adjclose_1) > 0:
        print '\nJanuary:'
        months.append(1)
        impliedVolByMonth(adjclose_1)
    if len(adjclose_2) > 0:
        months.append(2)
        print '\nFeburary:'
        impliedVolByMonth(adjclose_2)
    if len(adjclose_3) > 0:
        months.append(3)
        print '\nMarch:'
        impliedVolByMonth(adjclose_3)
    if len(adjclose_4) > 0:
        months.append(4)
        print '\nApril:'
        impliedVolByMonth(adjclose_4)
    if len(adjclose_5) > 0:
        months.append(5)
        print '\nMay:'
        impliedVolByMonth(adjclose_5)
    if len(adjclose_6) > 0:
        months.append(6)
        print '\nJune:'
        impliedVolByMonth(adjclose_6)
    if len(adjclose_7) > 0:
        months.append(7)
        print '\nJuly:'
        impliedVolByMonth(adjclose_7)
    if len(adjclose_8) > 0:
        print '\nAugust:'
        months.append(8)
        impliedVolByMonth(adjclose_8)
    if len(adjclose_9) > 0:
        months.append(9)
        print '\nSeptember:'
        impliedVolByMonth(adjclose_9)
    if len(adjclose_10) > 0:
        months.append(10)
        print '\nOctober:'
        impliedVolByMonth(adjclose_10)
    if len(adjclose_11) > 0:
        months.append(11)
        print '\nNovember:'
        impliedVolByMonth(adjclose_11)
    if len(adjclose_12) > 0:
        months.append(12)
        print '\nDecember:'
        impliedVolByMonth(adjclose_12)
    
    #for i in months, impliedvols:
    #    print i
        
    #i = 0
    #while i < len(impliedvols):
    #    print 'before log', impliedvols[i]
    #    impliedvols[i] = math.fabs(math.log(impliedvols[i]))
    #    print 'after log', impliedvols[i]  
    #    i += 1      
    #    
    #print ''
    #j = 0
    #while j < len(annualvolprime1):
    #    print 'before log', annualvolprime1[j]
    #    annualvolprime1[j] = math.fabs(math.log(annualvolprime1[j]))
    #    print 'after log', annualvolprime1[j]  
    #    j += 1 
    
    plt.grid(True)
    plt.plot(months, impliedvols)
    plt.plot(months, annualvolprime1)
    plt.title('Volatilities vs. Time')
    plt.xlabel('Months')
    plt.ylabel('Volatilities')
    #plt.yticks(np.arange(min(impliedvols), max(impliedvols+1), .001))
    plt.legend(['Implied Vols', 'Historical Vols'], loc='upper left')
    plt.show()
    

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
    sum = 0
    counter = 0
    i = 0
    while i < len(logreturns):
        y = logreturns[i]
        sum += y
        counter += 1
        i += 1
    x = sum / counter
    return x
    
def variancecalc(logreturns):
    i = 0
    while i < len(logreturns) - 1:
        y = logreturns[i]
        yprime = y - averagelog(logreturns)
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
    x = sum / counter
    #print "**********************************"
    #print "VarAvrg:", x
    return x


def stdev(varianceAvrg):
    x = math.sqrt(varianceAvrg)
    #print "Stdev:", x
    return x


def annualvol(stdev):
    annualvol = math.sqrt(252) * stdev
    #print "AnnualVol:", annualvol
    global annualvolprime 
    annualvolprime = annualvol
    #this should add historial vols by month in sequence
    annualvolprime1.append(annualvol)
    return annualvol
    
def annualvol2(stdev):
    return math.sqrt(252) * stdev
    
def annualvolimplied(modelOption, realOption):
        volimplied = stdev(varianceaverage(variancecalcs))
        annualvolimplied = 0
        real = realOption
        model = modelOption
        if real == model:
            annualvolimplied = annualvol2(volimplied)
        elif real > model:
            while (real > model):
                volimplied += 0.00001
                model = OptionPrice(spot, strike, daysToMaturityPrime, annualvol2(volimplied), rate, q, "c")
                annualvolimplied = annualvol2(volimplied)
                if annualvolimplied < 0:
                    print 'ERROR: OUT OF THE MONEY'
                    break
        else:
            while (real < model):
                volimplied -= 0.00001
                model = OptionPrice(spot, strike, daysToMaturityPrime, annualvol2(volimplied), rate, q, "c")
                annualvolimplied = annualvol2(volimplied)
                if annualvolimplied < 0:
                    print 'ERROR: OUT OF THE MONEY'
                    break
        
        # this should add implied vols by month in sequence        
        impliedvols.append(annualvolimplied)
        return annualvolimplied
        
def impliedVolByMonth(adjclose):
    #sum = 0
    #count = 0
    #for i in adjclose:
    #    sum += float(i)
    #    count += 1
    #
    #average = sum / count
    
    logreturn(adjclose)
    variancecalc(logreturns)
    annualvol(stdev(varianceaverage(variancecalcs)))
    
    option = OptionPrice(spot, strike, daysToMaturityPrime, annualvolprime, rate, q, "c")
    print "Price of Call: $", option
    
    impliedvol = annualvolimplied(option, realOptionPrice)
    
    #print "Average of adjclose:                     ", average
    print "Historical annual volalitility for Call: ", annualvolprime
    print "Implied annual volalitity for Call:      ", impliedvol
        
while True:
    stock = raw_input('Stock to pull: ')
    spot = float(raw_input('Spot: '))
    strike = float(raw_input('Strike: '))
    realOptionPrice = float(raw_input('Real Option Price: '))
    daysToMaturityPrime = float(raw_input('Days to Maturity: '))
    rate = float(raw_input('Risk-free Rate: '))
    q = float(raw_input('Div/yield: '))
    
    pullData(stock)
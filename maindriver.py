import datetime
import math
import urllib2

class maindriver(object):
    dates = [] 
    logreturns = []
    averagelogs = [] 
    variancecalcs = [] 
    annualvolprime = float()
    pi = 3.14159265358979
    annualvolprimeimplied = float()           

    @classmethod
    def OptionPrice(cls, spot, strike, NbExp, vol, rate, q, optionType):
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
        Nd1 = cls.cdnf(d1)
        Nd2 = cls.cdnf(d2)
        if optionType == "c":
            # call option
            return float((spot * math.exp(-q * T) * Nd1 - strike * math.exp(-rate * T) * Nd2))
        else:
            # put option
            return float((-spot * math.exp(-q * T) * (1 - Nd1) + strike * math.exp(-rate * T) * (1 - Nd2)))

    @classmethod
    def greeks(cls, spot, strike, NbExp, vol, rate, q, optionType):
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
        delta = float(((cls.OptionPrice(spot + dS, strike, NbExp, vol, rate, q, optionType) - cls.OptionPrice(spot - dS, strike, NbExp, vol, rate, q, optionType)) / (2 * dS)))
        gamma = float(((cls.OptionPrice(spot + dS, strike, NbExp, vol, rate, q, optionType) - 2 * cls.OptionPrice(spot, strike, NbExp, vol, rate, q, optionType) + cls.OptionPrice(spot - dS, strike, NbExp, vol, rate, q, optionType)) / (dS * dS)))
        vega = float(((cls.OptionPrice(spot, strike, NbExp, vol + dv, rate, q, optionType) - cls.OptionPrice(spot, strike, NbExp, vol - dv, rate, q, optionType)) / (2 * dv) / 100))
        rho = float(((cls.OptionPrice(spot, strike, NbExp, vol, rate + dr, q, optionType) - cls.OptionPrice(spot, strike, NbExp, vol, rate - dr, q, optionType)) / (2 * dr) / 1000))
        if NbExp == 0:
            # print "TESTTESTTESTTEST";
            theta = 0
        else:
            theta = float(((cls.OptionPrice(spot, strike, NbExp - dt, vol, rate, q, optionType) - cls.OptionPrice(spot, strike, NbExp + dt, vol, rate, q, optionType)) / (2 * dt)))
        print "delta>>>>>>", delta
        print "gamma>>>>>>", gamma
        print "vega>>>>>>", vega
        print "rho>>>>>>", rho
        print "theta>>>>>", theta
        return 0

    @classmethod
    def timeToMaturity(cls, year, month, day, hour, minute):
        maturity = datetime.datetime(year, month, day, hour, minute, 0, 0, None)
        #  Today's date 
        today = datetime.datetime.today()
        #  Get msec from each, and subtract.
        diff = maturity - today
        return diff.total_seconds() / (60 * 60 * 24)

    # Reference:http://stackoverflow.com/questions/442758/which-java-library-computes-the-cumulative-standard-normal-distribution-function
    @classmethod
    def cdnf(cls, x):
        neg = 1 if (x < 0) else 0
        if neg == 1:
            x *= -1
        k = (1 / (1 + 0.2316419 * x))
        y = ((((1.330274429 * k - 1.821255978) * k + 1.781477937) * k - 0.356563782) * k + 0.319381530) * k
        y = 1.0 - 0.398942280401 * math.exp(-0.5 * x * x) * y
        # print (1d-neg)*y+neg*(1d-y);
        return (1 - neg) * y + neg * (1 - y)

    # For Call Options
    @classmethod
    def annualvolimplied(cls, modelOption, realOption):
        volimplied = cls.stdev(cls.varianceaverage(cls.variancecalcs))
        annualvolimplied = 0
        real = realOption
        model = modelOption
        if real == model:
            annualvolimplied = cls.annualvol2(volimplied)
        elif real > model:
            while True:
                volimplied = volimplied + 0.00001
                model = cls.OptionPrice(105.88, 100.00, cls.daysToMaturityPrime2, cls.annualvol2(volimplied), 0.00229, 0, "c")
                annualvolimplied = cls.annualvol2(volimplied)
                if not ((real > model)):
                    break
        else:
            while True:
                volimplied = volimplied - 0.00001
                model = cls.OptionPrice(105.88, 100.00, cls.daysToMaturityPrime2, cls.annualvol2(volimplied), 0.00229, 0, "c")
                annualvolimplied = cls.annualvol2(volimplied)
                if not ((real < model)):
                    break
        return annualvolimplied

    @classmethod
    def annualvol2(cls, stdev):
        x = math.sqrt(252)
        annualvol2 = x * stdev
        # print "AnnualVolImplied:"+annualvol;
        # annualvolprimeimplied=annualvol2;
        return annualvol2

    # *********************Volatility Calc*******************************************************************************************
    @classmethod
    def logreturn(cls, dates):
        i = 0
        while i < len(dates) - 1:
            # print "Day :"+ i+ ":" + x;
            day2 = dates[i]
            day1 = dates[i+1]
            x = math.log(float(day1.adjclose)/float(day2.adjclose))
            cls.logreturns.append(x)
            i += 1

    @classmethod
    def averagelog(cls, logreturns):
        sum = 0
        counter = 0
        i = 0
        # print len(logreturns)
        # len(logreturns)-1
        while i < len(logreturns):
            y = logreturns[i]
            sum += y
            # print sum;
            counter += 1
            i += 1
        x = sum / counter
        # print x;
        return x

    @classmethod
    def variancecalc(cls, logreturns):
        i = 0
        while i < len(logreturns) - 1:
            y = logreturns[i]
            yprime = y - cls.averagelog(logreturns)
            cls.variancecalcs.append(math.pow(yprime, 2))
            i += 1

    @classmethod
    def varianceaverage(cls, variancecalc):
        sum = 0
        counter = 0
        i = 0
        while i < len(variancecalc) - 1:
            y = variancecalc[i]
            sum += y
            # print sum;
            counter += 1
            i += 1
        x = sum / counter
        print "******************"
        print "VarAvrg:", x
        return x

    @classmethod
    def stdev(cls, varianceAvrg):
        x = math.sqrt(varianceAvrg)
        print "Stdev:", x
        return x

    @classmethod
    def annualvol(cls, stdev):
        x = math.sqrt(252)
        annualvol = x * stdev
        print "AnnualVol:", annualvol
        cls.annualvolprime = annualvol
        return annualvol

    @classmethod
    def reader(cls):
        f = open("table1.txt", "r")
        for line in f:
            s = line.split(",")
            date = s[0]
            opent = s[1]
            high = s[2]
            low = s[3]
            close = s[4]
            volume = s[5]
            adjclose = s[6]
            d = MarketDate(date, opent, high, low, close, volume, adjclose)
            cls.dates.append(d)
    # ************************************************************************************************************************************
    # ************************************************************************************************************************************
    # ************************************************************************************************************************************
    # ********************************Wiki implementation*********************************************************************************
    # **********************************of Black Scholes**********************************************************************************
    # ************************************************************************************************************************************
    # ************************************************************************************************************************************
    # ************************************************************************************************************************************
    # ************************************************************************************************************************************
    @classmethod
    def europeanCallPrice(cls, vol, maturity, spot, strike, rate):
        Nd1S = long((cls.cdnf(cls.d1(vol, maturity, spot, strike, rate)) * spot))
        # print Nd1S;
        Nd2KerTt = long((cls.cdnf(cls.d2(vol, maturity, spot, strike, rate)) * strike * math.exp(-rate * maturity)))
        callprice = Nd1S - Nd2KerTt
        return callprice

    @classmethod
    def europeanPutPrice(cls, vol, maturity, spot, strike, rate):
        KerTt = long((strike * math.exp(-rate * maturity)))
        putprice = long((KerTt - spot + cls.europeanCallPrice(vol, maturity, spot, strike, rate)))
        return putprice

    @classmethod
    def d1(cls, vol, maturity, spot, strike, rate):
        d1 = float()
        a1 = 1 / (vol * math.sqrt(maturity))
        a2 = math.log(spot / strike)
        a3 = (rate + ((vol * vol) / 2)) * (maturity)
        d1 = (a2 + a3) * a1
        return d1

    @classmethod
    def d2(cls, vol, maturity, spot, strike, rate):
        d2 = float()
        a1 = 1 / (vol * math.sqrt(maturity))
        a2 = math.log(spot / strike)
        a3 = (rate - ((vol * vol) / 2)) * (maturity)
        d2 = (a2 + a3) * a1
        return d2

    @classmethod
    def main(cls, args):
        #while True:
        #    stock = raw_input('Stock to pull: ')
        #    cls.pullData(stock)
        daysToMaturity = cls.timeToMaturity(2014, 11, 22, 0, 1)
        #print daysToMaturity
        cls.daysToMaturityPrime2 = daysToMaturity
        
        
        cls.reader()
        cls.logreturn(cls.dates)
        cls.averagelog(cls.logreturns)
        cls.variancecalc(cls.logreturns)
        # for(double d: variancecalcs){
        #   print d;
        # } 
        cls.varianceaverage(cls.variancecalcs)
        cls.stdev(cls.varianceaverage(cls.variancecalcs))
        cls.annualvol(cls.stdev(cls.varianceaverage(cls.variancecalcs)))
        #   print "annualvolprime>>>>>>>>>>>>>>>>>>>>>>>>>>>"+annualvolprime;
        # ************************************************************************************************************************************
        # ***********Test of Wiki BS**********************************************************************************************************
        #           long daysToMaturityPrime=timeToMaturity(2014,4,25,0,1);
        #           long call=europeanCallPrice(annualvolprime,daysToMaturityPrime,539.19,525.00,0.001);
        # print annualvolprime;
        # print daysToMaturity;
        #           long put=europeanPutPrice(annualvolprime,daysToMaturityPrime,539.19,525.00,0.001);
        #           print "Price of E.Call: $"+call;
        #           print "Price of E.Put: $"+put;
        # ************************************************************************************************************************************
        print "--------------------------------\n---------------SG's No Beta-----\n---------------Hedge Alpha------\n--------------------------------\n"
        # OptionPrice(spot,strike,daystoMaturity,vol,rate,q,optiontype as in c or p)
        # long daysToMaturity=timeToMaturity(2014,4,25,0,1);
        c = "c"
        p = "p"
        # int daysToMaturityPrime2=(int) daysToMaturity;
        # for EW
        SgOption = cls.OptionPrice(105.88, 100.00, cls.daysToMaturityPrime2, cls.annualvolprime, 0.00229, 0, c)
        # long SgOptionPut=OptionPrice(64.82,59.50,daysToMaturityPrime2,annualvolprime,0.0012,0,p);
        #SgGreek = cls.greeks(105.88, 100.00, 43, cls.annualvolprime, 0.00229, 0.0001, c)
        print "SG's price of Call: $", SgOption
        # print "SG's price of Put: $"+SgOptionPut;
        # print "TIMMMMMMMMMMMME"+daysToMaturityPrime2;
        impliedvol = cls.annualvolimplied(SgOption, 8.1)
        print "SG's historical annual vol for Call: ", cls.annualvolprime
        print "SG's implied annualvol for Call: ", impliedvol

class MarketDate(object):    
    date = str()
    open = float()
    high = float()
    low = float()
    close = float()
    volume = float()
    adjclose = float()
    weight = float()

    def __init__(self, date, open, high, low, close, volume, adjclose):
        self.setDate(date)
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.adjclose = adjclose
        self.weight = 1
        
    @classmethod
    def getDate(self):
        return self.date
        
    @classmethod
    def setDate(self, date):
        self.date = date
        
    @classmethod
    def getOpen(self):
        return self.open
        
    @classmethod
    def getHigh(self):
        return self.high
        
    @classmethod
    def getLow(self):
        return self.low

    @classmethod
    def getClose(self):
        return self.close

    @classmethod
    def getVolume(self):
        return self.volume
    
    @classmethod
    def getAdjClose(self):
        return self.adjclose

    def __str__(self):
        return self.date + " " + self.open + " " + self.high + " " + self.low + " " + self.close + " " + self.volume + " " + self.adjclose


if __name__ == '__main__':
    import sys
    maindriver.main(sys.argv)


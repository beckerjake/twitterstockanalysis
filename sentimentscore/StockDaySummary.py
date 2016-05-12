import pymysql
import datetime
class StockDaySummary:
#this is a class that generates day summary information for stocks
#day summaray info includes the first hour delta, first hour % delta
#day delta, day % delta, date in question, stock name, start price, and end price
#date is in form 'YYYY-MM-DD'
    

    def __init__(self, day, stockSymbol, databaseName, tableName, user, password, host):
        self.date = day
        self.stockSymbol = stockSymbol
        self.database = databaseName
        self.__tableName = tableName
        self.firstHourD = 0
        self.firstHourPD = 0
        self.dayD = 0
        self.dayPD = 0
        self.startPrice = 0
        self.endPrice = 0

        #connect to database
        connectString = "host=\"" + host + "\", user=\"" + user + "\", passwd=\"" + password + "\", db=\"" + databaseName + "\""
        self.db = pymysql.connect(host=host, user=user, passwd=password, db=databaseName)
        #self.db = pymysql.connect(connectString)
#set up cursor
        self.cur = self.db.cursor()

#this makes call to other modules to get the stock data and then does computations, and returns a list of form [date, stockSymbol, startPrice, endPrice, dayD, dayPD, firstHourD, firstHourPD]
#return an empty list on error
    def returnStockDaySummary(self):
        stockDaySummary = [self.date, self.stockSymbol]
        stockPrices = self.getStockInfo()
        if len(stockPrices) != 3:
            print("incorrect number of stock prices returned in StockDaySummary.returnStockDaySummary\nReturning empty list")
            return []
#add start and end prices
        stockDaySummary.append(stockPrices[0])
        stockDaySummary.append(stockPrices[2])
#change in price over the whole day
        stockDaySummary.append(stockPrices[2] - stockPrices[0])
#% change in price over the whole day
        stockDaySummary.append((stockPrices[2] - stockPrices[0])/stockPrices[2])
#change in price over the first hour
        stockDaySummary.append(stockPrices[1] - stockPrices[0])
#% change in price over the first hour
        stockDaySummary.append((stockPrices[1] - stockPrices[0])/stockPrices[1])
        print stockDaySummary
        return stockDaySummary
        

#this function is responsible for making queries and returning a list of
#form [startPrice, endPrice, firstHourPrice]
    def getStockInfo(self):
#until we start grabbing the price at 13:30 we'll treat hour 14 as the open
#constants that define which hours are open, firstHour, and close
        openHour = 14
        firstHour = 15
        closeHour = 20
        stockPrices = [] 
#compute the timestamp of the next day
        nextDay = self.date[:-2] + "%02d" % (int(self.date[-2:]) + 1)
        queryString = "select price, time_alt from " + self.__tableName + " where symbol = \"" + self.stockSymbol + "\" and time_alt >= \"" + self.date + "\" and time_alt < \"" + nextDay + "\""
        self.cur.execute(queryString)
        for row in self.cur.fetchall():
            if row[1].hour == openHour:
                stockPrices.append(row[0])
            elif row[1].hour == firstHour:
                stockPrices.append(row[0])
            elif row[1].hour == closeHour:
                stockPrices.append(row[0])
                break
        return stockPrices
    def test(self):
        self.returnStockDaySummary()
a = StockDaySummary("2016-05-11","KO", "ticktalk", "stocks", "root", "" ,"localhost")
a.test()

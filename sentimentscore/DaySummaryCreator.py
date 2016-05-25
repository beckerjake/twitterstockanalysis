import pymysql
import sys
from sys import argv
from TweetDaySummary import TweetDaySummary
from StockDaySummary import StockDaySummary

#this file uses tweet and stock day summary objects to create and add rows
#to the day summary table
#New/current days are added with all stock price information as NULL
#date we are creating rows for is specified by the command line


#returns true if date is in 'YYYY-MM-DD' format, false otherwise
def checkDate(date):
    if len(date) != 10:
        return False
    if date[:4].isdigit() != True:
        return False
    if date[5:7].isdigit() != True:
        return False
    if date[8:].isdigit() != True:
        return False
    if date[4] != '-' or date[7] != '-':
        return False
    return True

#list of stocks that we will query from our database
stocks = ['BA','UNH','WFC','T','BP','PCG','KO','IBM','MSFT','MAR']

#returns a sql insert action string for daySummaries
def sqlInsert(tableName, fieldValues):
    insertStatement = "insert into " + tableName + " VALUES (0, "
    for i in range(0, 3):
        insertStatement += "\"" + fieldValues[i] + "\","
    for i in range(3, len(fieldValues)):
        insertStatement += str(fieldValues[i])
        insertStatement += ", "
   #take out the last comma and space
    insertStatement = insertStatement[:-2]
    insertStatement += ")"
    return insertStatement

def main(arg1):
#connect to database
    db = pymysql.connect(autocommit=True, host="localhost", user="root", passwd="", db="ticktalk")
    cur = db.cursor()
#grab date
    date = arg1
#if we don't have a legit date, exit
    if not checkDate(date):
        sys.exit("Incorrectly formatted date!")
#for every stock
    for i in range(len(stocks)):
#create stock and tweet day summary objects
        tweetSum = TweetDaySummary(date, stocks[i], "ticktalk", "tweets", "root", "", "localhost")
        stockSum = StockDaySummary(date, stocks[i], "ticktalk", "stocks", "root", "", "localhost")
        daySummary = tweetSum.returnTweetDaySummary()
        daySummary += stockSum.returnStockDaySummary()
        #change around the position of stockName
        daySummary.insert(2, daySummary[-1])
        del daySummary[-1]
#add to database
        print daySummary
        cur.execute(sqlInsert("daySummaries", daySummary))




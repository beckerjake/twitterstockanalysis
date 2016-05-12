
import pymysql
import datetime
class TweetDaySummary:
#this class generates a list that represents a summary of a day's tweets aboue a company
#tweets for a "day" constitue TODO
#assumes day is in 'YYYY-MM-DD' format
    def __init__(self, day, stockSymbol, databaseName, tableName, user, password, host):
        self.date = day
        self.stockSymbol = stockSymbol
        self.database = databaseName
        self.__tableName = tableName

        #connect to database
        connectString = "host=\"" + host + "\", user=\"" + user + "\", passwd=\"" + password + "\", db=\"" + databaseName + "\""
        self.db = pymysql.connect(host=host, user=user, passwd=password, db=databaseName)
#set up cursor
        self.cur = self.db.cursor()
#this calls other modules and returns a list of sum, positve sum, negative sum, weighted positive sum, weighted negative sum of the following fields:
#followers_count, listed_count, statuses_count
#sum  of total sentiment, positive sentiment, and negative
#we will also have average tweet_time for neu/pos/neg tweets
#return an empty list on error
    def returnTweetDaySummary(self):
#list of what we will eventually return
        tweetDaySummary = [0,0,0,0,0,0,0,0,0,0,0,0]
        times = []
#this is to grab a list of all tweets in the day about the proper stock
#we will grab followers listed statues time and sentiment fields
    def queryForTweets(self):
        tweets = []
#compute the timestamp of the next day
        nextDay = self.date[:-2] + "%02d" % (int(self.date[-2:]) + 1)
        queryString = "select followers_count, listed_count, statuses_count,score, tweet_time from " + self.__tableName + " where stock_symbol = \"$" + self.stockSymbol + "\" and tweet_time >= \"" + self.date + "\" and tweet_time < \"" + nextDay + "\""
        print queryString
        self.cur.execute(queryString)
        for row in self.cur.fetchall():
            tweets.append(row)
        print tweets
        print len(tweets)
        return tweets
    def test(self):
        self.queryForTweets()
a = TweetDaySummary("2016-05-06","MSFT", "ticktalk", "scoredtweets", "root", "" ,"localhost")
a.test()

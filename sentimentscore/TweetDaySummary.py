
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
        allTimes = []
        positiveTimes = []
        negativeTimes = []
        tweets = self.queryForTweets()
        for i in range(len(tweets)):
            score = tweets[i][3]
            allTimes.append(tweets[i][4])
#neutral scores
            tweetDaySummary[0] += tweets[i][0]*score
            tweetDaySummary[3] += tweets[i][1]*score
            tweetDaySummary[6] += tweets[i][2]*score
            tweetDaySummary[9] += score
#positive scores
            if score > 0:
                tweetDaySummary[1] += tweets[i][0]*score
                tweetDaySummary[4] += tweets[i][1]*score
                tweetDaySummary[7] += tweets[i][2]*score
                tweetDaySummary[10] += score
                positiveTimes.append(tweets[i][4])
#negative scores
            elif score < 0:
                tweetDaySummary[2] += tweets[i][0]*score
                tweetDaySummary[5] += tweets[i][1]*score
                tweetDaySummary[8] += tweets[i][2]*score
                tweetDaySummary[11] += score
                negativeTimes.append(tweets[i][4])

#calculate average times
        if len(positiveTimes) > 0:
            averagePositiveTime = self.avgTime(positiveTimes)
        else:
            averagePositiveTime = "NULL"
        if len(negativeTimes) > 0:
            averageNegativeTime = self.avgTime(negativeTimes)
        else:
            averageNegativeTime = "NULL"
        averageTime = self.avgTime(allTimes)
        tweetDaySummary.append(averageTime)
        tweetDaySummary.append(averagePositiveTime)
        tweetDaySummary.append(averageNegativeTime)
       #add the stock symbol and date
        summaryWithDateAndSymbol = [self.date, self.stockSymbol] + tweetDaySummary 
        return summaryWithDateAndSymbol
#used to compute an average of datetime objects
#returned in form: number of hours past midnight
    def avgTime(self, times):
        avg = 0
        if len(times) == 0:
            return 'NULL'
        for elem in times:
            avg += elem.second + 60*elem.minute + 3600*elem.hour
        avg /= float(len(times))
        avg /= 3600
        return avg
        
#this is to grab a list of all tweets in the day about the proper stock
#we will grab followers listed statues time and sentiment fields
    def queryForTweets(self):
        tweets = []
#compute the timestamp of the next day
        nextDay = self.date[:-2] + "%02d" % (int(self.date[-2:]) + 1)
        queryString = "select followers_count, listed_count, statuses_count,score, tweet_time from " + self.__tableName + " where stock_symbol = \"$" + self.stockSymbol + "\" and tweet_time >= \"" + self.date + "\" and tweet_time < \"" + nextDay + "\""
        self.cur.execute(queryString)
        for row in self.cur.fetchall():
            tweets.append(row)
        return tweets
    def test(self):
        print(self.returnTweetDaySummary())


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
#mean of all sentiment scores
        mean = .31
#list of what we will eventually return
        tweetDaySummary = [0,0,0,0,0,0,0,0,0,0,0,0]
        allTimes = []
        positiveTimes = []
        negativeTimes = []
        tweets = self.queryForTweets()
        followers = 0
        lists = 0
        for i in range(len(tweets)):
            score = tweets[i][3]
            allTimes.append(tweets[i][4])
            followers += tweets[i][0]
            lists += tweets[i][1] 
#neutral scores
            tweetDaySummary[0] += tweets[i][0]*score
            tweetDaySummary[3] += tweets[i][1]*score
            tweetDaySummary[6] += tweets[i][2]*score
            tweetDaySummary[9] += score
#positive scores
            if score > 0.31:
                tweetDaySummary[1] += tweets[i][0]*(score-mean)
                tweetDaySummary[4] += tweets[i][1]*(score-mean)
                tweetDaySummary[7] += tweets[i][2]*(score-mean)
                tweetDaySummary[10] += score
                positiveTimes.append(tweets[i][4])
#negative scores
            elif score < 0.31:
                tweetDaySummary[2] += tweets[i][0]*(score-mean)
                tweetDaySummary[5] += tweets[i][1]*(score-mean)
                tweetDaySummary[8] += tweets[i][2]*(score-mean)
                tweetDaySummary[11] += score
                negativeTimes.append(tweets[i][4])

        if len(tweets) > 0:
            averageSentiment = tweetDaySummary[9] / len(tweets)
        else:
            averageSentiment = "NULL"
        if followers > 0:
            waSentimentByFollowers = tweetDaySummary[0] / followers 
        else:
            waSentimentByFollowers = "NULL"
        if lists > 0:
            waSentimentByLists = tweetDaySummary[1] / lists
        else:
            waSentimentByLists = "NULL"
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
        tweetDaySummary.append(averageSentiment)
        tweetDaySummary.append(waSentimentByFollowers)
        tweetDaySummary.append(waSentimentByLists)
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
            avg += elem.second + 60*elem.minute + 3600*(elem.hour-4)
        avg /= float(len(times))
        avg /= 3600
        return avg
        
#this is to grab a list of all tweets in the day about the proper stock
#we will grab followers listed statues time and sentiment fields
    def queryForTweets(self):
        tweets = []
#compute the timestamp of the next day
        times = self.getMarketCloseToOpenTimes(self.date)
        startTime = times[0]
        endTime = times[1]
        queryString = "select followers_count, listed_count, statuses_count,score, tweet_time from " + self.__tableName + " where stock_symbol = \"$" + self.stockSymbol + "\" and tweet_time >= \"" + startTime + "\" and tweet_time < \"" + endTime + "\""
        print queryString
        self.cur.execute(queryString)
        for row in self.cur.fetchall():
            tweets.append(row)
        return tweets
    def test(self,date):
        self.getMarketCloseToOpenTimes(date)

#this takes as input a day in the market that we will create a TweetSummary for
#returns a list with two strings in 'YYYY-MM-DD HH:MM:SS' form
#Our tweet summary spans from the close of the market the previous day until market open of the day specified
#considerations, first/last day of month
#TODO weekends should have more associated tweets and span a longer time
    def getMarketCloseToOpenTimes(self,date):
#define constants
        daysInEachMonth = [31,28,31,30,31,30,31,31,30,31,30,31]
        startHour = " 20:00:00"
        endDate = date + " 13:30:00"
#grab numbers out of date
        year = int(date[:4])
        month = int(date[5:7])
        day = int(date[8:])
#check if first day of month and year
        if day == 1 and month == 1:
            year -= 1
            day = 31
            month = 12
#check if first day of month
        elif day == 1:
            month -= 1
            day = daysInEachMonth[month - 1]
        else:
            day -= 1

        startDate = str(year) + '-' + "%02d" % month + '-' + "%02d" % day + startHour
        print startDate
        print endDate
        return [startDate, endDate]
a = TweetDaySummary("2016-05-09",'MSFT','ticktalk','tweets','root','','localhost')
print a.returnTweetDaySummary()




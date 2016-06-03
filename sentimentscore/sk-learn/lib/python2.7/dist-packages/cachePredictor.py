from numpy import arange,array,ones,linalg,std
import pymysql
import constants as c
#array that contains names of all columns that represent twitter data aggregations
updateColNames = [
'date',
'symbol',
'stockName',
'followers_count',
'positive_followers_count',
'negative_followers_count',
'listed_count',
'positive_listed_count',
'negative_listed_count',
'statuses_count',
'positive_statuses_count'
,'negative_statuses_count',
'total_sentiment',
'positive_sentiment',
'negative_sentiment',
'average_time',
'positive_average_time',
'negative_average_time',
'average_sentiment',
'weighted_average_sentiment_by_followers',
'wa_sentiment_by_lists',
'totalMentions',
'start_price',
'hour_change',
'percent_hour_change',
'end_price',
'day_change',
'percent_day_change']
xi = arange(0,9)
A = array([xi, ones(9)])
y = [19,20,20.5,21.5,22,23,23,25.5,24]
w,resid = linalg.lstsq(A.T,y)[:2]

r2 = 1 - resid / (len(y) * std(y) ** 2)

#print("The slope is: " + str(w[0]))
#print("The intercept is: " + str(w[1]))
#print("The r^2 value is: " + str(r2))
#list of stocks that we will query from our database

class Predictor:
    def __init__(self, day, stockSymbols, databaseName, inputTableName, historyTableName, outputTableName, user, password, host):
        self.date = day
        self.stockSymbols = stockSymbols
        self.database = databaseName
        self.__outputTableName = outputTableName
        self.__inputTableName = inputTableName
        self.__historyTableName = historyTableName
        #list of all daysummaries
        self.daySummaries = []
        self.cleanDaySummaries = []    
        self.dayChanges = []
        self.hourChanges = []
        self.tweetVals = 0
#day change is the first col, hour change is the second col
        self.rVals = 0
        self.slopes = 0
        self.intercepts = 0
        self.bestR2Indices = []
        #20 40 60 80
        self.dayPercentiles = []
        self.hourPercentiles = []
        #connect to database
        connectString = "host=\"" + host + "\", user=\"" + user + "\", passwd=\"" + password + "\", db=\"" + databaseName + "\""
        self.db = pymysql.connect(host=host, user=user, passwd=password, db=databaseName)
#set up cursor
        self.cur = self.db.cursor()
        self.loadData()
    def loadData(self):
        self.loadDaySummaries()
        self.loadCleanDaySummaries()
        self.loadYArrays()
        self.loadXArrays()
        self.createCorrelationMatrix()
        self.bestR2Indices = self.getBestR2Indices()
        self.computePercentiles()
    def test(self):
        self.printColNamesOfBestR2Indices(self.bestR2Indices)
        self.printBestRegressionLines()
        self.applyFilters()
#        self.whereTheMagicHappens()
#grab all rows out of day summary table
    def loadDaySummaries(self):
        queryString = "select * from " + self.__inputTableName
        self.cur.execute(queryString)
        for row in self.cur.fetchall():
            self.daySummaries.append(row)
#this function clears all the member arrays we need for computing an
#individual regression
    def clearArrays(self):
        del self.cleanDaySummaries[:]
        del self.dayChanges[:]
        del self.hourChanges[:]
#this functions takes out any daySummaries that don't have the complete
#stock information
#these won't be used to make predictions
    def loadCleanDaySummaries(self):
        for row in self.daySummaries:
            if not row[c.hourpercentchange] == -10 and not row[c.daypercentchange] == -10:
                self.cleanDaySummaries.append(row)
#TODO: here would be a good place to apply filters or a dynamic filter
#we are filtering based on totalMentions and positivelistedcount (and 
#percent day change to make sure our rows have stock information
    def applyFilters(self):
        #get range of totalmentions and
        #get range of positive listed count
        maxMention = -1
        minMention = 999999
        maxListed = -1
        minListed = 99999999
        for i in range(len(self.cleanDaySummaries)):
            if self.cleanDaySummaries[i][c.totalmentionsindex] > maxMention:
                maxMention = self.cleanDaySummaries[i][c.totalmentionsindex] 
            if self.cleanDaySummaries[i][c.totalmentionsindex] < minMention:
                minMention = self.cleanDaySummaries[i][c.totalmentionsindex] 
            if self.cleanDaySummaries[i][c.positivelistedcountindex] > maxListed:
                maxListed = self.cleanDaySummaries[i][c.positivelistedcountindex] 
            if self.cleanDaySummaries[i][c.positivelistedcountindex] < minListed: 
                minListed = self.cleanDaySummaries[i][c.positivelistedcountindex] 
        #100th increments of each
        mentionInc = (maxMention - minMention)/100
        listedInc = (maxListed - minListed)/200
        #set up best filter values and best filter r2
        #all filter values are read as attributeVal > filtervalue
        bestMentionFilter = -1
        bestListedFilter = -1
        bestR2 = -1
        unfilteredDataLength = len(self.cleanDaySummaries)
        #double for loop
        for mentionFilter in range(int(minMention), int(maxMention), int(mentionInc)):
            breakIndex = -1
            for listedFilter in range(int(minListed), int(maxListed), int(listedInc)):
                breakIndex = listedFilter
            #make query based on filter
                queryString = "select * from " + self.__inputTableName + " where totalMentions > " + str(mentionFilter) + " and positive_listed_count > " + str(listedFilter) + " and percent_day_change > -9.9"
                self.cur.execute(queryString)
            #set result of query to cleandaysummaries
                newTempData = []
                self.clearArrays()
                for row in self.cur.fetchall():
                    self.cleanDaySummaries.append(row)
                dataRemaining = float(len(self.cleanDaySummaries))/unfilteredDataLength
#                print("we have only this percent of data remaining: " + str(dataRemaining))
                if dataRemaining < .24:
                    break
            #loadX and Y arrays
                self.loadYArrays()
                self.loadXArrays()
            #create correlation matrix
                self.createCorrelationMatrix()
            #get best correlation value
                self.bestR2Indices =  self.getBestR2Indices()
            #if better than current value
                if self.rVals[self.bestR2Indices[0]][0] > bestR2:
                #change indices and best value
                    bestR2 = self.rVals[self.bestR2Indices[0]][0] 
                    bestMentionFilter = mentionFilter
                    bestListedFilter = listedFilter
            #here we break again if we're below the limit on the coarsest
            #possible listedFilter
            if breakIndex == int(minListed):
                break
        #save filters as member variables to use when computing predictions
        #make one final computation so member variables reflect best R val
        print("The best r^2 value is: " + str(bestR2) " when we use at least " + str(dataRemaining) + " of the data.")
#create two arrays for the first hour percent change and day percent change
#these we will use for our y values
    def loadYArrays(self):
        for row in self.cleanDaySummaries:
            #add 1 because we don't have "ID" in the column names
            self.dayChanges.append(row[c.daypercentchange])
            self.hourChanges.append(row[c.hourpercentchange])

#create two dimensional array in which every row is tweet aggregation 
#this is a transposition of the cleandaysummary list
    def loadXArrays(self):
        self.tweetVals = [[0 for x in range(len(self.cleanDaySummaries))] for y in range(c.tweetcols)]
        #cycle through days
        for i in range(len(self.cleanDaySummaries)):
            #cycle through attributes of the row
            for j in range(c.tweetstartindex, c.tweetendindex):
                a = self.cleanDaySummaries[i][j]
                self.tweetVals[j-c.infocols][i] = a
#returns an array in which None has been exchanged for 0
    def cleanArray(self, inputList):
        rowOne = []
        for i in range(len(inputList[0])):
            if inputList[0][i] is None:
                rowOne.append(0)
            else:
                rowOne.append(inputList[0][i])
        rowTwo = []
        for i in range(len(inputList[1])):
            rowTwo.append(1)
        return array([rowOne, rowTwo])
#create function that takes an index (which represents a row) as input
#and returns that row as a transposed two dimensional array
    def getTransposedArray(self, index):
        toReturn = array([self.tweetVals[index], ones(len(self.cleanDaySummaries))])
        toReturn = self.cleanArray(toReturn)
        return zip(*toReturn)
#loop to create regression for every indep row for both dep arrays
#save the r^2 val in nx2 array
    def createCorrelationMatrix(self):
        self.rVals = [[0 for x in range(2)] for y in range(c.tweetcols)]
        self.slopes = [[0 for x in range(2)] for y in range(c.tweetcols)]
        self.intercepts = [[0 for x in range(2)] for y in range(c.tweetcols)]
        #for every tweet attritbute
        for i in range(c.tweetcols):
            #for the day change
            xVals = self.getTransposedArray(i)
            w,resid = linalg.lstsq(xVals, self.dayChanges)[:2]
            r2 = 1 - resid / (len(self.dayChanges) * std(self.dayChanges) ** 2)
            self.rVals[i][0] = r2[0]
            self.slopes[i][0] = w[0]
            self.intercepts[i][0] = w[1]
            #for the hour change
            w,resid = linalg.lstsq(xVals, self.hourChanges)[:2]
            r2 = 1 - resid / (len(self.hourChanges) * std(self.hourChanges) ** 2)
            self.rVals[i][1] = r2[0]
            self.slopes[i][1] = w[0]
            self.intercepts[i][1] = w[1]
#find the indices of three best indicators based on r^2 val for both dep vars
#find the indices of the three best r^2 vals in rVals
#returned in form [bestday, 2day, 3day, besthour, 2hour, 3hour]
    def getBestR2Indices(self):
        day1 = -1
        day2 = -1
        day3 = -1
        hour1 = -1
        hour2 = -1
        hour3 = -1
        dayi1 = -1
        dayi2 = -1
        dayi3 = -1
        houri1 = -1
        houri2 = -1
        houri3 = -1
        #find the best index for both
        for i in range(len(self.rVals)):
            if self.rVals[i][0] > day1:
                day1 = self.rVals[i][0]
                dayi1 = i
            if self.rVals[i][1] > hour1:
                hour1 = self.rVals[i][1]
                houri1 = i
        #second best
        for i in range(len(self.rVals)):
            if self.rVals[i][0] > day2 and i != dayi1:
                day2 = self.rVals[i][0]
                dayi2 = i
            if self.rVals[i][1] > hour2 and i != houri1:
                hour2 = self.rVals[i][1]
                houri2 = i
        #third best
        for i in range(len(self.rVals)):
            if self.rVals[i][0] > day3 and i != dayi1 and i != dayi2:
                day3 = self.rVals[i][0]
                dayi3 = i
            if self.rVals[i][1] > hour3 and i != houri1 and i != houri2:
                hour3 = self.rVals[i][1]
                houri3 = i
        return [dayi1, dayi2, dayi3, houri1, houri2, houri3]
#print out the column names of these three indicies
#takes input form getBestR2Indices
    def printColNamesOfBestR2Indices(self, indices):
        print("The best R2 val for day change comes from " +
                updateColNames[indices[0] +  c.updateinfocols] + ": \n"
                + str(self.rVals[indices[0]][0]))
        print("The 2nd best R2 val for day change comes from " +
                updateColNames[indices[1] +  c.updateinfocols] + ": \n"
                + str(self.rVals[indices[1]][0]))
        print("The 3rd best R2 val for day change comes from " +
                updateColNames[indices[2] +  c.updateinfocols] + ": \n"
                + str(self.rVals[indices[2]][0]))
        print("The best R2 val for hour change comes from " +
                updateColNames[indices[3] +  c.updateinfocols] + ": \n"
                + str(self.rVals[indices[3]][1]))
        print("The 2nd best R2 val for hour change comes from " +
                updateColNames[indices[4] +  c.updateinfocols] + ": \n"
                + str(self.rVals[indices[4]][1]))
        print("The 3rd best R2 val for hour change comes from " +
                updateColNames[indices[5] +  c.updateinfocols] + ": \n"
                + str(self.rVals[indices[5]][1]))
#this function prints the regression lines for the most correlated line
    def printBestRegressionLines(self):
        print("Best day line -- " + 
                updateColNames[self.bestR2Indices[0]+c.updateinfocols] +
                "\n y = " + str(self.slopes[self.bestR2Indices[0]][0]) +
                "x + " + str(self.intercepts[self.bestR2Indices[0]][0]))
        print("2nd best day line -- " + 
                updateColNames[self.bestR2Indices[1]+c.updateinfocols] +
                "\n y = " + str(self.slopes[self.bestR2Indices[1]][0]) +
                "x + " + str(self.intercepts[self.bestR2Indices[1]][0]))
        print("3nd best day line -- " + 
                updateColNames[self.bestR2Indices[2]+c.updateinfocols] +
                "\n y = " + str(self.slopes[self.bestR2Indices[2]][0]) +
                "x + " + str(self.intercepts[self.bestR2Indices[2]][0]))
        print("\nBest hour line -- " + 
                updateColNames[self.bestR2Indices[3]+c.updateinfocols] +
                "\n y = " + str(self.slopes[self.bestR2Indices[3]][1]) +
                "x + " + str(self.intercepts[self.bestR2Indices[3]][1]))
        print("2nd best hour line -- " + 
                updateColNames[self.bestR2Indices[4]+c.updateinfocols] +
                "\n y = " + str(self.slopes[self.bestR2Indices[4]][1]) +
                "x + " + str(self.intercepts[self.bestR2Indices[4]][1]))
        print("3rd best hour line -- " + 
                updateColNames[self.bestR2Indices[5]+c.updateinfocols] +
                "\n y = " + str(self.slopes[self.bestR2Indices[5]][1]) +
                "x + " + str(self.intercepts[self.bestR2Indices[5]][1]))

#determine cutoff values for predicted growth->reccomendation
#this is done be grabbing the performance data and computing
#20th, 40th, 60th, and 80th percentiles are stored in self.percentiles
    def computePercentiles(self):
        hourPerformance = []
        dayPerformance = []
        for i in range(len(self.daySummaries)):
            if self.daySummaries[i][c.daypercentchange] != -10 and self.daySummaries[i][c.hourpercentchange] != -10:
                hourPerformance.append(self.daySummaries[i][c.hourpercentchange])
                dayPerformance.append(self.daySummaries[i][c.daypercentchange])
        hourPerformance = sorted(hourPerformance)
        dayPerformance = sorted(dayPerformance)
        print dayPerformance
        dayLength = len(dayPerformance)
        hourLength = len(hourPerformance)
        for i in range(4):
            self.dayPercentiles.append(dayPerformance[int((.2 + i*.2)*dayLength)])
            self.hourPercentiles.append(hourPerformance[int((.2 + i*.2)*hourLength)])
        
#this function takes index into bestr2indices and the associated x coord
#returns the result of plugging it into the regression specified by
#slopes and intercepts
    def plugIntoRegression(self, r2Index, xcoord):
        #get index into slopes/regression
        lineIndex = self.bestR2Indices[r2Index]
        #get day/hour day = 0, hour = 1
        if r2Index > 3:
            isHour = 1
        else:
            isHour = 0
        #get slope
        slope = self.slopes[lineIndex][isHour]
        #get intercept
        intercept = self.intercepts[lineIndex][isHour]
        #plug in and return
        return slope * xcoord + intercept

#function that determines the avg daily mentions of every stock based on symbol

#function that queries to see what % of today's tweets are positive

#function that takes stock, day, pos/nge/neutral and returns tweet_id of tweet of the day
#this is workhorse function that uses everything et up from load data to:
#make a prediction for every stock
#grab the tweet of the day
#grab the % total mention volume and pos/neg %s
#writes these as a row into the database of current predictions
#write a row to the historical predictions table if we don't have the 
    #open price of the stock (update row if needed)
    def whereTheMagicHappens(self):
#for every stock we're looking at
        for i in range(len(stocks)):
    #grab that stocks current day summary row
            queryString = "select * from " + self.__inputTableName + " where symbol = \"" + stocks[i] + "\" and date = \"" + self.date + "\""
            self.cur.execute(queryString);
            row = self.cur.fetchall()
            print stocks[i]
            if len(row) != 1:#sanity check
                print("ERROR ERROR ERROR: returned multiple rows for one stock we are predicting in Predictor.py whereTheMagicHappens()")
            row = row[0]
        #TODO: if stock satisfies the filters we defined above
            #plug into regression equations for first hour and day
            xcoord = row[c.infocols + self.bestR2Indices[0]]
            print("the x coord is: " + str(xcoord))
            print("regression val is: " + str(self.plugIntoRegression(0, xcoord)))
        #write predictions to row
    #else, write "not enough data"
    #add avg daily mention number, %pos/neg to the row
    #grab tweet id of tweet of the day
    
    #add/update the row in historicalpredictions table
    #add/update row in current predicitons table


stocks = ['BA','UNH','WFC','T','BP','PCG','KO','IBM','MSFT','MAR']
a = Predictor('2016-06-02', stocks, "ticktalk", 
"daySummaries", "predictionHistory","currentPredictions",
"root", "", "localhost")
a.test()

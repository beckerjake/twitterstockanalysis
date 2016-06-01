from numpy import arange,array,ones,linalg,std
#array that contains names of all columns that represent twitter data aggregations
tweetAggregationColNames = ['followers_count','positive_followers_count','negative_followers_count','listed_count','positive_listed_count','negative_listed_count','statuses_count','positive_statuses_count','negative_statuses_count','total_sentiment','positive_sentiment','negative_sentiment','average_time','positive_average_time','negative_average_time','average_sentiment','wavg_sentiment_by_followers','wavg_sentiment_by_lists','totalMentions']
xi = arange(0,9)
A = array([xi, ones(9)])
print A
print A.T
y = [19,20,20.5,21.5,22,23,23,25.5,24]
w,resid = linalg.lstsq(A.T,y)[:2]

r2 = 1 - resid / (len(y) * std(y) ** 2)

print("The slope is: " + str(w[0]))
print("The intercept is: " + str(w[1]))
print("The r^2 value is: " + str(r2))


#grab all rows out of day summary table
#here would be a good place to apply filters or a dynamic filter

#create two arrays for the first hour percent change and day percent change
#these we will use for our y values

#create two dimensional array in which every row is tweet aggregation 

#create function that takes an index (which represents a row) as input
#and returns that row as a transposed two dimensional array

#loop to create regression for every indep row for both dep arrays
#save the r^2 val in nx2 array

#find the indices of three best indicators based on r^2 val for both dep vars
#print out the column names of these three indicies

#TODO: more comment detailing prediction mechanism

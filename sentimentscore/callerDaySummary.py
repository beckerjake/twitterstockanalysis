#this file is a script that calls day summary creator repeatedly
#with a list of dates to pass in
import DaySummaryCreator
#list of stocks that we will query from our database
stocks = ['BA','UNH','WFC','T','BP','PCG','KO','IBM','MSFT','MAR']
dates = ['2016-05-06','2016-05-09','2016-05-10', '2016-05-11', '2016-05-12', '2016-05-16','2016-05-17','2016-05-23', '2016-05-24','2016-05-25','2016-05-26','2016-05-27','2016-05-31','2016-06-01','2016-06-02']
for i in range(len(dates)):
    DaySummaryCreator.main(dates[i])

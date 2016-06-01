#this file is a script that calls day summary creator repeatedly
#with a list of dates to pass in
import DaySummaryCreator
dates = ['2016-05-06','2016-05-09','2016-05-10', '2016-05-11', '2016-05-12', '2016-05-16','2016-05-17','2016-05-23', '2016-05-24','2016-05-25','2016-05-26','2016-05-27']

for i in range(len(dates)):
    DaySummaryCreator.main(dates[i])

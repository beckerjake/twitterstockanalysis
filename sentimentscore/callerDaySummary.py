#this file is a script that calls day summary creator repeatedly
#with a list of dates to pass in
import DaySummaryCreator
dates = ['2016-05-06','2016-05-09','2016-05-10']

for i in range(len(dates)):
    DaySummaryCreator.main(dates[i])

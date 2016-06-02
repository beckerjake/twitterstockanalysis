#this file defines constants, most of which deal with indexes into
#the list of day summaries. This makes it easier to add new aggregations

#DAYSUMMARY CONSTANTS
totalcols = 29
infocols = 4
tweetcols = 19
stockcols = 6
updateinfocols = infocols - 1
daypercentchange = totalcols - 1
hourpercentchange = totalcols - stockcols + 2
tweetstartindex = infocols
tweetendindex = infocols + tweetcols

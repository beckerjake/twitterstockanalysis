# twitterstockanalysis
Project for CS 130

To run twtr_stocks, you'll need to install Node.
Then, use the commond '$ npm install twitter' to install the Twitter API client library.

For security, don't put the API keys in a commit.  This is a public repo and we don't want anyone to see or use our keys.  Instead, set them as environment variables on your system.
See twtr_stocks.js for the names of the environment variables.

The script can be run with '$ node twtr_stocks.js'
The text of tweets matching the tracking string (specified in the file) will be logged to the console.

Resources:

'Making a javascript string sql friendly' :
    http://stackoverflow.com/questions/7744912/making-a-javascript-string-sql-friendly
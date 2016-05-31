# twitterstockanalysis
Project for CS 130

To run twtr_stocks, you'll need to install Node.
Then, use the commond '$ npm install twitter' to install the Twitter API client library.

For security, don't put the API keys in a commit.  This is a public repo and we don't want anyone to see or use our keys.  Instead, set them as environment variables on your system.
See twtr_stocks.js for the names of the environment variables.

The script can be run with '$ node twtr_stocks.js'
The text of tweets matching the tracking string (specified in the file) will be logged to the console.

Resources:

Node Twitter streaming APIs:
    https://www.npmjs.com/package/twitter
    https://www.npmjs.com/package/twitter-stream-channels
        https://github.com/topheman/twitter-stream-channels

'Making a javascript string sql friendly' :
    http://stackoverflow.com/questions/7744912/making-a-javascript-string-sql-friendly
    
SQL updating
    http://www.w3schools.com/sql/sql_update.asp
    
MySQL error code 1175
    http://stackoverflow.com/questions/11448068/mysql-error-code-1175-during-update-in-mysql-workbench
    
MySQl - selecting by newest timestamp
    http://stackoverflow.com/questions/11912221/mysql-select-by-newest-timestamp
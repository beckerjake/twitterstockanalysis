// https://www.npmjs.com/package/twitter

var Twitter = require('twitter');

var client = new Twitter({
   consumer_key: process.env.TWITTER_CONSUMER_KEY,
   consumer_secret: process.env.TWITTER_CONSUMER_SECRET,
   access_token_key: process.env.TWITTER_ACCESS_TOKEN_KEY,
   access_token_secret: process.env.TWITTER_ACCESS_TOKEN_SECRET
});

var match = /(\$BA|\$UNH|\$WFC|\$T|\$BP|\$PCG|\$KO|\$IBM|\$MSFT|\$MAR)/;
var match2 = '\$MSFT'

client.stream('statuses/filter', {track: match2}, function(stream) {
    stream.on('data', function(tweet) {
        console.log(tweet);
    });
    
    stream.on('error', function(error) {
        throw error;
    });
});

// https://www.npmjs.com/package/twitter

var Twitter = require('twitter');
var mysql = require('mysql');

var connection = mysql.createConnection({
	host: 'localhost',
	user: 'root',
	password: '',
	database: 'ticktalk'
});

connection.connect();

var client = new Twitter({
   consumer_key: process.env.TWITTER_CONSUMER_KEY,
   consumer_secret: process.env.TWITTER_CONSUMER_SECRET,
   access_token_key: process.env.TWITTER_ACCESS_TOKEN_KEY,
   access_token_secret: process.env.TWITTER_ACCESS_TOKEN_SECRET
});

function getBoolVal(str) {
	return str ? 1 : 0;
}

function mysql_real_escape_string (str) {
	return str.replace(/[\0\x08\x09\x1a\n\r"'\\\%]/g, function (char) {
		switch (char) {
			case "\0":
				return "\\0";
			case "\x08":
				return "\\b";
			case "\x09":
				return "\\t";
			case "\x1a":
				return "\\z";
			case "\n":
				return "\\n";
			case "\r":
				return "\\r";
			case "\"":
			case "'":
			case "\\":
			case "%":
				return "\\"+char;
		}
	});
}

function storeTweetInDB(twt) {
	if (twt['lang'] == 'en') {
		var pkey = twt['id_str'];
		var tweetText = mysql_real_escape_string(twt['text']);
		var user = mysql_real_escape_string(twt['user']['id_str']);
		var name = mysql_real_escape_string(twt['user']['name']);
		var username = mysql_real_escape_string(twt['user']['screen_name']);
		var loc = "";
		
		if (twt['user']['location'] != null) {
			loc = mysql_real_escape_string(twt['user']['location']);
		}

		var description = "";
		if (twt['user']['description'] != null) {
			description = mysql_real_escape_string(twt['user']['description']);
		}
		
		var protectd = getBoolVal(twt['user']['protected']);
		var verified = getBoolVal(twt['user']['verified']);
		var followers_count = parseInt(twt['user']['followers_count']);
		var friends_count = parseInt(twt['user']['friends_count']);
		var listed_count = parseInt(twt['user']['listed_count']);
		var favourites_count = parseInt(twt['user']['favourites_count']);
		var statuses_count = parseInt(twt['user']['statuses_count']);
		var possibly_sensitive = getBoolVal(twt['possibly_sensitive']);
		var tweetTime = Math.floor(parseInt(twt['timestamp_ms']) / 1000);		// convert ms to s
		
		console.log('INSERT INTO tweets (tweet_id, tweet_text, user_id, name, user_name, location, description, protected, verified, followers_count, friends_count, listed_count, favourites_count, statuses_count, possibly_sensitive, tweet_time) VALUES (\''+pkey+'\',\''+tweetText+'\',\''+user+'\',\''+name+'\',\''+username+'\',\''+loc+'\',\''+description+'\','+protectd+','+verified+','+followers_count+','+friends_count+','+listed_count+','+favourites_count+','+statuses_count+','+possibly_sensitive+',FROM_UNIXTIME('+tweetTime+'))');
		
		connection.query('INSERT INTO tweets (tweet_id, tweet_text, user_id, name, user_name, location, description, protected, verified, followers_count, friends_count, listed_count, favourites_count, statuses_count, possibly_sensitive, tweet_time) VALUES (\''+pkey+'\',\''+tweetText+'\',\''+user+'\',\''+name+'\',\''+username+'\',\''+loc+'\',\''+description+'\','+protectd+','+verified+','+followers_count+','+friends_count+','+listed_count+','+favourites_count+','+statuses_count+','+possibly_sensitive+',FROM_UNIXTIME('+tweetTime+'))', function(err, rows, data) {
			if (err) {
				console.log(err);
			}
		});
	}	
}

client.stream('statuses/filter', {track: '\$BA, \$UNH, \$WFC, \$T, \$BP, \$PCG, \$KO, \$IBM, \$MSFT, \$MAR, \$ATVI, \$ED, \$FISV, \$CERN, \$MHK, \$MSI'}, function(stream) {
	stream.on('data', function(tweet) {
        storeTweetInDB(tweet);
   	});
    
    stream.on('error', function(error) {
        throw error;
    });
});


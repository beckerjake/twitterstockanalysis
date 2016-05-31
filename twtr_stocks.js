// https://github.com/topheman/twitter-stream-channels

var TwitterStreamChannels = require('twitter-stream-channels');
var mysql = require('mysql');

var connection = mysql.createConnection({
	host: 'localhost',
	user: 'root',
	password: '',
	database: 'ticktalk'
});

connection.connect();

var client = new TwitterStreamChannels({
   consumer_key: process.env.TWITTER_CONSUMER_KEY,
   consumer_secret: process.env.TWITTER_CONSUMER_SECRET,
   access_token_key: process.env.TWITTER_ACCESS_TOKEN_KEY,
   access_token_secret: process.env.TWITTER_ACCESS_TOKEN_SECRET
});

var channels = {
	"keywords_ba": 		['\$BA','boeing', 'planes', 'airbus', 'airlines'],
	"keywords_unh": 	['\$UNH'],
	"keywords_wfc": 	['\$WFC'],
	"keywords_t": 		['\$T'],
	"keywords_bp": 		['\$BP', 'BP', 'oil', 'petroleum'],
	"keywords_pcg": 	['\$PCG'],
	"keywords_ko": 		['\$KO'],
	"keywords_ibm": 	['\$IBM'],
	"keywords_msft": 	['\$MSFT'],
	"keywords_mar": 	['\$MAR'],
	"keywords_atvi": 	['\$ATVI'],
	"keywords_ed": 		['\$ED'],
	"keywords_fisv": 	['\$FISV'],
	"keywords_cern": 	['\$CERN'],
	"keywords_mhk": 	['\$MHK'],
	"keywords_msi": 	['\$MSI']
};

var stream = client.streamChannels({track:channels});

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

function storeTweetInDB(twt, sym) {
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
		
		var symbol_mentioned = 0;
		if (tweetText.indexOf(sym) > -1) {
			symbol_mentioned = 1;
		}
	
		connection.query('INSERT INTO tweets (tweet_id, stock_symbol, tweet_text, user_id, name, user_name, location, description, protected, verified, followers_count, friends_count, listed_count, favourites_count, statuses_count, possibly_sensitive, tweet_time, symbol_mentioned) VALUES (\''+pkey+'\',\''+sym+'\',\''+tweetText+'\',\''+user+'\',\''+name+'\',\''+username+'\',\''+loc+'\',\''+description+'\','+protectd+','+verified+','+followers_count+','+friends_count+','+listed_count+','+favourites_count+','+statuses_count+','+possibly_sensitive+',FROM_UNIXTIME('+tweetTime+'),'+symbol_mentioned+')', function(err, rows, data) {
			if (err) {
				console.log(err);
			}
		});
	}
}

stream.on('channels/keywords_ba', function(tweet) {
	storeTweetInDB(tweet, "\$BA");
});

stream.on('channels/keywords_unh', function(tweet) {
	storeTweetInDB(tweet, "\$UNH");
});

stream.on('channels/keywords_wfc', function(tweet) {
	storeTweetInDB(tweet, "\$WFC");
});

stream.on('channels/keywords_t', function(tweet) {
	storeTweetInDB(tweet, "\$T");
});

stream.on('channels/keywords_bp', function(tweet) {
	storeTweetInDB(tweet, "\$BP");
});

stream.on('channels/keywords_pcg', function(tweet) {
	storeTweetInDB(tweet, "\$PCG");
});

stream.on('channels/keywords_ko', function(tweet) {
	storeTweetInDB(tweet, "\$KO");
});

stream.on('channels/keywords_ibm', function(tweet) {
	storeTweetInDB(tweet, "\$IBM");
});

stream.on('channels/keywords_msft', function(tweet) {
	storeTweetInDB(tweet, "\$MSFT");
});

stream.on('channels/keywords_mar', function(tweet) {
	storeTweetInDB(tweet, "\$MAR");
});

stream.on('channels/keywords_atvi', function(tweet) {
	storeTweetInDB(tweet, "\$ATVI");
});

stream.on('channels/keywords_ed', function(tweet) {
	storeTweetInDB(tweet, "\$ED");
});

stream.on('channels/keywords_fisv', function(tweet) {
	storeTweetInDB(tweet, "\$FISV");
});

stream.on('channels/keywords_cern', function(tweet) {
	storeTweetInDB(tweet, "\$CERN");
});

stream.on('channels/keywords_mhk', function(tweet) {
	storeTweetInDB(tweet, "\$MHK");
});

stream.on('channels/keywords_msi', function(tweet) {
	storeTweetInDB(tweet, "\$MSI");
});
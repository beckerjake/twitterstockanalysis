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
	return str == 'true' ? true : false;
}

function storeTweetInDB(twt) {
	if (twt['lang'] == 'en') {
		var pkey = twt['id_str'];
		var text = twt['text'];
		var user = twt['user']['id_str'];
		var name = twt['user']['name'];
		var username = twt['user']['screen_name'];
		var loc = twt['user']['location'];
		var description = twt['user']['description'];
		var protectd = getBoolVal(twt['user']['protected']);
		var verified = getBoolVal(twt['user']['verified']);
		var followers_count = parseInt(twt['user']['followers_count']);
		var friends_count = parseInt(twt['user']['friends_count']);
		var listed_count = parseInt(twt['user']['listed_count']);
		var favourites_count = parseInt(twt['user']['favourites_count']);
		var statuses_count = parseInt(twt['user']['statuses_count']);
		var possibly_sensitive = getBoolVal(twt['possibly_sensitive']);
		var timestamp = parseInt(twt['timestamp']) / 1000;		// convert ms to s

	/*
	connection.query('INSERT INTO stocks (issuer_name, symbol, price, ts, time_alt, `change`, chg_percent, day_high, day_low, year_high, year_low, type, volume) VALUES (\''+issuer_name+'\',\''+symbol+'\','+price+','+ts+',FROM_UNIXTIME(\''+time_alt+'\'),'+change+','+chg_percent+','+day_high+','+day_low+','+year_high+','+year_low+',\''+type+'\','+volume+')', function(err, rows, data) {
			                if (err) {
									                    console.log(err);
														                }
																		            });
	*/
	}
}

client.stream('statuses/filter', {track: '\$BA, \$UNH, \$WFC, \$T, \$BP, \$PCG, \$KO, \$IBM, \$MSFT, \$MAR, \$ATVI, \$ED, \$FISV, \$CERN, \$MHK, \$MSI'}, function(stream) {
	stream.on('data', function(tweet) {
        storeTweetInDB(tweet);
   	});
    
    stream.on('error', function(error) {
		connection.end();
        throw error;
    });
});


// https://www.npmjs.com/package/twitter

var Twitter = require('twitter');

var client = new Twitter({
   consumer_key: process.env.TWITTER_CONSUMER_KEY,
   consumer_secret: process.env.TWITTER_CONSUMER_SECRET,
   access_token_key: process.env.TWITTER_ACCESS_TOKEN_KEY,
   access_token_secret: process.env.TWITTER_ACCESS_TOKEN_SECRET
});

//var stocksToTrack = ['\$BA', '\$UNH', '\$WFC', '\$T', '\$BP', '\$PCG', '\$KO', '\$IBM', '\$MSFT', '\$MAR'];

function storeTweetInDB(sym, twt) {
	console.log(sym + ": " + twt.text);
}

client.stream('statuses/filter', {track: '\$BA'}, function(stream) {
	stream.on('data', function(tweet) {
        storeTweetInDB('\$BA', tweet);
   	});
    
    stream.on('error', function(error) {
        throw error;
    });
});

client.stream('statuses/filter', {track: '\$UNH'}, function(stream) {
	stream.on('data', function(tweet) {
		storeTweetInDB('\$UNH', tweet);
	}); 

	stream.on('error', function(error) {
		throw error;
	}); 
});
/*
client.stream('statuses/filter', {track: '\$WFC'}, function(stream) {
	stream.on('data', function(tweet) {
		storeTweetInDB('\$WFC', tweet);
	}); 

	stream.on('error', function(error) {
		throw error;
	}); 
}); 

client.stream('statuses/filter', {track: '\$T'}, function(stream) {
	stream.on('data', function(tweet) {
		storeTweetInDB('\$T', tweet);
	}); 

	stream.on('error', function(error) {
		throw error;
	});
}); 

client.stream('statuses/filter', {track: '\$BP'}, function(stream) {
	stream.on('data', function(tweet) {
		storeTweetInDB('\$BP', tweet);
	}); 

	stream.on('error', function(error) {
		throw error;
	}); 
}); 

client.stream('statuses/filter', {track: '\$PCG'}, function(stream) {
	stream.on('data', function(tweet) {
		storeTweetInDB('\$PCG', tweet);
	}); 

	stream.on('error', function(error) {
		throw error;
	});
}); 

client.stream('statuses/filter', {track: '\$KO'}, function(stream) {
	stream.on('data', function(tweet) {
		storeTweetInDB('\$KO', tweet);
	}); 

	stream.on('error', function(error) {
		throw error;
	}); 
}); 

client.stream('statuses/filter', {track: '\$IBM'}, function(stream) {
	stream.on('data', function(tweet) {
		storeTweetInDB('\$IBM', tweet);
	}); 

	stream.on('error', function(error) {
		throw error;
	});
});

client.stream('statuses/filter', {track: '\$MSFT'}, function(stream) {
	stream.on('data', function(tweet) {
		storeTweetInDB('\$MSFT', tweet);
	});

	stream.on('error', function(error) {
		throw error;
	});
});

client.stream('statuses/filter', {track: '\$MAR'}, function(stream) {
	stream.on('data', function(tweet) {
		storeTweetInDB('\$MAR', tweet);
	});

	stream.on('error', function(error) {
	      throw error;
    });
});*/

#!/usr/local/bin/node

var request = require('request')
var mysql = require('mysql')

var connection = mysql.createConnection({
	host: 'localhost',
	user: 'root',
	password: process.env.MYSQL_PASSWD,
	database: 'ticktalk'
	});

connection.connect();

var url = "http://finance.yahoo.com/webservice/v1/symbols/BA,UNH,WFC,T,BP,PCG,KO,IBM,MSFT,MAR/quote?format=json&view=detail"

request({
	url: url,
	json: true
}, function(error, response, body) {
	if (!error && response.statusCode === 200) {
		var stockDataList = body["list"]["resources"];
		for (var i = 0; i < stockDataList.length; i++) {
			var fields = stockDataList[i]["resource"]["fields"];

			var issuer_name = fields["issuer_name"];
			var symbol = fields["symbol"];
			var price = parseFloat(fields["price"]);
			var ts = parseInt(fields["ts"]);
			var time_alt = fields["ts"];
			var change = parseFloat(fields["change"]);
			var chg_percent = parseFloat(fields["chg_percent"]);
			var day_high = parseFloat(fields["day_high"]);
			var day_low = parseFloat(fields["day_low"]);
			var year_high = parseFloat(fields["year_high"]);
			var year_low = parseFloat(fields["year_low"]);
			var type = fields["type"];
			var volume = parseInt(fields["volume"]);

			connection.query('INSERT INTO stocks (issuer_name, symbol, price, ts, time_alt, `change`, chg_percent, day_high, day_low, year_high, year_low, type, volume) VALUES (\''+issuer_name+'\',\''+symbol+'\','+price+','+ts+',FROM_UNIXTIME(\''+time_alt+'\'),'+change+','+chg_percent+','+day_high+','+day_low+','+year_high+','+year_low+',\''+type+'\','+volume+')', function(err, rows, data) {
				if (err) {
					console.log("Error inserting stock data into database.");
					console.log(err);			
				}
			});
		
			if (i == stockDataList.length - 1) {
				connection.end();
			}
		}
	}
});


#!/usr/local/bin/node

var request = require("request")

var url = "http://finance.yahoo.com/webservice/v1/symbols/BA,UNH,WFC,T,BP,PCG,KO,IBM,MSFT,MAR/quote?format=json&view=detail"

request({
	url: url,
	json: true
}, function(error, response, body) {
	if (!error && response.statusCode === 200) {
		var stockDataList = body["list"]["resources"];
		for (var i = 0; i < stockDataList.length; i++) {
			var fields = stockDataList[i]["resource"]["fields"];
			console.log(fields["name"] + ": " + fields["price"]);
		}
	}
})



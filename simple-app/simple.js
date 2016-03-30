var http = require('http');

var request = require("request");

var server = http.createServer(function (req, res) {
    res.writeHead(200, {"Content-Type": "text/plain"});

    request({
        uri: 'http://localhost:8080/sample',
        method: 'GET',
        maxRedirects:3
    }, function(error, response, body) {
        if (!error) {
        	res.write(body)
            res.write(response.statusCode.toString());
        } else {
            //response.end(error);
            res.write(error);
        }
    });     

    res.end();
});
server.listen(3000);
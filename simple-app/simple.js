var http = require('http');

var request = require("request");

request({
  uri: "http://10.67.79.47:8080/sample",
  method: "GET",
  timeout: 10000,
  followRedirect: true,
  maxRedirects: 10
}, function(error, response, body) {
  console.log(body);
});


var server = http.createServer(function(req, res) {
  res.writeHead(200);
  res.end(request);
});



server.listen(3000);
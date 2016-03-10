# http-server
This is project creates two sockets that communicate with each other using HTTP. 


AUTHORS <br>
Norton Pengra http://github.com/qwergram


Iris Carrera http://github.com/icarrera

##client.py
Our client sends requests to our server. User inputs an HTTP request. 

##server.py
Our server accepts requests from our client and sends responses that follow HTTP. Before accepting HTTP requests, our server verifies and parses the first line and headers of the HTTP request sent by the client with a parse_request function. If the method is GET and the HTTP version is HTTP/1.1, our server returns the URI. Otherwise, an appropriate Python error is raised and an HTTP 4xx or 5xx status code is displayed. We created a parse_headers function to verify and parse the headers are in the format of Header Key: Header Value. If the HTTP headers are in the correct format, we return parsed_headers for use in the parse_request function. Otherwise, we raise a KeyError and a 400 status code is displayed. If the HTTP request is accepted, the server replies with a 200 status code.




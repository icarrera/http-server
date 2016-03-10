# -*-coding:utf-8-*-
"""Handle server operations of reading incoming streams and echoing them"""
import socket

buffer_length = 1024
PORT = 5006


def setup_server():
    """Build a socket object on localhost and specified port"""
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    server.bind((u'127.0.0.1', PORT))
    server.listen(1)
    return server


def server_listen(server):
    """Accept connections from the client"""
    conn, addr = server.accept()
    return (conn, addr)


def server_read(connection):
    """Read and parse message from client"""

    string = ''.encode('utf-8')
    while True:
        part = connection.recv(buffer_length)
        string += part
        if len(part) < buffer_length or len(part) == 0:
            break
    return string.decode('utf-8')


def parse_request(request):
    """Parses our HTTP request."""
    # Python built-in library names the first line of the request request_line
    request_line = request.split('\n')[0]
    request_line = request_line.strip()
    method, uri, version = request_line.split()
    if method.upper() != 'GET':
        raise TypeError('Error 405: Method Not Allowed')
    if version.upper().split('/')[0] != 'HTTP':
        raise TypeError('Error 400: Bad Request')
    if version.upper().split('/')[1] != '1.1':
        raise ValueError('Error 505: Invalid HTTP Version')
    return uri


def parse_headers(request):
    """Validates and parses the headers of our HTTP request."""
    parsed_headers = {}
    http_header = request.replace('\r', '').split('\n')[1:]
    idx = http_header.index('')
    http_header = http_header[:idx]
    for header in http_header:
        if not len(header.split(': ')) == 2:
            raise SyntaxError('Error 400: Bad Request')
        header_key, header_value = header.split(': ')
        parsed_headers[header_key] = header_value
    return parsed_headers


def server_response(string, connection):
    """Send back specified string to specified connection"""
    connection.send(string.encode('utf-8'))


def response_ok():
    """Send back an HTTP 200 OK status message"""
    return "HTTP/1.1 200 OK<CRLF>\n.<CRLF>\r\n\r\n"


def response_error(code=500, message="Whoops! Something Broke."):
    """Send back an HTTP 500 error message"""
    if code == 500:
        image = "<img src=\"https://s3.amazonaws.com/images.seroundtable.com/t-google-404-1299071983.jpg\"><h1> 500 ERROR!</h1>"
    else:
        image = ""
    return "HTTP/1.1 {} {}\n.<CRLF>\r\nContent-type: text/html\r\n\r\n{}".format(code, message, image)


def server():
    """Main server loop"""
    try:
        socket = setup_server()
        while True:
            connection, address = socket.accept()
            try:
                result = server_read(connection)
                parse_request(result)
                print("log:", result)
                to_send = response_ok() + result
                server_response(to_send, connection)
            except:
                server_response(response_error(), connection)
    except KeyboardInterrupt:
        print("Closing the server!")
        try:
            connection.close()
        except NameError:
            pass
    finally:
        socket.close()

if __name__ == "__main__":
    server()

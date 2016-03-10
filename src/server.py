# -*-coding:utf-8-*-
"""Handle server operations of reading incoming streams and echoing them"""
import socket

buffer_length = 1024
PORT = 5002


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
    method, url, version = request_line.split()
    if method.upper() != 'GET':
        raise TypeError('Error 405: Method Not Allowed')
    if version.upper().split('/')[0] != 'HTTP':
        raise TypeError('Error 400: Bad Request')
    if version.upper().split('/')[1] != '1.1':
        raise ValueError('Error 505: Invalid HTTP Version')


def parse_headers(request):
    """Validates and parses the headers of our HTTP request."""
    http_






def server_response(string, connection):
    """Send back specified string to specified connection"""
    connection.send(string.encode('utf-8'))


def response_ok():
    """Send back an HTTP 200 OK status message"""
    return "HTTP/1.1 200 OK<CRLF>\n.<CRLF>\r\n\r\n"


def response_error():
    """Send back an HTTP 500 error message"""
    return "HTTP/1.1 500 Internal Server Error\n.<CRLF>\r\n\r\n"


def server():
    """Main server loop"""
    try:
        socket = setup_server()
        while True:
            connection, address = socket.accept()
            try:
                result = server_read(connection)
                print("log:", result)
                to_send = response_ok() + result
                server_response(to_send, connection)
            except:
                server_response(response_error(), connection)
    except KeyboardInterrupt:
        print("Closing the server!")
    finally:
        socket.close()

if __name__ == "__main__":
    server()

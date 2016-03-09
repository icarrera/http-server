# -*-coding:utf-8-*-
"""Handle server operations of reading incoming streams and echoing them"""
import socket

buffer_length = 1024
PORT = 5001


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

    # XXX 3/6/16
    # What we should've done was exclude the if statement and call server_response()
    # REGARDLESS of whether we've recieved the whole message or not, because
    # We don't care, we just want to echo immediately.

    string = ''.encode('utf-8')
    while True:
        part = connection.recv(buffer_length)
        string += part
        if len(part) < buffer_length or len(part) == 0:
            break
    return string.decode('utf-8')


def server_response(string, connection):
    """Send back specified string to specified connection"""
    connection.send(string.encode('utf-8'))


def response_ok():
    """Send back an HTTP 200 OK status message"""
    return "HTTP/1.1 200 OK<CRLF>\n.<CRLF>\n\n"


def response_error():
    """Send back an HTTP 500 error message"""
    return "HTTP/1.1 500 Internal Server Error\n.<CRLF>\n\n"


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

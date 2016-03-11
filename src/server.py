# -*-coding:utf-8-*-
"""Handle server operations of reading incoming streams and echoing them"""
import socket
import os
import io
import sys

buffer_length = 1024
PORT = 5000
IP = "0.0.0.0"

ROOT = "./webroot/"


def setup_server():
    """Build a socket object on localhost and specified port"""
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    server.bind((IP, PORT))
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
    # raise ValueError("404: Not Found")
    print([request])
    request_line = request.split('\n')[0]
    request_line = request_line.strip()
    try:
        method, uri, version = request_line.split()
    except ValueError:
        raise SyntaxError('400: Bad Request (6)')
    if method.upper() != 'GET':
        raise TypeError('405: Method Not Allowed')
    if version.upper().split('/')[0] != 'HTTP':
        raise TypeError('400: Bad Request (5)')
    if version.upper().split('/')[1] != '1.1':
        raise ValueError('505: Invalid HTTP Version')
    headers = parse_headers(request)
    content, mime = resolve_uri(uri)
    return (content, mime)


def parse_headers(request):
    """Validates and parses the headers of our HTTP request."""
    parsed_headers = {}
    http_header = request.replace('\r', '').split('\n')[1:]
    if not http_header:
        raise KeyError("400: Bad Request (3)")
    idx = http_header.index('')
    http_header = http_header[:idx]
    for header in http_header:
        if not len(header.split(': ')) == 2:
            raise SyntaxError('400: Bad Request (2)')
        header_key, header_value = header.split(': ')
        parsed_headers[header_key.lower()] = header_value
    if not parsed_headers.get('host'):
        raise KeyError("400: Bad Request (1)")
    return parsed_headers


def server_response(string, connection):
    """Send back specified string to specified connection"""
    connection.send(string.encode('utf-8'))


def response_ok(content, tag):
    """Send back an HTTP 200 OK status message"""
    return ("HTTP/1.1 200 OK\r\nContent-type: {}\r\n\r\n{}".format(tag, content))


def response_error(code=500, message="Whoops! Something Broke."):
    """Send back an HTTP 500 error message"""
    if code == 500:
        image = "<img src=\"https://s3.amazonaws.com/images.seroundtable.com/t-google-404-1299071983.jpg\"><h1> 500 ERROR!</h1>"
    else:
        image = ""
    return "HTTP/1.1 {} {}\r\nContent-type: text/html\r\n\r\n{}".format(code, message, image)

def directory_response(path):
    """Returns listing of that directory."""
    html_return = "<ul>"
    for node in os.listdir(path):
        print(path)
        if os.path.isdir(os.path.join(path, node)):
            html_return += "<a href=\"{}/\"><li>{}</li></a>".format(node, node)
        else:
            html_return += "<a href=\"{}\"><li>{}</li></a>".format(node, node)
    html_return += "</ul>"
    return (html_return, "text/html")


def file_response(path):
    """Returns file."""
    try:
        with io.open(path) as f:
            content = f.read()
        return (content, "text/{}".format(os.path.splitext(path)[-1][1:]))
    except Exception as e:
        sys.exit(e)
        raise IOError("404: Not Found")


def resolve_uri(uri):
    """Resolves our uri."""
    path = os.path.join(ROOT, uri[1:])
    if os.path.isdir(path):
        return directory_response(path)
    elif os.path.isfile(path):
        return file_response(path)
    else:
        print("404: Not Found")
        raise IOError("404: Not Found")


def server():
    """Main server loop."""
    try:
        socket = setup_server()
        while True:
            connection, address = socket.accept()
            try:
                result, mime = parse_request(server_read(connection))
                print("log:", result)
                to_send = response_ok(result, mime)
                server_response(to_send, connection)
            except Exception as error:
                try:
                    error = error.args[0]
                    code = int(error.split(':')[0])
                    error = error.split(':')[1].strip()
                except:
                    code = 500
                    error = "Server Error"
                server_response(response_error(code, error), connection)
            finally:
                connection.close()
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

# -*- coding: utf-8 -*-
from gevent.server import StreamServer
from gevent.monkey import patch_all
import sys
from server import parse_request, server_read, response_ok, server_response, response_error

IP = '127.0.0.1'
PORT = int(sys.argv[1])

def server_handler(connection, address):
    """Handles the gevent StreamServer for individual clients."""
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

if __name__ == "__main__":
    patch_all()
    server = StreamServer((IP, PORT), server_handler)
    server.serve_forever()

# -*-coding:utf-8-*-
from __future__ import unicode_literals
import socket


buffer_length = 4
PORT = 5000


def setup_server():
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    server.bind((u'127.0.0.1', PORT))
    server.listen(1)
    return server


def server_listen(server):
    conn, addr = server.accept()
    return (conn, addr)


def server_read(connection):
    string = ''.encode('utf-8')
    while True:
        print("readings")
        part = connection.recv(buffer_length)
        print(len(part))
        string += part
        if len(part) < buffer_length or len(part) == 0:
            print("breaking")
            break
    return (string.decode('utf-8'), connection)


def server_echo(string, connection):
    # stream_info = [i for i in socket.getaddrinfo('127.0.0.1', PORT) if i[1] == socket.SOCK_STREAM[0]]
    # connection.connect(('127.0.0.1', PORT))
    connection.send(string.encode('utf-8'))


def server():
    try:
        socket = setup_server()
        while True:
            connection, address = server_listen(socket)
            result, connection = server_read(connection)
            server_echo(result, connection)
    except KeyboardInterrupt:
        print("Closing the server!")
    finally:
        socket.close()

if __name__ == "__main__":
    server()

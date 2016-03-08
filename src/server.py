# -*-coding:utf-8-*-
import socket

buffer_length = 1024

def setup_server():
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    server.bind(('127.0.0.1', 5000))
    server.listen(1)
    return server

def server_listen(server):
    conn, addr = server.accept()
    return (conn, addr)

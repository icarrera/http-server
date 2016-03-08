# -*-coding:utf-8-*-
# from __future__ import unicode_literals
import socket
import sys


buffer_length = 4

PORT = 5000


def setup_socket():
    info = socket.getaddrinfo('127.0.0.1', PORT)
    return [i for i in info if i[1] == socket.SOCK_STREAM][0]


def build_client(socket_details):
    client = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    client.settimeout(1)
    return client


def send_message(socket, message):
    socket.connect(('127.0.0.1', PORT))
    socket.sendall(scrub_message(message))


def scrub_message(message):
    if len(message) % buffer_length == 0:
        message += '\r'
    if hasattr(message, "decode"):
        return message.decode('utf-8').encode('utf-8')
    else:
        return message.encode('utf-8')



def get_reply(client):
    chunks = []
    while True:
        chunk = client.recv(buffer_length)
        # client = client.accept()
        chunk = chunk
        chunks.append(chunk)
        if len(chunk) < buffer_length or len(chunk) == 0:
            return (b''.join(chunks)).decode('utf-8').replace('\r', '')


def close(socket):
    socket.close()


def client(message):
    client = build_client(setup_socket())
    try:
        send_message(client, message)
        echo = get_reply(client)
    finally:
        close(client)

    print(echo)
    # print(len(echo))
    return echo

if __name__ == "__main__":
    client(sys.argv[1])

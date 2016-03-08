# -*-coding:utf-8-*-
import socket
import sys

buffer_length = 1024

PORT = 5002


def setup_socket():
    info = socket.getaddrinfo('127.0.0.1', PORT)
    return [i for i in info if i[1] == socket.SOCK_STREAM][0]


def build_client(socket_details):
    return socket.socket(socket.AF_INET,
                         socket.SOCK_STREAM,
                         socket.IPPROTO_TCP)


def send_message(socket, message):
    socket.connect(('127.0.0.1', PORT))
    socket.sendall(message.encode('utf-8'))


def get_reply(client):
    chunks = []
    while True:
        chunk = client.recv(buffer_length).decode('utf-8')
        chunks.append(chunk)
        if len(chunk) < buffer_length or len(chunk) == 0:
            return ''.join(chunks)


def close(socket):
    socket.close()


def client(message):
    client = build_client(setup_socket())
    try:
        send_message(client, message)
        echo = get_reply(client)
        print(echo)
    finally:
        close(client)

if __name__ == "__main__":
    client(sys.argv[1])

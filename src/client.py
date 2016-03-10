# -*-coding:utf-8-*-
"""Handle client operations of building a client and recieving messages from server"""
import socket
import sys


buffer_length = 1024

PORT = 5005


def setup_socket():
    """Gather required information for building a socket object"""
    info = socket.getaddrinfo('127.0.0.1', PORT)
    return [i for i in info if i[1] == socket.SOCK_STREAM][0]


def build_client(socket_details):
    """Use given information to build a socket object"""
    client = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    client.settimeout(1)
    return client


def send_message(socket, message):
    """Send a scrubbed message to the server"""
    socket.connect(('127.0.0.1', PORT))
    socket.sendall(message)


def scrub_message(message):
    """Take the text, and depending if it's python3 or 2, encode it into utf-8"""
    if not isinstance(message, str):
        raise TypeError("Message must be string!")
    if len(message) % buffer_length == 0:
        message += '\r'
    if hasattr(message, "decode"):
        return message.decode('utf-8').encode('utf-8')
    else:
        return message.encode('utf-8')


def get_reply(client):
    """Get reply from the server"""
    chunks = []
    while True:
        chunk = client.recv(buffer_length)
        chunks.append(chunk)
        if len(chunk) < buffer_length or len(chunk) == 0:
            return (b''.join(chunks)).decode('utf-8').replace('\r', '')


def close(socket):
    """Close socket gracefully"""
    socket.close()


def client(message):
    """Main functionality of building a client and echoing return value"""
    message = scrub_message(message)
    client = build_client(setup_socket())
    try:
        send_message(client, message)
        echo = get_reply(client)
    finally:
        close(client)

    print(echo)
    return echo

if __name__ == "__main__":
    client(sys.argv[1])

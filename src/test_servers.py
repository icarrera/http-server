# -*- coding: utf-8 -*-
# import pytest
import client
import pytest

HTTP_RESPONSE_CODE = "HTTP/1.1 200 OK"

def test_reply_with_strings():
    """Test if echo is same text that was sent"""
    assert client.client("GET /test/ HTTP/1.1\r\nHost: localhost\r\n\r\n").startswith("HTTP/1.1 404")


def test_reply_with_non_strings():
    """Test if nonstring objects passed into client raise TypeError"""
    with pytest.raises(TypeError):
        client.client(123567890)


def test_buffer_minus_one():
    """Test if echo is same text that was sent if len(message) is buffer_length - 1"""
    message = "a" * 1023
    assert client.client("GET " + message + " HTTP/1.1\r\nHost: localhost\r\n\r\n").startswith("HTTP/1.1 404")


def test_several_buffers():
    """Test if echo is same text that was sent if len(message) is a multiple of buffer_length"""
    message = ("a" * 1024) + ("b" * 1024)
    assert client.client("GET " + message + " HTTP/1.1\r\nHost: localhost\r\n\r\n").startswith("HTTP/1.1 404")


def test_non_ascii():
    """Test if echo is same text that was sent if message contains non-ascii character"""

    message = u"¡¢"

    # hasattr() determines the python version, if the string has the ability
    # to be decoded, then we are running python2 and requires the string to be
    # decoded and encoded.

    if hasattr(message, "decode"):
        with pytest.raises(TypeError):
            assert client.client("GET " + message + " HTTP/1.1\r\nHost: localhost\r\n\r\n").startswith(HTTP_RESPONSE_CODE).decode('utf-8')
    else:
        client.client("GET " + message + " HTTP/1.1\r\nHost: localhost\r\n\r\n").startswith("HTTP/1.1 404")


def test_400():
    """Tests 505 Response Code."""
    assert client.client("hlkjlkkjl").startswith("HTTP/1.1 400")


def test_505():
    """Tests 505 Response Code."""
    assert client.client("GET /index.html HTTP/0.999").startswith("HTTP/1.1 505")


def test_200():
    """Tests 200 Response Code."""
    assert client.client("GET /sample.txt HTTP/1.1\r\nHost: localhost\r\n").startswith("HTTP/1.1 200")


def test_directory_response():
    from server import directory_response
    assert "<li>" in directory_response('/')[0]


def test_file_response():
    from server import file_response
    assert b"This is" in file_response('./webroot/sample.txt')[0]

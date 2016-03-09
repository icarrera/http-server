# -*- coding: utf-8 -*-
# import pytest
import client
import pytest

HTTP_RESPONSE_CODE = "HTTP/1.1 200 OK<CRLF>\n.<CRLF>\n"

STRINGS = [
    "Waffles",
    "",
    "f" * 1024,
]

NON_STRINGS = [
    1,
    {"asdfasdg": 7},
    5.42,
    object,
    ("luluz,", ),
    client.client
]

NON_ASCII = [
    "£500 worth of waffles",
    "¡Hola!",
    "I lost 5¢",
    "Get ¥24000",
    "copyright©Microsoft",
    "Test passed in 5µs",
]


@pytest.mark.parametrize("message,", STRINGS)
def test_reply_with_strings(message):
    """Test if echo is same text that was sent"""
    assert client.client(message) == HTTP_RESPONSE_CODE + message


@pytest.mark.parametrize("message,", NON_STRINGS)
def test_reply_with_non_strings(message):
    with pytest.raises(TypeError):
        client.client(message)


def test_buffer_minus_one():
    """Test if echo is same text that was sent if len(message) is buffer_length - 1"""
    message = "a" * 1023
    assert client.client(message) == HTTP_RESPONSE_CODE + message


def test_several_buffers():
    """Test if echo is same text that was sent if len(message) is a multiple of buffer_length"""
    message = ("a" * 1024) + ("b" * 1024)
    assert client.client(message) == HTTP_RESPONSE_CODE + message


@pytest.mark.parametrize("message,", NON_ASCII)
def test_non_ascii(message):
    """Test if echo is same text that was sent if message contains non-ascii character"""

    # hasattr() determines the python version, if the string has the ability
    # to be decoded, then we are running python2 and requires the string to be
    # decoded and encoded.

    if hasattr(message, "decode"):
        assert client.client(message) == HTTP_RESPONSE_CODE + message.decode('utf-8')
    else:
        assert client.client(message) == HTTP_RESPONSE_CODE + message

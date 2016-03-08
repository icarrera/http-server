# -*- coding: utf-8 -*-
# import pytest
import client


def test_echo_is_identical():
    message = "500 worth of waffles"
    assert client.client(message) == message


def test_buffer_minus_one():
    message = "a" * 1023
    assert client.client(message) == message


def test_several_buffers():
    message = ("a" * 1024) + ("b" * 1024)
    assert client.client(message) == message


def test_non_ascii():
    message = "£500 worth of waffles"

    # hasattr determines the python version, if the string has the ability
    # to be decoded, then we are running python2 and requires the string to be
    # decoded and encoded.

    if hasattr(message, "decode"):
        assert client.client(message) == message.decode('utf-8')
    else:
        assert client.client(message) == message

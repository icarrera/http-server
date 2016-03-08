# -*- coding: utf-8 -*-
# import pytest
import client


def test_echo_is_identical():
    """Test if echo is same text that was sent"""
    message = "500 worth of waffles"
    assert client.client(message) == message


def test_buffer_minus_one():
    """Test if echo is same text that was sent if len(message) is buffer_length - 1"""
    message = "a" * 1023
    assert client.client(message) == message


def test_several_buffers():
    """Test if echo is same text that was sent if len(message) is a multiple of buffer_length"""
    message = ("a" * 1024) + ("b" * 1024)
    assert client.client(message) == message


def test_non_ascii():
    """Test if echo is same text that was sent if message contains non-ascii character"""
    message = "£500 worth of waffles"

    # hasattr() determines the python version, if the string has the ability
    # to be decoded, then we are running python2 and requires the string to be
    # decoded and encoded.

    if hasattr(message, "decode"):
        assert client.client(message) == message.decode('utf-8')
    else:
        assert client.client(message) == message

import typing
import unittest

from usage_parser import UsageParser

class TestNormalUsage(unittest.TestCase):
    '''UsageParser.parse: Given a single string => Given an ID that does not end with 4 or 6'''

    input: str
    expected: typing.List[typing.Mapping[str, typing.Any]]

    def setUp(self):
        self.input = '7291,293451'
        self.expected = [
            dict(
                id=7291,
                bytes_used=293451,
                cellid=None,
                dmcc=None,
                ip=None,
                mnc=None,
            ),
        ]


    def test_return_basic_string_data(self):
        '''Then it will return basic string data'''
        self.assertListEqual(
            UsageParser.parse(self.input),
            self.expected
        )

class TestExtendedUsage(unittest.TestCase):
    '''UsageParser.parse: Given a single string => Given an ID that ends with 4'''

    input: str
    expected: typing.List[typing.Mapping[str, typing.Any]]

    def setUp(self):
        self.input = '7194,b33,394,495593,192'
        self.expected = [
            dict(
                id=7194,
                bytes_used=495593,
                cellid=192,
                dmcc='b33',
                ip=None,
                mnc=394,
            ),
        ]


    def test_return_extended_string_data(self):
        '''Then it will return extended string data'''
        self.assertListEqual(
            UsageParser.parse(self.input),
            self.expected
        )

class TestHexUsage(unittest.TestCase):
    '''UsageParser.parse: Given a single string => Given an ID that ends with 6'''

    input: str
    expected: typing.List[typing.Mapping[str, typing.Any]]

    def setUp(self):
        self.input = '316,0e893279227712cac0014aff'
        self.expected = [
            dict(
                id=316,
                bytes_used=12921,
                cellid=578228938,
                dmcc=None,
                ip='192.1.74.255',
                mnc=3721,
            ),
        ]


    def test_return_hex_string_data(self):
        '''Then it will return hex string data'''
        self.assertListEqual(
            UsageParser.parse(self.input),
            self.expected
        )

class TestStringArray(unittest.TestCase):
    '''UsageParser.parse: Given an array of strings'''

    input: typing.List[str]
    expected: typing.List[typing.Mapping[str, typing.Any]]

    def setUp(self):
        self.input = [
            '4,0d39f,0,495594,214',
            '16,be833279000000c063e5e63d',
            '9991,2935',
        ]

        self.expected = [
            dict(
                id=4,
                bytes_used=495594,
                cellid=214,
                dmcc='0d39f',
                ip=None,
                mnc=0,
            ),
            dict(
                id=16,
                bytes_used=12921,
                cellid=192,
                dmcc=None,
                ip='99.229.230.61',
                mnc=48771,
            ),
            dict(
                id=9991,
                bytes_used=2935,
                cellid=None,
                dmcc=None,
                ip=None,
                mnc=None,
            ),
        ]

    def test_return_all_string_data(self):
        '''Then it will parse each string according to its ID and return an array of data'''
        self.assertListEqual(
            UsageParser.parse(*self.input),
            self.expected
        )

class TestFailureUsage(unittest.TestCase):
    '''UsageParser.parse: Given an invalid input handle the scenario correctly'''

    input: str
    expected: typing.List[typing.Mapping[str, typing.Any]]

    def setUp(self):
        self.input = '7291293451'
        self.expected = []


    def test_return_basic_string_data(self):
        '''Then it will return basic string data'''
        self.assertListEqual(
            UsageParser.parse(self.input),
            self.expected
        )

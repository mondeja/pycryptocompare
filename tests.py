#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from pycryptocompare import CryptoCompare

from time import time
from pprint import pprint

""" ###########################################
    ############  POLONIEX TESTS  #############
    ###########################################
"""

class TestCryptoCompare(unittest.TestCase):
    """
    Integration tests for CryptoCompare commands. These will fail 
    in the absence of an internet connection or if CryptoCompare API goes down.
    """
    def setUp(self):
        self.cc = CryptoCompare()

    """ ###########################################
        #############  INFO METHODS  ##############
        ###########################################
    """

    def test_documentation(self):
        actual = self.cc.documentation()
        self.assertIs(type(actual), dict)

        # With functions
        actual = self.cc.documentation(func=self.cc.generate_avg)
        self.assertIs(type(actual), dict)

    def test_stats(self):
        actual = self.cc.server_stats()
        self.assertIs(type(actual), dict)

    def test_rate_calls(self):
        periods = ("all", "hour", "second")

        for period in periods:
            actual = self.cc.rate_calls(period)
            self.assertIn(type(actual), (list, dict))

    def test_cache_duration(self):
        actual = self.cc.cache_duration(self.cc.price)
        self.assertIs(type(actual), self.cc.parse_int)
        

    """ ###########################################
        #############  DATA METHODS  ##############
        ###########################################
    """

    def test_coin_list(self):
        actual = self.cc.coin_list(["BTC", "ETH"])
        self.assertIs(type(actual), dict)

    def test_price(self):
        calls = [
            ("BTC", "ETH"),
            ("BTC", "ETH, USD"),
            (["BTC", "ETH"], "EUR"),
            ("BTC,ETH", ["EUR", "CNY"])
        ]
        for full in (True, False):
            for params in calls:
                actual = self.cc.price(*params, full=full)
                self.assertIs(type(actual), dict)

    def test_generate_avg(self):
        calls = [
            ("BTC", "USD", "Poloniex"),
            ("BTC", "USD", ["Poloniex"]),
        ]
        for params in calls:
            actual = self.cc.generate_avg(*params)
            self.assertIs(type(actual), dict)
            self.assertIn(list(actual.keys()), 
                               (["DISPLAY", "RAW"], 
                                   ["RAW", "DISPLAY"]))

    def test_day_avg(self):
        actual = self.cc.day_avg("BTC", "USD", e="Kraken",
                                 avgType="MidHighLow", 
                                 UTCHourDiff=2, 
                                 toTS=int(time() - 60**2*24))
    
    def test_price_historical(self):
        actual = self.cc.price_historical("BTC", "USD",
                                          ts=int(time()-60**2*24*365))
        self.assertIs(type(actual), dict)

    def test_social_stats(self):
        actual = self.cc.social_stats(1182) # BTC
        self.assertIs(type(actual), dict)

    def test_histo(self):
        for period in ("minute", "hour", "day"):
            actual = self.cc.histo(period, "BTC", "EUR")
            self.assertIs(type(actual), dict)

    def test_mining_contracts(self):
        actual = self.cc.mining_contracts()
        self.assertIs(type(actual), dict)

    def test_mining_equipment(self):
        actual = self.cc.mining_equipment()
        self.assertIs(type(actual), dict)

    def test_top_pairs(self):
        actual = self.cc.top_pairs("BTC")
        self.assertIs(type(actual), dict)
        self.assertEqual(len(actual["Data"]), 5)

        actual = self.cc.top_pairs("BTC", limit=20)
        self.assertEqual(len(actual["Data"]), 20)

    def test_top_exchanges(self):
        actual = self.cc.top_exchanges("BTC", "USD", limit=20)
        self.assertIs(type(actual), dict)
        self.assertEqual(len(actual["Data"]), 20)

    def test_top_volumes(self):
        actual = self.cc.top_volumes("BTC")
        self.assertIs(type(actual), dict)
        self.assertEqual(len(actual["Data"]), 50)

    def test_exchanges(self):
        actual = self.cc.exchanges()
        self.assertIs(type(actual), dict)

    def test_news_providers(self):
        actual = self.cc.news_providers()
        self.assertIs(type(actual), list)

    def test_news(self):
        actual = self.cc.news()
        self.assertIs(type(actual), list)

if __name__ == "__main__":
    unittest.main()
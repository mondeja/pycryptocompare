#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from urllib import urlencode as _urlencode
    str = unicode
# python 3
except:
    from urllib.parse import urlencode as _urlencode

from json import loads as _loads
from requests import post as _post
from requests import get as _get
from requests.exceptions import (ConnectionError, 
                                ConnectTimeout,
                                ReadTimeout)

from decimal import Decimal
from re import sub


WEB_URL_ROUTES = [
    "data/coinlist",
    "data/socialstats",
    "data/miningcontracts",
    "data/miningequipment",
]

API_URL_ROUTES = [
    "documentation",
    "stats",
    "stats/rate/hour",
    "stats/rate/second",
    "data/pricemulti",
    "data/pricemultifull",
    "data/generateAvg", 
    "data/dayAvg",
    "data/pricehistorical",
    "data/histominute",
    "data/histohour",
    "data/histoday",
    "data/top/pairs",
    "data/top/exchanges",
    "data/top/volumes",
    "data/all/exchanges",
    "data/news/providers",
    "data/news/",

]

MAP_ROUTES = {
    "documentation": "",
    "stats": "stats",
    "stats/rate/hour": "stats/rate/hour/limit",
    "stats/rate/second": "stats/rate/second/limit",

}
class CryptoCompareError(Exception):
    """
    Exception for catch invalid commands and other repsonses
    that don't match with 200 code responses.
    """ 
    def __init__(self, err):
        print(err)

class CryptoCompare(object):
    """ Main class for retrieve data from coinmarketcap

    :param parse_float: parser used by json.loads() for
        retrieve float type returns (optional, default == Decimal)
    :type parse_float: any

    :param parse_int: parser used by json.loads() for
        retrieve int type returns (optional, default == int) 
    :type parse_int: any

    :param timeout: Timeout getting responses
        (optional, default == 30)
    :type timeout: int

    :return: CryptoCompare object
    :rtype: <class 'cryptocompare.CryptoCompare'>
    """

    def __init__(self, parse_float=Decimal, 
                 parse_int=int, timeout=30):
        self.api_url = "https://min-api.cryptocompare.com/"
        self.web_url = "https://www.cryptocompare.com/api/"
        self.parse_float = parse_float
        self.parse_int = parse_int
        self.timeout = timeout

    def __call__(self, route, args={}):
        """
        Main Api Function
        - raises 'cryptocompare.CryptoCompareError' if the <route> is not valid, or
            if an error is returned from Cryptocompare API
        - returns decoded json api message
        """
        if route in API_URL_ROUTES:
            url = self.api_url
            if route in MAP_ROUTES:
                url += MAP_ROUTES[route]
            else:
                url += route
        elif route in WEB_URL_ROUTES:
            url = self.web_url + route
        else:
            raise CryptoCompareError("Invalid Command!: %s" % command)

        ret = _get(url + "?" + _urlencode(args), timeout=self.timeout)

        jsonout = _loads(ret.text, 
                         parse_float=self.parse_float,
                         parse_int=self.parse_int)

        if "Response" in jsonout:
            if jsonout["Response"] == "Success":
                return jsonout
            else:
                raise CryptoCompareError(jsonout["Message"])
        return jsonout
    
    """ ###########################################
        #############  INFO METHODS  ##############
        ###########################################
    """

    def documentation(self, func=None):
        """
        Get API documentation
        
        Example call:
            ---------------------------------------
            >>> cc = CryptoCompare()
            >>> cc.documentation(func=cc.price)
            ---------------------------------------

        Endpoint:
            https://min-api.cryptocompare.com/

        :param func: You can pass a method for return
            his API documentation. As default, returns
            entire documentation. Only works with 
            format Endpoints of the min-api.
            (optional, defaul == None)
        :type func: function
        """
        response = self.__call__("documentation")
        if not func:
            return response
        else:
            response = response["AvailableCalls"]
            if func == self.price:
                response = response["Price"]
                response = dict(Single=response["Single"],
                                Multi=response["Multi"],
                                MultiFull=response["MultiFull"])
            elif func == self.generate_avg:
                response = response["Price"]["GenerateAvg"]
            elif func == self.day_avg:
                response = response["Price"]["DayAvg"]
            elif func == self.price_historical:
                response = response["Price"]["PriceHistorical"]
            elif func == self.histo:
                response = dict(HistoDay=response["HistoDay"],
                                HistoHour=response["HistoHour"],
                                HistoMinute=response["HistoMinute"])
            elif func == self.top_pairs:
                response = response["TopPairs"]
            elif func == self.top_exchanges:
                response = response["TopExchanges"]
            elif func == self.top_volumes:
                response = response["TopVolumes"]
            elif func == self.exchanges:
                response = response["AllExchanges"]
            elif func == self.news_providers:
                response = response["AllNewsProviders"]
            elif func == self.news:
                response = response["News"]
            else:
                msg = "%s method doesn't appears in API documentation"
                raise ValueError(msg % func.__name__)
        return response

    def server_stats(self):
        """
        Get server state and other information

        Endpoint:
            https://min-api.cryptocompare.com/stats
        """
        return self.__call__("stats")

    def rate_calls(self, period="all"):
        """
        Get made and limit calls by period of time.
        If period == "all", return calls in 
        hour and second periods.

        Endpoint:
            https://min-api.cryptocompare.com/stats/rate/<period>/limit

        Example response:
            [{'hour': {'CallsLeft': {'Histo': 6000, 'News': 30000, 'Price': 150000},
                       'CallsMade': {'Histo': 0, 'News': 0, 'Price': 0},
                       'Message': 'Total Rate limit hour stats'}},
             {'second': {'CallsLeft': {'Histo': 15, 'News': 15, 'Price': 50},
                         'CallsMade': {'Histo': 0, 'News': 0, 'Price': 0},
                         'Message': 'Total Rate limit second stats'}}
            ]

        :param period: Period for retrieve calls stats.
            Valid periods are "hour" and "second".
            (optional, default == "all")
        :type period: str
        """
        valid_periods = ("hour", "second", "all")

        if period not in valid_periods:
            msg = '%s is not a valid period, please select: "all", "hour" or "second"'
            raise ValueError(msg % period)

        if period == "all":
            return [{period: self.__call__("stats/rate/" + period)} \
                       for period in ("hour", "second")]
        else:
            return self.__call__("stats/rate/" + period)

    def cache_duration(self, func):
        """
        Get server cache duration in seconds
        for a method passed as argument

        :param func: Method to retrieve cache duration
        :type func: function
        """
        doc = self.documentation(func=func)
        if func == self.price:
            response = doc["Single"]["Info"]["CacheDuration"]
        else:
            response = doc["Info"]["CacheDuration"]
        return self.parse_int(sub(r"\D", "", response))


    """ ###########################################
        #############  DATA METHODS  ##############
        ###########################################
    """

    def _parse_strlist(self, argName, arg, args):
        """
        Internal function for convert 
        a list into string list comma separated
        and append to args dict of requests.
        Used at multiples methods in the wrapper.
        """
        if not isinstance(arg, list):
            if "," in arg:
                arg = arg.replace(" ", "")
        else:
            arg = ",".join(arg)
        args[argName] = arg
        return args


    def coin_list(self, coins="all"):
        """
        Get general information about all the coins

        Endpoint:
            https://www.cryptocompare.com/api/data/coinlist

        Example response:
            [
                "BTC": {"Id": "1182",
                        "Url": "/coins/btc/overview",
                        "ImageUrl": "/media/19633/btc.png",
                        "Name": "BTC",
                        "Symbol": "BTC",
                        "CoinName": "Bitcoin",
                        "FullName": "Bitcoin (BTC)",
                        "Algorithm": "SHA256",
                        "ProofType": "PoW",
                        "FullyPremined": "0",
                        "TotalCoinSupply": "21000000",
                        "PreMinedValue": "N/A",
                        "TotalCoinsFreeFloat": "N/A",
                        "SortOrder": "1",
                        "Sponsored": false

                    },
                ...
            ]

        :param coins: Coins to retrieve, as default
            retrieve all coins in CryptoCompare.
            Otherwise a single coin in string or 
            list of coin symbols can be used.
        :type coins: list or str

        :return: List of dictionaries containing information 
            for the coins specified by the input. The key of 
            the top dictionary corresponds to the coin symbol.
        :rtype: list
        """
        if not isinstance(coins, list) and coins != 'all':
            coins = [coins]

        data = self.__call__("data/coinlist")["Data"]

        if coins != "all":
            data = {c: data[c] for c in coins}
        
        return data

    def price(self, fsyms, tsyms, e=None, 
              extraParams=None, sign=False,
              tryConversion=True, full=False):
        """
        Get the latest price for a list of 
        one or more currencies. 
        Really fast, 20-60 ms. 
        Cached each 10 seconds in server side.

        Endpoints: 
            https://min-api.cryptocompare.com/data/pricemulti
            https://min-api.cryptocompare.com/data/pricemultifull

        Example responses:
            -------------------------------------------

            price(fsyms="ETH,BTC", tsyms=["BTC","USD","EUR"])
            __________________________________________

            {
                "BTC": {
                    "BTC": 1,
                    "USD": 5726.51,
                    "EUR": 4802.44
                },
                "ETH": {
                    "BTC": 0.05867,
                    "USD": 335.25,
                    "EUR": 280.94
                }
            }
            -------------------------------------------
            
            price(fsyms="ETH", tsyms="BTC")
            __________________________________________
            
            {
                "RAW": {
                    "BTC": {
                        "BTC": {
                            "TYPE": "5",
                            "MARKET": "CCCAGG",
                            "FROMSYMBOL": "ETH",
                            "TOSYMBOL": "ETH",
                            "FLAGS": "4",
                            "PRICE": 1,
                            "LASTUPDATE": 1508094999,
                            "LASTVOLUME": 0,
                            "LASTVOLUMETO": 0,
                            "LASTTRADEID": 0,
                            "VOLUMEDAY": 0,
                            "VOLUMEDAYTO": 0,
                            "VOLUME24HOUR": 0,
                            "VOLUME24HOURTO": 0,
                            "OPENDAY": 1,
                            "HIGHDAY": 1,
                            "LOWDAY": 1,
                            "OPEN24HOUR": 1,
                            "HIGH24HOUR": 1,
                            "LOW24HOUR": 1,
                            "LASTMARKET": "Kraken",
                            "CHANGE24HOUR": 0,
                            "CHANGEPCT24HOUR": 0,
                            "SUPPLY": 16625512,
                            "MKTCAP": 16625512
                        }
                    }
                },
             ...
            }            

            -------------------------------------------

        :param fsyms: From symbols, include multiple symbols
        :type fsyms: list or str

        :param tsyms: To symbols, include multiple symbols
        :param tsyms: list or str

        :return: Dict or dicts (more than one fsyms)
            containing actual prices information from
            one ore more exchanges.
        :rtype: dict

        :param e: Exchange, as default returns 
            CryptoCompare current aggregate for 
            all supported by CryptoCompare.
            See: 
                https://www.cryptocompare.com/coins/guides/how-does-our-cryptocurrecy-index-work/
            For see all available exchanges,
            use the "exchanges" method
            (optional, default == None)
        :type e: str

        :param extraParams: Name of your application
            (optional, default == None)
        :type extraParams: str

        :param sign: If set to true, the server 
            will sign the requests.
            (optional, default == False)
        :type sign: bool

        :param tryConversion: If set to false,
            the server will try to get values 
            without using any conversion at all.
        :type tryConversion: bool

        :param full: If True, returns prices info 
            along with other info like volumes, 
            24 hours high and low prices, 
            market capitalization... and 
            BTC will be used for conversion 
        :type full: bool
        """
        args = dict(sign=sign, 
                    tryConversion=tryConversion,
                    extraParams=extraParams)

        syms_params = (("tsyms", tsyms), ("fsyms", fsyms))
        for name, value in syms_params:
            args = self._parse_strlist(name, value, args)
        
        if e:
            args["e"] = e

        command = "data/pricemulti"
        if full:
            command += "full"

        return self.__call__(command, args)

    def generate_avg(self, fsym, tsym, markets, **kwargs):
        """
        Compute the current trading info 
        (price, vol, open, high, low etc) 
        of the requested pair as a volume 
        weighted average based on 
        the markets requested.

        Endpoint: 
            https://min-api.cryptocompare.com/data/generateAvg

        Example response:
            {'DISPLAY': {'CHANGE24HOUR': 'Ƀ 0.0018',
                         'CHANGEPCT24HOUR': '3.09',
                         'FROMSYMBOL': 'Ξ',
                         'HIGH24HOUR': 'Ƀ 0.06243',
                         'LASTMARKET': 'Poloniex',
                         'LASTTRADEID': '35158987',
                         'LASTUPDATE': 'Just now',
                         'LASTVOLUME': 'Ξ 0.05398',
                         'LASTVOLUMETO': 'Ƀ 0.003240',
                         'LOW24HOUR': 'Ƀ 0.05824',
                         'MARKET': 'CUSTOMAGG',
                         'OPEN24HOUR': 'Ƀ 0.05834',
                         'PRICE': 'Ƀ 0.06014',
                         'TOSYMBOL': 'Ƀ',
                         'VOLUME24HOUR': 'Ξ 144,264.8',
                         'VOLUME24HOURTO': 'Ƀ 8,705.89'},
             'RAW': {'CHANGE24HOUR': Decimal('0.001799999999999996'),
                     'CHANGEPCT24HOUR': Decimal('3.085361672951656'),
                     'FLAGS': 0,
                     'FROMSYMBOL': 'ETH',
                     'HIGH24HOUR': Decimal('0.06243318'),
                     'LASTMARKET': 'Poloniex',
                     'LASTTRADEID': '35158987',
                     'LASTUPDATE': 1508149367,
                     'LASTVOLUME': Decimal('0.05398062'),
                     'LASTVOLUMETO': Decimal('0.00323975'),
                     'LOW24HOUR': Decimal('0.05824126'),
                     'MARKET': 'CUSTOMAGG',
                     'OPEN24HOUR': Decimal('0.05834'),
                     'PRICE': Decimal('0.06014'),
                     'TOSYMBOL': 'BTC',
                     'VOLUME24HOUR': Decimal('144264.78081847998'),
                     'VOLUME24HOURTO': Decimal('8705.892006258466')}
             }


        :param fsym: From symbol
        :type fsym: str

        :param tsym: To symbol
        :param tsym: str

        :param markets: Name of exchanges, 
            for compute average, include multiple.
        :type markets: str or list

        :param **kwargs: See extraParams, sign 
            and tryConversion params in price method

        :return: Volume weighted average based
            on the Exchange for the market selected
        :rtype: dict
        """
        args = dict(**kwargs)
        args["tsym"], args["fsym"] = (tsym, fsym)
        
        args = self._parse_strlist("markets", markets, args)
            
        return self.__call__("data/generateAvg", args)

    def day_avg(self, fsym, tsym, e=None, avgType="HourVWAP",
                UTCHourDiff="0", toTS=None, **kwargs):
        """
        Get day average price. The values 
        are based on hourly vwap data and 
        the average can be calculated in different 
        ways. It uses BTC conversion if data is not 
        available because the coin is not trading 
        in the specified currency. 
        If tryConversion is set to false it will 
        give you the direct data.
        Also for different timezones use the UTCHourDiff 
        param. 

        Endpoint:
            https://min-api.cryptocompare.com/data/dayAvg

        Example response:
            {'ConversionType': {'conversionSymbol': '', 
                                'type': 'force_direct'},
              'USD': Decimal('5634.95')
              }

        :param fsym: From symbol
        :type fsym: str

        :param tsym: To symbol
        :param tsym: str

        :param e: Exchange, as default returns 
            CryptoCompare current aggregate for 
            all supported by CryptoCompare.
            (optional, default == None)
        :type e: str

        :param avgType:    The calculation valid types are: 
            ["HourVWAP" (a VWAP of the hourly close price),
             "MidHighLow" (the average between the 24h high and low),
             "VolFVolT" (the total volume from / the total volume to, 
                          only avilable with tryConversion set to false 
                          so only for direct trades but the value 
                          should be the most accurate price)]
            (optional, default == "HourVWAP")
        :type avgType: str

        :param UTCHourDiff: By deafult it does UTC, 
            if you want a different time zone just 
            pass the hour difference. 
            For PST you would pass -8 for example.
            (optional, default == "0")
        :type UTCHourDiff: str or int

        :param toTS: If no toTS is given it will 
            automatically do the current day average.
            (optional, default == None)
        :type toTS: str or int

        :param **kwargs: See extraParams, sign 
            and tryConversion params in price method
        """
        args = dict(fsym=fsym, tsym=tsym,
                    avgType=avgType, 
                    UTCHourDiff=str(UTCHourDiff),
                    **kwargs)
        if e:
            args["e"] = e
        if toTS:
            args["toTS"] = str(toTS)
        return self.__call__("data/dayAvg", args)

    def price_historical(self, fsym, tsyms, ts=None,
                         markets=None, **kwargs):
        """
        Get the price of any cryptocurrency in any other
        currency that you need at a given timestamp. 
        The price comes from the daily info - so it 
        would be the price at the end of the day 
        GMT based on the requested TS. 
        If the crypto does not trade directly into 
        the toSymbol requested, BTC will be used for 
        conversion. Tries to get direct trading pair 
        data, if there is none or it is more than 
        30 days before the ts requested, it uses BTC 
        conversion. If the opposite pair trades we 
        invert it (eg.: BTC-XMR)

        Endpoint:
            https://min-api.cryptocompare.com/data/pricehistorical

        Example response:
            {'BTC': {'USD': Decimal('640.12')}}

        :param fsym: From symbol
        :type fsym: str

        :param tsyms: To symbols, include multiple symbols
        :param tsyms: list or str

        :param ts: Timestamp for request historical price.
            (optional, default == None)
        :type ts: int or str

        :param markets: Name of exchanges, include multiple.
            As default CCAGG, (optional, default == None)
        :type markets: list or str

        :param **kwargs: See extraParams, sign 
            and tryConversion params in price method
        """
        args = dict(fsym=fsym, **kwargs)
        args = self._parse_strlist("tsyms", tsyms, args)

        if ts:
            args["ts"] = str(ts)
        if markets:
            args = self._parse_strlist("markets", markets, args)

        return self.__call__("data/pricehistorical", args)

    def social_stats(self, id):
        """
        Get CryptoCompare website, Facebook, code repository, 
        Twitter and Reddit data for coins. If called with 
        the id of a cryptopian you just get data from 
        our website that is available to the public. 
        
        Endpoint:
            https://www.cryptocompare.com/api/data/socialstats

        Example response:
            https://www.cryptocompare.com/api/data/socialstats/?id=1182

        :param id: The id of the coin/exchange 
            you want social data for. For get the id
            of a coin, use the coin_list method.
        :type id: int or str

        :return: https://www.cryptocompare.com/api/#-api-data-socialstats-
        :rtype: dict
        """
        args = dict(id=str(id))
        return self.__call__("data/socialstats", args)

    def histo(self, period, fsym, tsym,
              aggregate="1", limit=None,
              toTs=None, **kwargs):
        """
        Get open, high, low, close, volumefrom and volumeto from 
        the each period time passed as argument of historical data.
        
        Endpoints:
            https://min-api.cryptocompare.com/data/histominute
            https://min-api.cryptocompare.com/data/histohour
            https://min-api.cryptocompare.com/data/histoday

        Example response:
            https://min-api.cryptocompare.com/data/histominute?fsym=BTC&tsym=USD&limit=60&aggregate=3&e=CCCAGG

        :param period: Select period from you want data for
            For period == "minute", the data is stored for 7 days.
            Valid periods:
                ["minute", "hour", "day"]
        :type period: str

        :param fsym: From symbol
        :type fsym: str

        :param tsym: To symbol
        :param tsym: str

        :param aggregate: (Optional, default == "1")
        :type aggregate: str or int

        :param limit: Limit of returns (max 2000)
            (optional, default == None)
        :type limit: str or int

        :param toTs: to timestamp
        :type toTs: str or int

        :param **kwargs: See extraParams, sign 
            and tryConversion params in price method
        """
        args = dict(fsym=fsym, tsym=tsym,
                    aggregate=str(aggregate), 
                    **kwargs)
        if limit:
            args["limit"] = str(limit)
        if toTs:
            args["toTs"] = str(toTs)

        call = "data/histo" + period
        return self.__call__(call, args)

    def mining_contracts(self):
        """
        Returns all the mining contracts

        Endpoint:
            https://www.cryptocompare.com/api/data/miningcontracts/
        """
        return self.__call__("data/miningcontracts")

    def mining_equipment(self):
        """
        Get all the mining equipment

        Endpoint:
            https://www.cryptocompare.com/api/data/miningequipment/
        """
        return self.__call__("data/miningequipment")

    def top_pairs(self, fsym, tsym=None, limit="5", **kwargs):
        """
        Get top pairs by volume for a currency 
        (always uses our aggregated data). 
        The number of pairs you get is the minimum 
        of the limit you set (default 5) 
        and the total number of pairs available.

        Endpoint:
            https://min-api.cryptocompare.com/data/top/pairs

        Example response:
            https://min-api.cryptocompare.com/data/top/pairs?fsym=ETH
         
        :param fsym: From symbol
        :type fsym: str

        :param tsym: To symbol
            (optional, default == None)
        :param tsym: str

        :param limit: Numbers of pairs you get, max 2000
            (optional, default == 5)
        :type limit: str or int

        :param **kwargs: See sign and extraParams params 
            in price method
        """
        args = dict(fsym=fsym, limit=str(limit), **kwargs)
        if tsym:
            args["tsym"] = tsym
        return self.__call__("data/top/pairs", args)

    def top_exchanges(self, fsym, tsym, limit="5", **kwargs):
        """
        Get top exchanges by 24 hour 
        trading volume for the currency pair.

        Endpoint:
            https://min-api.cryptocompare.com/data/top/exchanges

        :param fsym: From symbol
        :type fsym: str

        :param tsym: To symbol
            (optional, default == None)
        :param tsym: str

        :param limit: Numbers of exchanges you get, 
            max 2000 (optional, default == "5")
        :type limit: str or int

        :param **kwargs: See sign and extraParams params 
            in price method
        """
        args = dict(fsym=fsym, limit=str(limit), **kwargs)
        if tsym:
            args["tsym"] = tsym
        return self.__call__("data/top/exchanges", args)

    def top_volumes(self, tsym, limit="50", **kwargs):
        """
        Get top coins by volume for the to currency. 
        It returns volume24hto and total supply 
        (where available). The number of coins you get 
        is the minimum of the limit you set (default 50) 
        and the total number of coins available"
        
        Endpoint:
            https://min-api.cryptocompare.com/data/top/volumes

        :param tsym: To symbol
        :param tsym: str

        :param limit: max amount of coins to retrieve
        :type limit: str or int

        :param **kwargs: See sign and extraParams params 
            in price method
        """
        args = dict(tsym=tsym, limit=str(int(limit)-1), 
                    **kwargs)
        return self.__call__("data/top/volumes", args)

    def exchanges(self, **kwargs):
        """
        Returns all the exchanges that CryptoCompare 
        has integrated with.

        Endpoint:
            https://min-api.cryptocompare.com/data/all/exchanges

        :param **kwargs: See sign and extraParams params 
            in price method
        """
        args = dict(**kwargs)
        return self.__call__("data/all/exchanges", args)

    def news_providers(self, **kwargs):
        """
        Returns all the news providers that CryptoCompare 
        has integrated with.

        Endpoint:
            https://min-api.cryptocompare.com/data/news/providers

        :param **kwargs: See sign and extraParams params 
            in price method
        """
        args = dict(**kwargs)
        return self.__call__("data/news/providers", args)

    def news(self, feeds=None, lTs=None, 
             lang=None, **kwargs):
        """
        Returns recent news classified.

        Endpoint:
            https://min-api.cryptocompare.com/data/news/

        :param feeds: Filter by news providers, see
            news providers method, (optional, default == None)
        :type feeds: str or list

        :param lTs: Limit timestamp (optional, default == None)
        :type lTs: str or int

        :param lang: Language of news filter, English as default
            (optional, default == None)

        :param **kwargs: See sign and extraParams params 
            in price method
        """
        args = dict(**kwargs)
        if feeds:
            args = self._parse_strlist("feeds", 
                                       feeds, args)
        if lTs:
            args["lTs"] = lTs
        if lang:
            args["lang"] = lang

        return self.__call__("data/news/", args)
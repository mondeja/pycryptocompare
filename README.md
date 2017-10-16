<h1>pycryptocompare</h1>

[pycryptocompare](https://github.com/mondeja/pycryptocompare) is a Python3 wrapper for the [Cryptocompare API](https://www.cryptocompare.com/api/) of [cryptocompare.com](https://www.cryptocompare.com/).

### Installation
```
git clone https://github.com/mondeja/pycryptocompare.git
cd pycryptocompare
python3 setup.py install
```

### Usage
```python
>>> from pycryptocompare import CryptoCompare
>>> cc = CryptoCompare()
>>> BTC_ETH_to_EUR = cc.price(["BTC", "ETH"], "EUR", full=True)
``` 

### Documentation
Currently only available in docstrings.

### Testing
```
cd pycryptocompare/tests
python3 tests.py
```
## Development progress
Some methods like `CoinSnapshot` not supported because [will be edited in the near future](https://www.cryptocompare.com/api/#-api-data-coinsnapshot-).

## Support

If you are experiencing issues, please let me know (mondejar1994@gmail.com).

## License

Copyright (c) 2017 Álvaro Mondéjar Rubio <mondejar1994@gmail.com>.
All rights reserved.

Redistribution and use in source and binary forms are permitted
provided that the above copyright notice and this paragraph are
duplicated in all such forms and that any documentation, advertising
materials, and other materials related to such distribution and use
acknowledge that the software was developed by Álvaro Mondéjar Rubio. The
name of the Álvaro Mondéjar Rubio may not be used to endorse or promote
products derived from this software without specific prior written
permission.

THIS SOFTWARE IS PROVIDED “AS IS” AND WITHOUT ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

### Buy me a coffee? :)

If you feel like buying me a coffee (or a beer?), donations are welcome:

```
BTC : 1LfUF4AcvH7Wd1wTc7Mmqobj4AypUbpvN5
ETH : 0x7428fE875226880DaD222c726F6340eec42Db567
STEEM: @mondeja
```
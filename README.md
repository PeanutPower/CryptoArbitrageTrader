CryptoArbitrageTrader
=====================

Compares the prices sell / buy for various Altcoins on the exchanges: Coins-E, BTC-e, Vircurex and Cryptsy. It executes the Sell / buy trades as arbitrage of given percentage is found.

Developed and shared by JohnDorien on Bitcointalk

https://bitcointalk.org/index.php?topic=263815.0

Donations to JohnDorien:

BTC: 1JxT7dgLxbdHR9iBpu7v4z4ph3kjD5pjA9

LTC: LQ32aPGFGwFb7MxvLTai2ePwRFRbnSKpWv


Getting Started
================

1. You will need Python on your system:
http://www.python.org/getit/
(Windows: You may wish to add C:\Python27\; to your PATH environment variables to you can run "python" from the command line)
If you are running windows you'll also need pycurl
http://www.lfd.uci.edu/~gohlke/pythonlibs/

2. Clone the repo somewhere

3. Edit config.py

"Edit the config.py with your API Keypairs for every exchange
Edit the value "amount" if you like to
Have at least the amount of altcoins you set in the config in your available funds of each exchange. BTC fund has to be highest price altcoin * amount"

4. Run: python arbitrage_trader.py

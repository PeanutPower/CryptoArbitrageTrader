# (c) by JohnDorien
# Contact: JohnDorien on Bitcointalk forums
# No warranty for anything!

# If you like this, please donate!

# BTC: 1JxT7dgLxbdHR9iBpu7v4z4ph3kjD5pjA9
# LTC: LQ32aPGFGwFb7MxvLTai2ePwRFRbnSKpWv


import btc_e_api, thread, time
from time import strftime
from vircurex import *
from PyCryptsy import PyCryptsy
from crypto import crypto

FEE = 1.02 # fee for every trade (2%)
Diff = 1.02 # 2 % arbitrage to execute
curr = ["ltc","ftc","ppc","nvc","nmc"] #currencies to trade if arbitrage is found
exc = ["btc-e", "vircu", "cryptsy", "coins-e"] #exchanges to trade on for the function calls
amount1 = 10 #the number of altcoins to be traded vs. btc in each trade

# BTC-e login data:
key = 'public_key'
secret = 'secret_key'
btce = btc_e_api.API(key,secret)

#Vircurex Login Data:
vircurex = Account("username", "api_secret")

#Crypto-trade Login Data:
key="Public_Key"
secret="Secret_Key"
cryp = crypto(key,secret)	

#Cryptsy Login Data:
cryptsy = PyCryptsy('Public_Key', 'Secret_Key')

#coins-e Login Data:
PUBLIC_KEY = "Public_Key"  
PRIVATE_KEY = "Secret_Key"

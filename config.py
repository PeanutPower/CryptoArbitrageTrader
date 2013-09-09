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
curr = ["xpm","ltc","ftc","ppc","nmc"] #currencies to trade if arbitrage is found
exc = ["crypto","vircu","btc-e","coins-e"] #exchanges to trade on for the function calls
# ["btc-e", "vircu", "cryptsy", "coins-e"]
amount1 = 1 #the number of altcoins to be traded vs. btc in each trade

# BTC-e login data:
btce = btc_e_api.API('XJP018WC-35J8SO7G-Z7QH8BDU-JEVRV5VA-G23W3ZSN','caf818fa22084b672a0d53e05fc6f0e903e1e242976034f8aa2666f5c502b497')

#Vircurex Login Data:
vircurex = Account('peanutpower', '745p2V8v5c5J21u')

#Crypto-trade Login Data:
cryp = crypto('67FF99C7-69D1-A090-C3C9-12AB9BD94E14','c27b6251614b4baeebc115358f79697636fa27b6')	

#Cryptsy Login Data:
cryptsy = PyCryptsy('db34131d6a8f0bbc19028f322cd22a6b986dde69', '79d5bf670a684b3bbbc109f6f64d4ed48c84b1b426546c30a5bcac43d7d8687c2c2d6b96f13b2c2f')

#coins-e Login Data:
PUBLIC_KEY = '14def7bc47f9858551b34f7cda5a17d64fe76112c21f53838a03f2f3'
PRIVATE_KEY = 'f0896ce593aa2ed4232dff8abc0581f69fd77bd6eaf8360cf682b462b89cbd31'

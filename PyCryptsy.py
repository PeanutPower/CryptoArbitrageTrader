# coding=iso-8859-1

# PyCryptsy: a Python binding to the Cryptsy API
#
# Copyright © 2013 Scott Alfter
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import pycurl
import time
import hmac
import hashlib
import urllib
import StringIO
import json

class PyCryptsy:
  
  # constructor (Key: API public key, Secret: API private key)
  def __init__(self, Key, Secret):
    self.key=Key
    self.secret=Secret
    
  # issue any supported query (method: string, req: dictionary with method parameters)
  def Query(self, method, req):
    # generate POST data string
    req["method"]=method
    req["nonce"]=int(time.time())  
    post_data=urllib.urlencode(req)
  
    # sign it
    sign=hmac.new(self.secret, post_data, hashlib.sha512).hexdigest()

    # extra headers for request
    headers=["Sign: "+sign, "Key: "+self.key]
  
    # curl handle
    b=StringIO.StringIO()
    ch=pycurl.Curl()
    ch.setopt(pycurl.URL, "https://www.cryptsy.com/api")
    ch.setopt(pycurl.POSTFIELDS, post_data)
    ch.setopt(pycurl.HTTPHEADER, headers)
    ch.setopt(pycurl.SSL_VERIFYPEER, 0)
    ch.setopt(pycurl.WRITEFUNCTION, b.write)
    try:
      ch.perform()
    except pycurl.error, error:
      errno, errstr=error
      raise Exception("pycurl error: "+errstr)
  
    # decode and return
    try:
      rtnval=json.loads(b.getvalue())
    except:
      raise Exception("unable to decode response")
    return rtnval

  # get market ID (return None if not found)
  def GetMarketID (self, src, dest):
    try:
      r=self.Query("getmarkets", {})
      for i, market in enumerate(r["return"]):
        if market["primary_currency_code"].upper()==src.upper() and market["secondary_currency_code"].upper()==dest.upper():
          mkt_id=market["marketid"]
      return mkt_id
    except:
      return None
    
  # get buy price for a currency pair
  def GetBuyPrice (self, src, dest):
    mktid = self.GetMarketID(src, dest)
    if mktid is None:
      return 0
    try:
      r=self.Query("marketorders", {"marketid": mktid})
      return float(r["return"]["buyorders"][0]["buyprice"])
    except:
      return 0

  # get sell price for a currency pair
  def GetSellPrice (self, src, dest):
    mktid = self.GetMarketID(src, dest)
    if mktid is None:
      return 0
    try:
      r=self.Query("marketorders", {"marketid": mktid})
      return float(r["return"]["sellorders"][0]["sellprice"])
    except:
      return 0

  # get available balance for a currency
  def GetAvailableBalance (self, curr):
    try:
      r=self.Query("getinfo", {})
      return float(r["return"]["balances_available"][curr.upper()])
    except:
      return 0
        
  # create a sell order
  def CreateSellOrder (self, src, dest, qty, price):
    try:
      return self.Query("createorder", {"marketid": self.GetMarketID(src, dest), "ordertype": "Sell", "quantity": qty, "price": price})
    except:
      return None

  # create a buy order
  def CreateBuyOrder (self, src, dest, qty, price):
    try:
      return self.Query("createorder", {"marketid": self.GetMarketID(src, dest), "ordertype": "Buy", "quantity": qty, "price": price})
    except:
      return None

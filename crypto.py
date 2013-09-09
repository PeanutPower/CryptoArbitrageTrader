#Matuszed 2013-07-03
#Questions about usage email mindsdecree@gmail.com

import time,hmac,base64,hashlib,urllib,urllib2,json
class crypto:
	timeout = 15
	tryout = 8

	def __init__(self, key='', secret='', agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0'):
		self.key, self.secret, self.agent = key, secret, agent
		self.time = {'init': time.time(), 'req': time.time()}
		self.reqs = {'max': 10, 'window': 10, 'curr': 0}
		self.base = 'https://www.crypto-trade.com/api/1/'

	def throttle(self):
		# check that in a given time window (10 seconds),
		# no more than a maximum number of requests (10)
		# have been sent, otherwise sleep for a bit
		diff = time.time() - self.time['req']
		if diff > self.reqs['window']:
			self.reqs['curr'] = 0
			self.time['req'] = time.time()
		self.reqs['curr'] += 1
		if self.reqs['curr'] > self.reqs['max']:
			print 'Request limit reached...'
			time.sleep(self.reqs['window'] - diff)

	def makereq(self, path, data):
		# bare-bones hmac rest sign
                params = {'nonce':str(int(time.time() * 1e3))}
		return urllib2.Request(self.base + path, params, {
                        #'Content-Type' :'application/json',
			'AuthKey': self.key,
			'AuthSign': hmac.new(self.secret, data, hashlib.sha512).hexdigest()
		})

	def req(self, path, inp={}):
		t0 = time.time()
		tries = 0
		while True:
			# check if have been making too many requests
			self.throttle()

			try:
				# send request
				inp['nonce'] = str(int(time.time() * 1e3))
				inpstr = urllib.urlencode(inp.items())
				req = self.makereq(path, inpstr)
				response = urllib2.urlopen(req, inpstr)

				# interpret json response
				output = json.load(response)
				if 'error' in output:
					raise ValueError(output['error'])
				return output
				
			except Exception as e:
				print "Error: %s" % e

			# don't wait too long
			tries += 1
			if time.time() - t0 > self.timeout or tries > self.tryout:
				raise Exception('Timeout')
				
		
#key="MYKEY"
#secret="MYSECRET"
#cryp = crypto(key,secret)				
#			
#Example placing an order			
#cryp.req('trade',{"pair":"ltc_btc","type":"Buy","amount":ltc_bid_amount,"rate":price_to_bid})		
#						
#Example Cancelling an order
#cryp.req('cancelorder',{"orderid":order_id})
#
#Example Get Funds
#account_info=cryp.req('getinfo')
#orig_crypto_ltc_amount=float(account_info['data']['funds']['ltc'])
#orig_crypto_btc_amount=float(account_info['data']['funds']['btc'])
#orig_crypto_usd_amount=float(account_info['data']['funds']['usd'])
#
#Example Get Last Two Days of Orders
#unix_time_lag=int(time.time()-166400)
#for order in cryp.req('ordershistory',{'start_date':unix_time_lag})['data']:
#    if  order["status"]=="Active" or order["status"]=='Partly Completed':
#	cryp.req('cancelorder',{"orderid":int(order["id"])})


	

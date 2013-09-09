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
import crypto
from config import *
from coinse_api import *
 
########################################################

def getDepth_btce(pairpart1, pairpart2):
	depth_btce = btce.depth(pairpart1+'_'+pairpart2)
	return depth_btce

def getDepth_vircurex(pairpart1, pairpart2):
	depth_vircurex = Pair(pairpart1+"_"+pairpart2)
	return depth_vircurex

def getDepth_cryptsy(pairpart1, pairpart2):
	pairpart1 = pairpart1.upper()
	pairpart2 = pairpart2.upper()
	target1=cryptsy.GetBuyPrice(pairpart1, pairpart2)
	target2=cryptsy.GetSellPrice(pairpart1, pairpart2)
	depth_cryptsy = [target1, target2]
	return depth_cryptsy

def getDepth_cryptotrade(pairpart1, pairpart2):
	depth_cryptotrade = cryp.req('depth/'+pairpart1+'_'+pairpart2)
	return depth_cryptotrade

def getDepth_coinse(pairpart1, pairpart2):
	pairpart1 = pairpart1.upper()
	pairpart2 = pairpart2.upper()
	depth_coinse = unauthenticated_request('market/'+pairpart1+'_'+pairpart2+'/',"depth")#,{'pair':pairpart1+'_'+pairpart2})
	return depth_coinse

#########################################################
def getS(exchange, pairpart1, pairpart2):
	if exchange == "btc-e":
		depth_btce = getDepth_btce(pairpart1, pairpart2)
		sprice = depth_btce['bids'][0][0]
	elif exchange == "vircu":
		depth_vircurex = getDepth_vircurex(pairpart1, pairpart2)
		sprice = depth_vircurex.highest_bid
	elif exchange == "cryptsy":
		#getDepth_cryptsy(pairpart1, pairpart2)
		pairpart1 = pairpart1.upper()
		pairpart2 = pairpart2.upper()
		sprice = cryptsy.GetSellPrice(pairpart2, pairpart1)
	elif exchange == "crypto":
		depth_cryptotrade = getDepth_cryptotrade(pairpart1, pairpart2)
		sprice = depth_cryptotrade['bids'][0][0]
	elif exchange == "coins-e":
		depth_coinse = getDepth_coinse(pairpart1, pairpart2)
		sprice = depth_coinse['marketdepth']['bids'][1]['r']
	else:
		sprice = 0
	return sprice

def getB(exchange, pairpart1, pairpart2):
	if exchange == "btc-e":
		depth_btce = getDepth_btce(pairpart1, pairpart2)
		bprice = depth_btce['asks'][0][0]
	elif exchange == "vircu":
		depth_vircurex = getDepth_vircurex(pairpart1, pairpart2)
		bprice = depth_vircurex.lowest_ask
	elif exchange == "cryptsy":
		#getDepth_cryptsy(pairpart1, pairpart2)
		pairpart1 = pairpart1.upper()
		pairpart2 = pairpart2.upper()
		bprice = cryptsy.GetBuyPrice(pairpart1, pairpart2)
	elif exchange == "crypto":
		depth_cryptotrade = getDepth_cryptotrade(pairpart1, pairpart2)
		bprice = depth_cryptotrade['asks'][0][0]
	elif exchange == "coins-e":
		depth_coinse = getDepth_coinse(pairpart1, pairpart2)
		bprice = depth_coinse['marketdepth']['asks'][0]['r']
	else:
		bprice = 0
	return bprice

#############################################################

def make_trade(exchange, type, amount, pairpart1, pairpart2, rate):   # Type = "buy" or "sell"
	if exchange == "btc-e":
		if type == "buy":
			btce.trade('buy',amount, pairpart1+'_'+pairpart2, rate)
		else:
			btce.trade('sell',amount, pairpart1+'_'+pairpart2, rate)
	elif exchange == "vircu":
		if type == "buy":
			vircurex.buy(pairpart1, amount, pairpart2, rate)
		else:
			vircurex.sell(pairpart1, amount, pairpart2, rate)
	elif exchange == "cryptsy":
		if type == "buy":
			cryptsy.CreateBuyOrder(pairpart1, pairpart2, amount, rate)
		else:
			cryptsy.CreateSellOrder(pairpart1, pairpart2, amount, rate)
	elif exchange == "crypto":
		if type == "buy":
			cryp.req('private/trade',{"pair":pairpart1+"_"+pairpart2,"type":"Buy","amount":amount,"rate":rate})
		else:
			cryp.req('private/trade',{"pair":pairpart1+"_"+pairpart2,"type":"Sell","amount":amount,"rate":rate})
	elif exchange == "coins-e":
		if type == "buy":
			authenticated_request('market/%s/' % (pairpart1+'_'+pairpart2),"neworder",{'order_type':'buy', 'rate':rate, 'quantity':amount,})
		else:
			authenticated_request('market/%s/' % (pairpart1+'_'+pairpart2),"neworder",{'order_type':'sell', 'rate':rate, 'quantity':amount,})
	else:
		return 0

#############################################################

def compare():
	#print "starting arbitrage checking"
	pairpart2 = "btc"

	n=0
	while n<=(len(curr)-1):
		print "Starting Arbitrage checking for Currency " + curr[n]
		pairpart1 = curr[n]
		m=0
		while m<=(len(exc)-1):
			#print "m = " + str(m)
			k = 0
			while k<=(len(exc)-1):
				#print "k = " + str(k)
				try:
					sprice = getS(exc[m], curr[n], "btc")
					#print "SPrice = " + sprice + " on " + exc[m]
					bprice = getB(exc[k], curr[n], "btc")
					#print "BPrice = " + bprice + " on " + exc[k]
				except Exception:
					pass
				#print "BPrice = " + str(bprice) + " on " + exc[k] #enable for debug
				if round((int(bprice) * Diff * FEE),8) < round((int(sprice) * FEE),8):
					make_trade(exc[m], "buy", amount1, pairpart1, "btc", bprice)
					make_trade(exc[k], "sell", amount1, pairpart1, "btc", sprice)
					#printouts for debugging
					#print "price on " + exc[m] + " for " + curr[n] + " is " + str(sprice) + " BTC"
					#print "price on " + exc[k] + " for " + curr[n] + " is " + str(bprice) + " BTC"
					print "executing trade at a win per 1" + curr[n] + " of " + str(round(((str(sprice) * FEE)-(str(bprice) * Diff * FEE)),8)) + "BTC"
				else:
					try:
						sprice = getS(exc[k], curr[n], "btc")
						bprice = getB(exc[m], curr[n], "btc")
					except Exception:
						pass
					if round((int(bprice) * Diff * FEE),8) < round((int(sprice) * FEE),8):
						make_trade(exc[k], "buy", amount1, pairpart1, "btc", bprice)
						make_trade(exc[m], "sell", amount1, pairpart1, "btc", sprice)
						#printouts for debugging
						#print "price on " + exc[k] + " for " + curr[n] + " is " + str(sprice) + " BTC"
						#print "price on " + exc[m] + " for " + curr[n] + " is " + str(bprice) + " BTC"
						print "executing trade at a win per 1" + curr[n] + " of " + str(round(((sprice * FEE)-(bprice * Diff * FEE)),8)) + "BTC"
				k+=1
			m+=1
		n+=1


###############################################################

def main():
	"""main funtion, called at the start of the program"""
 
	def run1(sleeptime, lock):
		while True:
			lock.acquire()
			compare() #die Hauptfunktion der Arbitrage
			print "Round completed"
			lock.release()
			time.sleep(sleeptime)
 
	lock = thread.allocate_lock()
	thread.start_new_thread(run1, (15, lock))
 
	while True:
		pass

if __name__ == "__main__":
	main()

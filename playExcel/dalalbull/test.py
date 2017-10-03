from urllib import request
import pprint

import json

pp = pprint.PrettyPrinter(indent=4)

#nifty_top50 = ['ACC', 'AMBUJACEM', 'AXISBANK', 'BAJAJ-AUTO', 'BHARTIARTL', 'BHEL',
#	'BPCL', 'CAIRN', 'CIPLA', 'DLF', 'DRREDDY', 'GAIL', 'GRASIM', 'HCLTECH', 'HDFC', 
#	'HDFCBANK', 'HEROHONDA', 'HINDALCO', 'HINDUNILVR', 'ICICIBANK', 'IDFC', 'INFOSYSTCH', 'ITC',
#	'JINDALSTEL', 'JPASSOCIAT', 'KOTAKBANK', 'LT', 'M&M', 'MARUTI', 'NTPC', 'ONGC', 'PNB',
#	'POWERGRID', 'RANBAXY', 'RCOM', 'RELCAPITAL', 'RELIANCE', 'RELINFRA', 'RPOWER',
#	'SAIL', 'SBIN', 'SESAGOA', 'SIEMENS', 'STER', 'SUNPHARMA', 'TATAMOTORS', 'TATAPOWER',
#	'TATASTEEL', 'TCS', 'WIPRO']

nifty_top50 = ['HCLTECH', 'CIPLA', 'TATAMOTORS', 'SUNPHARMA', 'BOSCHLTD', 'WIPRO', 'ITC', 'TATAMTRDVR', 'TECHM',
	'M&M', 'INFRATEL', 'KOTAKBANK', 'BPCL', 'LUPIN', 'DRREDDY', 'HDFC', 'TCS', 'MARUTI', 'HDFCBANK', 'ONGC',
 	'POWERGRID', 'ASIANPAINT', 'COALINDIA', 'AXISBANK', 'BAJAJ-AUTO', 'HINDUNILVR', 'BHARTIARTL', 'SBIN', 'IOC',
	'ADANIPORTS', 'INFY', 'EICHERMOT', 'AUROPHARMA', 'INDUSINDBK', 'NTPC', 'BANKBARODA', 'TATAPOWER', 'RELIANCE', 
	'ZEEL', 'HEROMOTOCO', 'GAIL', 'AMBUJACEM', 'LT', 'ACC', 'ICICIBANK', 'IBULHSGFIN', 'TATASTEEL', 'VEDL', 
	'HINDALCO', 'YESBANK', 'ULTRACEMCO'
	]


SECRET_KEY = '2905cb1d-76e0-48f5-b823-8384af1d0642'
def getCompanyDetails(symbol):
	url = 'http://nimblerest.lisuns.com:4531/GetLastQuote/?accessKey=%s&xml=false&exchange=NSE&instrumentIdentifier=%s'%(SECRET_KEY,symbol)
	try_count = 0
	while True:
		try:
			page = request.urlopen(url).read()	
			data = json.loads(page.decode('utf-8'))
			break
		except:
			print("Failed once")
			try_count += 1
			if try_count == 3:
				print("Try count exceeded!")
				return None
	required_data = {}
	required_data['current_price'] = float(data['LASTTRADEPRICE'])
	required_data['high'] = float(data['HIGH'])
	required_data['low'] = float(data['LOW'])
	required_data['open_price'] = float(data['OPEN'])
	required_data['change'] = required_data['current_price'] - float(data['CLOSE']) 
	required_data['change_per'] = float(required_data['change']*100)/float(data['CLOSE']) 
	required_data['trade_Qty'] = float(data['TOTALQTYTRADED'])/100000
	required_data['trade_Value'] = float(data['VALUE'])/float(data['TOTALQTYTRADED'])

	return required_data


#for sym in nifty_top50:
#	print(sym)
#	pp.pprint(getCompanyDetails('HINDALCO'))

import os
import time
while True:
	os.system("clear")
	print(getCompanyDetails('HINDALCO'))
	time.sleep(1)

'''
TOTALQTYTRADED
c=Stock_data.objects.get(symbol=company['symbol'])
	c.current_price=yahoo['list']['resources'][symbolmap[company['symbol']]]['resource']['fields']['price']
	c.high=company['high'].replace(",","")
	c.low=company['low'].replace(",","")
	c.open_price=company['open'].replace(",","")
	c.change=company['ptsC'].replace(",","")
	c.change_per=company['per'].replace(",","")
	c.trade_Qty=company['trdVol'].replace(",","")
c.trade_Value=company['ntP'].replace(",","")
c.save()
'''
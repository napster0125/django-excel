from __future__ import absolute_import,unicode_literals

from celery import shared_task
from urllib import request
import urllib
import json
import datetime
from .models import User,Portfolio,Stock_data,Transaction,History,Pending,Old_Stock_data

from .consumers import sellDataPush,niftyChannelDataPush,graphDataPush,portfolioDataPush,tickerDataPush


#Deletes all old stock data



#======Tasks======#

@shared_task
def tq(): 	
	print("Stock Update");	
	stockdata()
	print("Orders");	
	orders()
	return 


@shared_task
def dq():
	if isGoodTime(): 
		print("Graph Values Update");
		oldstockdata()
		graphDataPush()
	else:
		print("Not the time for graph broadcast")
	return 


@shared_task
def orderLeaderboard():
	if isGoodTime():
		print("Leaderboard ordered!")
		ordered_data = Portfolio.objects.order_by('-net_worth')
		rank = 1
		for e in ordered_data:
			e.rank = rank
			rank += 1
			e.save()
	return

@shared_task
def net():
    print("Networth Update");
    networth()
    return


@shared_task
def broadcastNiftyData():
	if isGoodTime():
		print("Nifty data broadcasted!")
		niftyChannelDataPush()
	else:
		print("Not the time for nifty broadcast")


# @shared_task
# def broadcastLeaderboardData():
# 	if isGoodTime():
# 		print("Leaderboard data broadcasted!")
# 		leaderboardChannelDataPush()
# 	else:
# 		print("Not the time for leaderboard broadcast")



@shared_task
def broadcastSellData():
	if isGoodTime():
		print("Sellers data broadcasted!")
		sellDataPush()
	else:
		print("Not the time for sell broadcast")

@shared_task
def broadcastPortfolioData():
	if isGoodTime():
		print("Portfolio data broadcasted!")
		portfolioDataPush()
	else:
		print("Not the time for portfolio broadcast")

@shared_task
def broadcastTickerData():
	if isGoodTime():
		print("Ticker data broadcasted!")
		tickerDataPush()
	else:
		print("Not the time for ticker broadcast")



#==========Utility Functions========#
				
#==========Sell/Short-Cover========#        
def sell_sc(username,symbol,quantity,typ):
	qnty=float(quantity)
	try:
		price = float(Stock_data.objects.get(symbol=symbol).current_price)
		port = Portfolio.objects.get(user_id=username)
		cash_bal = float(port.cash_bal)
		no_trans = float(port.no_trans)
		margin = float(port.margin)
		
		if(typ=="Sell"):
			b_ss="Buy"
		else:
			b_ss="Short Sell"
		
		try:
			t=Transaction.objects.get(symbol=symbol,user_id=username,buy_ss=b_ss)
			old_quantity = float(t.quantity)
			old_value = float(t.value)
			
			if(quantity<=old_quantity):
				new_quantity=old_quantity-qnty
				old_total=(old_value/old_quantity)*qnty
				new_value=old_value-old_total;
				if(new_quantity==0):
					t.delete()
				else:
					t.quantity=new_quantity
					t.value=new_value
					t.save()
				try:
					port = Portfolio.objects.get(user_id=username)
					old_cash_bal = float(port.cash_bal)
					margin =float(port.margin)
					no_trans = float(port.no_trans)
					if(typ == "Short Cover"):
						sc_profit=old_total-qnty*price
						cash_bal=old_cash_bal+sc_profit
						margin=(margin-(old_value/2))+(new_value/2)
					elif(typ == "Sell"):
						cash_bal=old_cash_bal+(qnty*price)						
					no_trans=no_trans+1
					if(no_trans<=100):
						brokerage=((0.5/100)*price)*qnty
					elif(no_trans<=1000):
						brokerage=((1/100)*price)*qnty
					else:
						brokerage=((1.5/100)*price)*qnty
					
					print("\nupdating portfolio")
					cash_bal-=brokerage
					port.cash_bal=cash_bal
					port.margin=margin
					port.no_trans=no_trans
					port.save()
					print("Pending order completed")
					history=History(user_id=username,time=datetime.datetime.now(),symbol=symbol,buy_ss=typ,quantity=qnty,price=price)
					history.save()
					return True
				except Portfolio.DoesNotExist:
					print("Error fetching portfolio")
		except Transaction.DoesNotExist:
			print("Error fetching from transactions ")
			return False
	except Stock_data.DoesNotExist:
		return False
	return False
#==========Buy/Short-Sell========#
def buy_ss(username,symbol,quantity,typ):	
	qnty=float(quantity)
	try:
		price = float(Stock_data.objects.get(symbol=symbol).current_price)
		port = Portfolio.objects.get(user_id=username)
		cash_bal = float(port.cash_bal)
		no_trans = float(port.no_trans)
		margin = float(port.margin)
		if(no_trans+1<=100):
			brokerage=((0.5/100)*price)*qnty
		else:
			if(no_trans+1<=1000):
				brokerage=((1/100)*price)*qnty
			else:
				brokerage=((1.5/100)*price)*qnty
		if(((cash_bal-margin-brokerage)>0 and (cash_bal-margin-brokerage)>=(price*qnty) and typ == "Buy") or ((cash_bal-margin-brokerage)>=((price*qnty)/2) and typ == "Short Sell")):
			try:
				trans = Transaction.objects.get(user_id=username,symbol=symbol,buy_ss=typ)
				old_qnty = float(trans.quantity)
				value = float(trans.value)
				value +=(qnty*price)
				new_qnty = old_qnty + qnty
				trans.quantity=new_qnty
				trans.value=value
				trans.save()
				print("Pending order completed")
			except Transaction.DoesNotExist:
				value = qnty*price
				trans = Transaction(user_id=username,symbol=symbol,buy_ss=typ,quantity=qnty,value=value)
				trans.save()
				print("Pending order completed")  					
			if(typ =="Buy"): 
				cash_bal_up = cash_bal-(qnty*price)
				margin_up = margin
			else:
				if(typ =="Short Sell"): 
					cash_bal_up = cash_bal
					margin_up = margin+(qnty*price)/2
			cash_bal_up -= brokerage
			no_trans+=1
			port.cash_bal=cash_bal_up
			port.margin=margin_up
			port.no_trans=no_trans
			port.save()
			history=History(user_id=username,time=datetime.datetime.now(),symbol=symbol,buy_ss=typ,quantity=qnty,price=price)
			history.save()
			return True
	except Stock_data.DoesNotExist:
		return False	
	return False


#===============Orders=================#
def orders():
	ret=False
	if(datetime.datetime.now().strftime("%A")!='Sunday' and datetime.datetime.now().strftime("%A")!='Saturday'):
		if((datetime.datetime.now().time()>=datetime.time(hour=9,minute=00,second=00)) and (datetime.datetime.now().time()<=datetime.time(hour=9,minute=1,second=00))):
			Old_Stock_data.objects.all().delete()
	if (datetime.datetime.now().time()>=datetime.time(hour=9,minute=6,second=0)) and (datetime.datetime.now().time()<=datetime.time(hour=9,minute=6,second=30)):
		oldstockdata()
	if(datetime.datetime.now().time()>=datetime.time(hour=15,minute=30,second=00)):
		try:
			day_endq=Transaction.objects.filter(buy_ss='Short Sell')
			for i in day_endq :
				username = i.user_id 
				symbol = i.symbol
				quantity = i.quantity
				type_temp = "Short Cover";
				print("Short Cover")
				ret= sell_sc(username,symbol,quantity,type_temp)		
		except Transaction.DoesNotExist :
			print("No Transactions")   		
		Pending.objects.all().delete()
	else:
		try:
			pending_ord = Pending.objects.all()
			for i in pending_ord :
				idn = i.id
				username = i.user_id
				symbol = i.symbol
				typ = i.buy_ss
				quantity = i.quantity
				price = i.value
				try:
					stock_qry = Stock_data.objects.get(symbol=symbol)
					current_price  = stock_qry.current_price
					if(current_price >0):
						if(current_price<=price):
							if(typ == "Buy"):
								ret= buy_ss(username,symbol,quantity,typ)
							else:
								if(typ == "Short Cover"):
									ret=sell_sc(username,symbol,quantity,typ)
						else:
							if(current_price>=price):
								if(typ == "Sell"):
									ret=sell_sc(username,symbol,quantity,typ)
								else:
									if(typ == "Short Sell"):
										ret=buy_ss(username,symbol,quantity,typ)
						if(ret==True):
							ret=False
							del_query = Pending.objects.get(id=idn,user_id=username,symbol=symbol,buy_ss=typ,quantity=quantity,value=price)
							del_query.delete()
				except Stock_data.DoesNotExist:
					print("Company Not Listed")
		except Pending.DoesNotExist:
			print("No Pending Orders")	

#========Networth Update========#
def networth():
	u = User.objects.all()
	for k in u:
		try:
			i=Portfolio.objects.get(user_id=k.user_id)	
			net_worth=float(i.cash_bal)
			try:
				trans=Transaction.objects.filter(user_id=i.user_id,buy_ss='Buy')
				for j in trans:
					try:
						current_price = float(Stock_data.objects.get(symbol=j.symbol).current_price)
						net_worth+=current_price*float(j.quantity)
					except Stock_data.DoesNotExist:
						print("Company Not Listed")
				i.net_worth = net_worth
				i.save()
			except Transaction.DoesNotExist:
				print("No Transactons")
		except Portfolio.DoesNotExist:
			print("Fail")
	return

#=======Stock Database Update=========#








#====== Utility functions =======#
_start_time = datetime.time(hour=9,minute=15,second=30)#,second=00)
_end_time = datetime.time(hour=15,minute=29,second=30)#,minute=30,second=00)
def isGoodTime():
	now = datetime.datetime.now()
	if(now.strftime("%A")!='Sunday' and now.strftime("%A")!='Saturday'):		
		if( _start_time <= now.time() < _end_time):
			return True
	return False


def onlyAtGoodTime(func):
	def new_func(*args,**kwargs):
		if isGoodTime():
			return func(*args,**kwargs)
		else:
			print("Not the time for %s"%func.__name__)
			return None
	return new_func




hdr = {
	'User-Agent': "Mozilla/5.0 (Linux; Android 6.0.1; MotoG3 Build/MPI24.107-55) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.81 Mobile Safari/537.36",
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	'Accept-Encoding': 'none',
	'Accept-Language': 'en-US,en;q=0.8',
	'Connection': 'keep-alive'
}

API_KEY = '2905cb1d-76e0-48f5-b823-8384af1d0642'
nse_url = 'http://nseindia.com/live_market/dynaContent/live_watch/stock_watch/niftyStockWatch.json'

def getRemoteData(url,tries_allowed=3):
	while tries_allowed>0:
		try:
			req = request.Request(url,headers=hdr)
			page = request.urlopen(req).read()
			data = json.loads(page.decode('utf-8'))
			return data
		except:
			tries_allowed -= 1
	return None


def getCompanyDetails(symbol):
	url = 'http://nimblerest.lisuns.com:4531/GetLastQuote/?accessKey=%s&xml=false&exchange=NSE&instrumentIdentifier=%s'%(API_KEY,symbol)
	data = getRemoteData(url)
	required_data = {}
	required_data['current_price'] = float(data['SELLPRICE'])
	required_data['high'] = float(data['HIGH'])
	required_data['low'] = float(data['LOW'])
	required_data['open_price'] = float(data['OPEN'])
	required_data['change'] = required_data['current_price'] - float(data['CLOSE']) 
	required_data['change_per'] = float(required_data['change']*100)/float(data['OPEN']) 
	required_data['trade_Qty'] = float(data['TOTALQTYTRADED'])/100000
	required_data['trade_Value'] = float(data['VALUE'])
	return required_data


nifty_top50 = [
	'HCLTECH', 'CIPLA', 'TATAMOTORS', 'SUNPHARMA', 'BOSCHLTD', 'WIPRO', 'ITC', 'TATAMTRDVR', 'TECHM',
	'INFRATEL', 'KOTAKBANK', 'BPCL', 'LUPIN', 'DRREDDY', 'HDFC', 'TCS', 'MARUTI', 'HDFCBANK', 'ONGC',
	'POWERGRID', 'ASIANPAINT', 'COALINDIA', 'AXISBANK', 'BAJAJ-AUTO', 'HINDUNILVR', 'BHARTIARTL', 'SBIN', 'IOC',
	'ADANIPORTS', 'INFY', 'EICHERMOT', 'AUROPHARMA', 'INDUSINDBK', 'NTPC', 'BANKBARODA', 'TATAPOWER', 'RELIANCE', 
	'ZEEL', 'HEROMOTOCO', 'AMBUJACEM', 'LT', 'ACC', 'ICICIBANK', 'IBULHSGFIN', 'TATASTEEL', 'VEDL', 
	'HINDALCO', 'YESBANK', 'ULTRACEMCO', 'GAIL',
]

_first_half_query = '+'.join(nifty_top50[:25])
_second_half_query = '+'.join(nifty_top50[25:])


base_url_formatted = 'http://nimblerest.lisuns.com:4531/GetLastQuoteArray/?accessKey=%s&exchange=NSE&instrumentIdentifiers=%s'
def getBulkData():
	url = base_url_formatted%(API_KEY,_first_half_query)
	data = getRemoteData(url)
	url = base_url_formatted%(API_KEY,_second_half_query)
	data += getRemoteData(url)
	
	formatted_data = []
	count = 0
	for d in data: 
		count += 1
		required_data = {}
		required_data['current_price'] = float(d['SELLPRICE'])
		required_data['high'] = float(d['HIGH'])
		required_data['low'] = float(d['LOW'])
		required_data['open_price'] = float(d['OPEN'])
		required_data['change'] = required_data['current_price'] - float(d['CLOSE']) 
		required_data['change_per'] = float(required_data['change']*100)/float(d['OPEN']) 
		required_data['trade_Qty'] = float(d['TOTALQTYTRADED'])/100000
		required_data['trade_Value'] = float(d['VALUE'])

		yield (required_data,d['INSTRUMENTIDENTIFIER'])



#=================================================================================================================


@onlyAtGoodTime
def stockdata():
	print("Stockdata called!!")
	json_data = getRemoteData(nse_url)
	company = json_data['latestData'][0]

	c,__ = Stock_data.objects.get_or_create(symbol='NIFTY 50')
	c.current_price = float(company['ltp'].replace(",",""))
	c.high = float(company['high'].replace(",",""))
	c.low = float(company['low'].replace(",",""))
	c.open_price = float(company['open'].replace(",",""))
	c.change = float(company['ch'].replace(",",""))
	c.change_per = float(company['per'].replace(",",""))
	c.trade_Qty = float(json_data['trdVolumesum'].replace(",",""))
	c.trade_Value = float(json_data['trdValueSum'].replace(",",""))
	c.save()

	company_data_generator = getBulkData()

	for data,symbol in company_data_generator:
		c,__ = Stock_data.objects.get_or_create(symbol=symbol)
		c.current_price = data['current_price'] 
		c.high = data['high']
		c.low = data['low']
		c.open_price = data['open_price']
		c.change = data['change']
		c.change_per = data['change_per']
		c.trade_Qty = data['trade_Qty']
		c.trade_Value = data['trade_Value']
		c.save()


#===============STOCK UPDATE FOR GRAPH=============

@onlyAtGoodTime
def oldstockdata():
	json_data = getRemoteData(nse_url)
	company=json_data['latestData'][0]
	c=Old_Stock_data(symbol="NIFTY 50",
		current_price=company['ltp'].replace(",",""),
		)
	c.save() 	 	




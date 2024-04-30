import sys, getopt

import datetime
import time

from time import sleep
from pandas import read_csv


def run_sim_slow_turtle(file_name, window_size_short, window_size_long, max_loss, coin, cash, debug):
	df = read_csv(file_name,skiprows=0, sep=",", dtype={'Open': float, 'High': float, 'Low': float, 'Close': float})
	#Date,Open,High,Low,Close,Adj Close,Volume
	data = df[['Open','High','Low','Close']]
	
	fee = 0.0
	trades = 0
	data_len = len(data)
	close_price = 0.0
	multiplier = 1.0
	last_buy = 0.0
	last_sell = 0.0

	window_size_start = max(window_size_short, window_size_long)

	for i in range(window_size_start,data_len):
		high_price = data['High'][i]
		low_price = data['Low'][i]
		close_price_old = data['Close'][i-1]
		close_price = data['Close'][i]
		decision = 0

		if (window_size_short >= window_size_long):
			return (coin,cash,(coin + cash/close_price),(coin*close_price + cash),trades)	
		        		        
		if i == window_size_start:
			if (debug):
				print('MON',i,close_price,close_price,close_price,close_price,0,coin,cash,coin + cash/close_price,coin*close_price + cash,trades,0)
				
		aver_long = sum(data['Close'][i-(window_size_long*1):i+1])/window_size_long
		aver_short = sum(data['Close'][i-(window_size_short*1):i+1])/window_size_short
		min_range = min(data['Low'][i-window_size_short:i])
		max_range = max(data['High'][i-window_size_long:i])
		
		if i > window_size_start:
			if (coin > 0):
				#looking to sell
				if ((close_price < min_range) or (close_price < last_buy*(1-max_loss))):
					if last_buy == 0:
						last_buy = close_price
					if (debug):
						print('TRANS: SELL',i,coin*(1-fee),close_price,'from',last_buy,'P/L',(close_price-last_buy)*coin-coin*fee)
					cash = coin*close_price*(1-fee)
					coin = 0.0
					trades = trades + 1
					decision = -1
					last_sell = close_price
				
			elif (cash > 0):
				#looking to buy
				if (close_price > max_range):
					coin = cash/close_price*(1-fee)
					if last_sell == 0:
						last_sell = close_price
					if (debug):
						print('TRANS: BUY',i,coin,close_price*(1+fee),'from',last_sell,'P/L',0)
					cash = 0.0
					trades = trades + 1
					decision = 1
					last_buy = close_price
		
			if (debug):
				print('MON',i,close_price,min_range,max_range,close_price,0,coin,cash,coin + cash/close_price,coin*close_price + cash,trades,decision)
                    

	if (debug):
		print('MON',data_len,close_price,min_range,max_range,close_price,0,coin,cash,coin + cash/close_price,coin*close_price + cash,trades,decision)
	return (coin,cash,(coin + cash/close_price),(coin*close_price + cash),trades)	


def main(argv):
	symbol= ''
	#this is how many coins you want to buy or sell, used to find bid price
	targetTrade=0.0
	outputfile = ''
	if len(argv) != 7:
		print ('python backtester.py <data_file> <window_short> <window_long> <max_loss> <start_coin> <start_cash> <debug>')
		sys.exit(2)
	else:
		data_file=argv[0]
		window_size_short=int(argv[1])
		window_size_long=int(argv[2])
			
		max_loss=float(argv[3])/100.0
		start_coin=float(argv[4])
		start_cash=float(argv[5])
		if argv[6] == 'True':
			debug = True
		else:
			debug = False

		if window_size_long <= window_size_short:
			if debug:
				print('window_size_long must be greater than window_size_short, exiting without running backtesting...')
			else:
				best_exp = (window_size_short, window_size_long, max_loss*100, start_coin,start_cash,start_coin,start_cash,0)
				print('best experiment for file',data_file,best_exp)
			sys.exit(2)

	if debug:
		print('MON','timestamp','weightedPrice','RollingMin','RollingMax','averPrice','stdevPrice','coin','cash','curBalanceCoin','curBalanceDollar','trades','decision')
	(coin,cash,balance_coin,balance_cash,trades) = run_sim_slow_turtle(data_file, window_size_short, window_size_long, max_loss, start_coin, start_cash, debug)
	best_exp = (window_size_short, window_size_long, max_loss*100, start_coin,start_cash,balance_coin,balance_cash,trades)
	if debug == False:
		print('best experiment for file',data_file,best_exp)
			

if __name__ == "__main__":
   main(sys.argv[1:])




    	

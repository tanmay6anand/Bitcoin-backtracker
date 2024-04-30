# uses the date_to_milliseconds and interval_to_milliseconds functions
# https://gist.github.com/sammchardy/3547cfab1faf78e385b3fcb83ad86395
# https://gist.github.com/sammchardy/fcbb2b836d1f694f39bddd569d1c16fe

import sys, getopt
from binance.client import Client
import time

def get_historical_klines(symbol, interval, start_str, end_str=None):
    """Get Historical Klines from Binance
    See dateparse docs for valid start and end string formats http://dateparser.readthedocs.io/en/latest/
    If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"
    :param symbol: Name of symbol pair e.g BNBBTC
    :type symbol: str
    :param interval: Biannce Kline interval
    :type interval: str
    :param start_str: Start date string in UTC format
    :type start_str: str
    :param end_str: optional - end date string in UTC format
    :type end_str: str
    :return: list of OHLCV values
    """
    # create the Binance client, no need for api key
    client = Client("", "")

    # init our list
    output_data = []

    # setup the max limit
    limit = 500

    # convert interval to useful value in seconds
    timeframe = interval_to_milliseconds(interval)

    # convert our date strings to milliseconds
    start_ts = date_to_milliseconds(start_str)

    # if an end time was passed convert it
    end_ts = None
    if end_str:
        end_ts = date_to_milliseconds(end_str)

    idx = 0
    # it can be difficult to know when a symbol was listed on Binance so allow start time to be before list date
    symbol_existed = False
    while True:
        # fetch the klines from start_ts up to max 500 entries or the end_ts if set
        temp_data = client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit,
            startTime=start_ts,
            endTime=end_ts
        )

        # handle the case where our start date is before the symbol pair listed on Binance
        if not symbol_existed and len(temp_data):
            symbol_existed = True

        if symbol_existed:
            # append this loops data to our output data
            output_data += temp_data

            # update our start timestamp using the last value in the array and add the interval timeframe
            start_ts = temp_data[len(temp_data) - 1][0] + timeframe
        else:
            # it wasn't listed yet, increment our start date
            start_ts += timeframe

        idx += 1
        # check if we received less than the required limit and exit the loop
        if len(temp_data) < limit:
            # exit the while loop
            break

        # sleep after every 3rd call to be kind to the API
        if idx % 3 == 0:
            time.sleep(1)

    return output_data

def main(argv):
	symbol= ''
	#this is how many coins you want to buy or sell, used to find bid price
	targetTrade=0.0
	outputfile = ''
	if len(argv) != 5:
		print ('python binance-reader-candle.py <coin_symbol> <START_TIME_SEC> <END_TIME_SEC> <STEP_SEC> <output_file>')
		sys.exit(2)
	else:
		symbol=argv[0]
		#stime = "01/12/2011"
		START_TIME = int(argv[1])
		#START_TIME = round(datetime.datetime.strptime(argv[1], "%m/%d/%Y").replace(tzinfo=datetime.timezone.utc).timestamp())
		END_TIME = int(argv[2])
		#END_TIME = round(datetime.datetime.strptime(argv[2], "%m/%d/%Y").replace(tzinfo=datetime.timezone.utc).timestamp())
		STEP = argv[3]
		outputfile=argv[4]
		#outputfileTrade=argv[5]

	data = get_historical_klines(symbol, STEP, START_TIME, END_TIME)
	print(data)
	print('finished!')

if __name__ == "__main__":
   main(sys.argv[1:])




    	

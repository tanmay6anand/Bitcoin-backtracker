Author: Tanmay Anand

Date: 04-30-24

Requirements: Python 3.x

Libraries: pandas and plotly

Tools: parallel, sort

Questions: tanmay6anand@gmail.com



#run backtester and get just the output
#usage: python backtester.py <data_file> <window_short> <window_long> <max_loss> <start_coin> <start_cash> <debug>
```properties
python backtester.py btcusd-2018-2023.csv 10 30 50 0 1000 False
```

#run backtester and get all output for each time entry in datafile
```properties
python backtester.py btcusd-2018-2023.csv 10 30 50 0 1000 True
```

#run backtester and get all output for each time entry in datafile needed to plot results, and store it in results.txt
```properties
python backtester.py btcusd-2018-2023.csv 10 30 50 0 1000 True | grep MON > results.txt
```
#generate plot from results.txt file and save it in results.html file
#Usage: python graphresults.py <file_name_input> <file_name_output> <show>
```properties
python graphresults.py results.txt results.html True
```
#run in parallel 16 backtesting runs with different parameters and store results in parameter-sweep.txt
```properties
time parallel -j 16 --bar -k python backtester.py btcusd-2018-2023.csv {1} {2} {3} 0 1000 False ::: 10 20 30 40 ::: 10 20 30 40 ::: 10 20 30 40 > parameter-sweep.txt
```
#sort results in parameter-sweep.txt based on final balance (12th column)
```properties
sort parameter-sweep.txt -k12,12n | tail
```
#retrieve candle data from Binance
#python binance-reader-candle.py <coin_symbol> <START_TIME_SEC> <END_TIME_SEC> <STEP_SEC> <output_file>
```properties
python binance-reader-candle.py BTCUSD 1677045600 1677132000 1 btcusd.csv
```
import pandas as pd
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import plotly.express as px
import math

class backtester():
	def __init__(self):
		pass
	

	def importData(self, file,skip_nth):
		df1 = pd.read_csv(file, parse_dates=['timestamp'], delimiter=' ')

		df1 = df1[df1['decision'] != 0]
		
		df2 = pd.read_csv(file, parse_dates=['timestamp'], delimiter=' ')
		df2 = df2[df2.index % skip_nth == 0] 
		
		frames = [df1, df2]

		self.df = pd.concat(frames)		
		self.df = self.df.sort_index()

		print(self.df)
		
	def makePlots(self, file, show):
        # Initiate a fig that contains 3 subplots
		fig = make_subplots(rows=3, cols=1, vertical_spacing=0.02, shared_xaxes=True)

        # Main - Price plot
        #   This plot to be displayed at the bottom or row 3
		#
		fig.append_trace(go.Scatter(x=self.df['timestamp'], y=self.df['RollingMin'], name='Price Min'), row=3, col=1)
		fig.append_trace(go.Scatter(x=self.df['timestamp'], y=self.df['RollingMax'], name='Price Max'), row=3, col=1)
		#
		fig.append_trace(go.Scatter(x=self.df['timestamp'], y=self.df['weightedPrice'], name='Price'), row=3, col=1)
        
		# # BUY marker for Main plot
		fig.append_trace(go.Scatter(x=self.df[self.df['decision'] == 1]['timestamp'], y=self.df[self.df['decision'] == 1]['weightedPrice'],legendgroup='group1', mode='markers', marker_symbol='triangle-up', marker_color='green',marker_size=15, text='BUY', name='BUY decision'), row=3, col=1)
		# # SELL marker for Main plot
		fig.append_trace(go.Scatter(x=self.df[self.df['decision'] == -1]['timestamp'],y=self.df[self.df['decision'] == -1]['weightedPrice'], legendgroup='group2',mode='markers', marker_symbol='triangle-down', marker_color='red',marker_size=15, text='SELL', name='SELL decision'), row=3, col=1)

        # Bid/Ask spread
        #   This plot to be displayed at the top or row 1
		fig.append_trace(go.Scatter(x=self.df['timestamp'], y=self.df['curBalanceCoin'], name='Balance Coin'), row=1, col=1)

        # Volume
        #   Plot on a separate subplot
		fig.append_trace(go.Scatter(x=self.df['timestamp'], y=self.df['curBalanceDollar'], name='Balance $'), row=2, col=1)

        # Hides all xticks label except the last row i.e. row 3
		fig.update_xaxes(showticklabels=False)
		fig.update_xaxes(showticklabels=True, row=3, col=1)

        # Axis labels
		fig['layout']['xaxis3']['title'] = 'Data Source:'+' -- '+file
		fig['layout']['yaxis']['title'] = 'Balance (Coin)'
		fig['layout']['yaxis2']['title'] = 'Balance ($)'
		fig['layout']['yaxis3']['title'] = 'Price ($)'

        # Option to export plot as HTML
		#if toCSV: 
		plotly.offline.plot(fig, filename=file, auto_open=False)
				
		if show:
			fig.show()


def main():
	# grammar check
	args = sys.argv[1:]
	if len(args) != 3:
		print("Usage: python graphresults.py <file_name_input> <file_name_output> <show>")
		sys.exit(0)

	backtest = backtester()
	backtest.importData(args[0],1)
	if args[2] == 'True':
		show = True
	else:
		show = False
	backtest.makePlots(args[1],show)

if __name__ == '__main__':
	main()
import matplotlib.pyplot as plt
import datetime as dt
import pandas_datareader as web
plt.style.use('dark_background')

class UserInputs:

    ticker = input('enter ticker symbol:')
    tf = input('enter timeframe:')
    year = int(input('what year would you like to start test?'))
    initial_principle = float(input('enter initial investment:'))
    og_principle = initial_principle

    # load stock data
    start = dt.datetime(year, 1, 1)
    end = dt.datetime.now()
    df = web.DataReader(ticker, 'yahoo', start, end)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import pandas_datareader as web
import mplfinance as mpf

# initial user inputs
ticker = input('enter ticker symbol:')
tf = input('enter timeframe:')

# load stock data
start = dt.datetime(2000, 1, 1)
end = dt.datetime.now()
df = web.DataReader(ticker, 'yahoo', start, end)

# manipulates data time frame
def resample():
    global df
    df = df.resample(tf).agg(
                {'Close': 'last',
                 'High': 'max',
                 'Low': 'min',
                 'Open': 'first',
                 'Volume': 'sum'}).dropna()

# all strategies w/ static methods
class Strategies:
    pos = 0
    buys = []
    sells = []

# opening & closing positions
    @staticmethod
    def opening(i):
        buying_price = df['Close'][i].round(2)
        Strategies.buys.append(buying_price)
        print(f'--buying @ {buying_price}')
    @staticmethod
    def closing(i):
        selling_price = df['Close'][i].round(2)
        Strategies.sells.append(selling_price)
        print(f'--selling @ {selling_price}')

# sma buying strats
    @staticmethod
    def SMAandSMA(short, long):

        for i in range(0, len(df.index)):
            close = df['Close'][i].round(2)
            df['short'] = df['Close'].rolling(window=short).mean()[i]
            df['long'] = df['Close'].rolling(window=long).mean()[i]

            if df['short'][i] > df['long'][i] and Strategies.pos == 0:
                Strategies.pos = 1
                Strategies.opening(i)

            elif df['short'][i] < df['long'][i] and Strategies.pos == 1:
                Strategies.pos = 0
                Strategies.closing(i)

            elif Strategies.pos == 1:
                print(f'holding @ {close}')

            else:
                print(f'No Positiion {close}')

    @staticmethod
    def SMAandEMA(sma, ema):

        for i in range(0, len(df.index)):
            close = df['Close'][i].round(2)
            df['short_sma'] = df['Close'].rolling(window=sma).mean()[i]
            df['long_ema'] = df.Close.ewm(span=ema, adjust=False).mean()[i]

            if df['short_sma'][i] > df['long_ema'][i] and Strategies.pos == 0:
                Strategies.pos = 1
                Strategies.opening(i)

            elif df['short_sma'][i] < df['long_ema'][i] and Strategies.pos == 1:
                Strategies.pos = 0
                Strategies.closing(i)

            elif Strategies.pos == 1:
                print(f'holding @ {close}')

            else:
                print(f'No Positiion {close}')

    @staticmethod
    def SMAandMACD(sma, span):

        # macd strategy
        short_ema = df.Close.ewm(span=12, adjust=False).mean()
        long_ema = df.Close.ewm(span=26, adjust=False).mean()

        MACD = short_ema - long_ema
        signal = MACD.ewm(span=span, adjust=False).mean()

        df['macd'] = MACD
        df['signal'] = signal

        for i in range(0, len(df.index)):
            close = df['Close'][i].round(2)
            df['sma'] = df['Close'].rolling(window=sma).mean()[i]

            if close > df['short_sma'][i] and Strategies.pos == 0:
                Strategies.pos = 1
                Strategies.opening(i)

            elif df['macd'][i] < df['signal'][i] and Strategies.pos == 1:
                Strategies.pos = 0
                Strategies.closing(i)

            elif Strategies.pos == 1:
                print(f'holding @ {close}')

            else:
                print(f'No Positiion {close}')

# ema buying strats
    @staticmethod
    def EMAandEMA(short, long):
        for i in range(0, len(df.index)):
            close = df['Close'][i].round(2)
            df['short_ema'] = df.Close.ewm(span=short, adjust=False).mean()[i]
            df['long_ema'] = df.Close.ewm(span=long, adjust=False).mean()[i]

            if df['short_ema'][i] > df['long_ema'][i] and Strategies.pos == 0:
                Strategies.pos = 1
                Strategies.opening(i)

            elif df['short_ema'][i] < df['long_ema'][i] and Strategies.pos == 1:
                Strategies.pos = 0
                Strategies.closing(i)

            elif Strategies.pos == 1:
                print(f'holding @ {close}')

            else:
                print(f'No Positiion {close}')

    @staticmethod
    def EMAandSMA(ema, sma):
        for i in range(0, len(df.index)):
            close = df['Close'][i].round(2)
            df['ema'] = df.Close.ewm(span=ema, adjust=False).mean()[i]
            df['sma'] = df['Close'].rolling(window=sma).mean()[i]

            if close > df['ema'][i] and Strategies.pos == 0:
                Strategies.pos = 1
                Strategies.opening(i)

            elif close < df['sma'][i] and Strategies.pos == 1:
                Strategies.pos = 0
                Strategies.closing(i)

            elif Strategies.pos == 1:
                print(f'holding @ {close}')

            else:
                print(f'No Positiion {close}')

    @staticmethod
    def EMAandMACD(ema, span):
        # macd strategy
        short_ema = df.Close.ewm(span=12, adjust=False).mean()
        long_ema = df.Close.ewm(span=26, adjust=False).mean()

        MACD = short_ema - long_ema
        signal = MACD.ewm(span=span, adjust=False).mean()

        df['macd'] = MACD
        df['signal'] = signal

        for i in range(0, len(df.index)):
            close = df['Close'][i].round(2)
            df['ema'] = df.Close.ewm(span=ema, adjust=False).mean()[i]


            if close > df['ema'][i] and Strategies.pos == 0:
                Strategies.pos = 1
                Strategies.opening(i)

            elif df['macd'][i] < df['signal'][i] and Strategies.pos == 1:
                Strategies.pos = 0
                Strategies.closing(i)

            elif Strategies.pos == 1:
                print(f'holding @ {close}')

            else:
                print(f'No Positiion {close}')

# macd buying strats
    @staticmethod
    def MACDandMACD(span_buy, span_sell):
        # macd strategy
        short_ema = df.Close.ewm(span=12, adjust=False).mean()
        long_ema = df.Close.ewm(span=26, adjust=False).mean()

        MACD = short_ema - long_ema
        signal_buy = MACD.ewm(span=span_buy, adjust=False).mean()
        signal_sell = MACD.ewm(span=span_sell, adjust=False).mean()

        df['macd'] = MACD
        df['signal_buy'] = signal_buy
        df['signal_sell'] = signal_sell

        for i in range(0, len(df.index)):
            close = df['Close'][i].round(2)

            if df['signal_buy'][i] > df['macd'][i] and Strategies.pos == 0:
                Strategies.pos = 1
                Strategies.opening(i)

            elif df['signal_sell'] < df['macd'] and Strategies.pos == 1:
                Strategies.pos = 0
                Strategies.closing(i)

            elif Strategies.pos == 1:
                print(f'holding @ {close}')

            else:
                print(f'No Positiion {close}')

    @staticmethod
    def MACDandSMA(span, sma):
        # macd strategy
        short_ema = df.Close.ewm(span=12, adjust=False).mean()
        long_ema = df.Close.ewm(span=26, adjust=False).mean()

        MACD = short_ema - long_ema
        signal= MACD.ewm(span=span, adjust=False).mean()

        df['macd'] = MACD
        df['signal'] = signal

        for i in range(0, len(df.index)):
            close = df['Close'][i].round(2)
            df['sma'] = df['Close'].rolling(window=sma).mean()[i]

            if df['signal'][i] > df['macd'][i] and Strategies.pos == 0:
                Strategies.pos = 1
                Strategies.opening(i)

            elif df['sma'] < close and Strategies.pos == 1:
                Strategies.pos = 0
                Strategies.closing(i)

            elif Strategies.pos == 1:
                print(f'holding @ {close}')

            else:
                print(f'No Positiion {close}')

    @staticmethod
    def MACDandEMA(span, ema):
        # macd strategy
        short_ema = df.Close.ewm(span=12, adjust=False).mean()
        long_ema = df.Close.ewm(span=26, adjust=False).mean()

        MACD = short_ema - long_ema
        signal = MACD.ewm(span=span, adjust=False).mean()

        df['macd'] = MACD
        df['signal'] = signal

        for i in range(0, len(df.index)):
            close = df['Close'][i].round(2)
            df['ema'] = df.Close.ewm(span=ema, adjust=False).mean()[i]

            if df['signal'][i] > df['macd'][i] and Strategies.pos == 0:
                Strategies.pos = 1
                Strategies.opening(i)

            elif df['ema'][i] < close and Strategies.pos == 1:
                Strategies.pos = 0
                Strategies.closing(i)

            elif Strategies.pos == 1:
                print(f'holding @ {close}')

            else:
                print(f'No Positiion {close}')

# user selects strategy... runs strategies class
class SelectStrategy:

    buy_choice = input('what indicator would you like to buy on? \n'
                   '1) SMA \n'
                   '2) EMA \n'
                   '3) MACD \n')

    @staticmethod
    def buy_sma():
            sell_choice = input('what indicator would you like to sell on? \n'
                       '1) SMA \n'
                       '2) EMA \n'
                       '3) MACD \n')
            if 'sma' in sell_choice.lower():
                short = int(input('enter short SMA length'))
                long = int(input('enter long SMA length'))
                Strategies.SMAandSMA(short, long)
            elif 'ema' in sell_choice.lower():
                short_sma = int(input('enter short SMA length'))
                long_ema = int(input('enter long EMA length'))
                Strategies.SMAandEMA(short_sma, long_ema)
            else:
                short_sma = int(input('enter short SMA length'))
                span = int(input('enter MACD span'))
                Strategies.SMAandMACD(short_sma, span)

    @staticmethod
    def buy_ema():
        sell_choice = input('what indicator would you like to sell on? \n'
                            '1) SMA \n'
                            '2) EMA \n'
                            '3) MACD \n')
        if 'sma' in sell_choice.lower():
            ema = int(input('enter length for ema'))
            sma = int(input('enter length for sma'))
            Strategies.EMAandSMA(ema, sma)
        elif 'ema' in sell_choice.lower():
            short = int(input('enter length for buying ema'))
            long = int(input('enter length for selling ema'))
            Strategies.EMAandEMA(short, long)
        else:
            ema = int(input('enter length for ema'))
            span = int(input('enter length for macd span'))
            Strategies.EMAandMACD(ema, span)

    @staticmethod
    def buy_macd():
        sell_choice = input('what indicator would you like to sell on? \n'
                            '1) SMA \n'
                            '2) EMA \n'
                            '3) MACD \n')
        if 'sma' in sell_choice.lower():
            span = int(input('enter length for macd span'))
            sma = int(input('enter length for sma'))
            Strategies.MACDandSMA(span, sma)
        elif 'ema' in sell_choice.lower():
            span = int(input('enter length for macd span'))
            ema = int(input('enter length for ema'))
            Strategies.MACDandEMA(span, ema)
        else:
            span_buy = int(input('enter length for buying macd span'))
            span_sell = int(input('enter length for selling macd span'))
            Strategies.MACDandMACD(span_buy, span_sell)

    @staticmethod
    def execute():
        if 'sma' in SelectStrategy.buy_choice.lower():
            SelectStrategy.buy_sma()

        elif 'ema' in SelectStrategy.buy_choice.lower():
            SelectStrategy.buy_ema()

        else:
            SelectStrategy.buy_macd()

resample()
SelectStrategy.execute()

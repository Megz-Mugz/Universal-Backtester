from Model.UserInputs import UserInputs

import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import pandas_datareader as web
from sklearn.metrics import r2_score
plt.style.use('dark_background')

df = 0

# all strategies w/ static methods
class Strategies:
    pos = 0
    buys = []
    sells = []
    percent_change = []
    wins = []
    losses = []
    principle_change = []

# manipulates data time frame
    @staticmethod
    def resample():
        global df
        df = UserInputs.df.resample(UserInputs.tf).agg(
            {'Close': 'last',
             'High': 'max',
             'Low': 'min',
             'Open': 'first',
             'Volume': 'sum'}).dropna()

# opening & closing positions
    @staticmethod
    def opening(i):
        buying_price = df['Close'][i].round(2)
        Strategies.buys.append(buying_price)
        # print(f'--buying @ {buying_price}')
    @staticmethod
    def closing(i):
        selling_price = df['Close'][i].round(2)
        Strategies.sells.append(selling_price)
        # print(f'--selling @ {selling_price}')
    @staticmethod
    def holding(i):
        # print(f'holding @ {df["Close"][i].round(2)}')
        pass
    @staticmethod
    def closed(i):
        # print(f'No Positiion {df["Close"][i].round(2)}')
        pass

    # sma buying strats
    @staticmethod
    def SMAandSMA(buying_sma, selling_sma):

        for i in range(0, len(df.index)):
            close = df['Close'][i].round(2)
            df['buying'] = df['Close'].rolling(window=buying_sma).mean()[i]
            df['selling'] = df['Close'].rolling(window=selling_sma).mean()[i]

            if close > df['buying'][i] and Strategies.pos == 0:
                Strategies.pos = 1
                Strategies.opening(i)

            elif close < df['selling'][i] and Strategies.pos == 1:
                Strategies.pos = 0
                Strategies.closing(i)

            elif Strategies.pos == 1:
                Strategies.holding(i)
            else:
                Strategies.closed(i)

    @staticmethod
    def SMAandEMA(buying_sma, selling_ema):

        for i in range(0, len(df.index)):
            close = df['Close'][i].round(2)
            df['buying_sma'] = df['Close'].rolling(window=buying_sma).mean()[i]
            df['selling_ema'] = df.Close.ewm(span=selling_ema, adjust=False).mean()[i]

            if close > df['buying_sma'][i] and Strategies.pos == 0:
                Strategies.pos = 1
                Strategies.opening(i)

            elif close < df['selling_ema'][i] and Strategies.pos == 1:
                Strategies.pos = 0
                Strategies.closing(i)

            elif Strategies.pos == 1:
                Strategies.holding(i)

            else:
                Strategies.closed(i)

    @staticmethod
    def SMAandMACD(buying_sma, selling_span):

        # macd strategy
        short_ema = df.Close.ewm(span=12, adjust=False).mean()
        long_ema = df.Close.ewm(span=26, adjust=False).mean()

        MACD = short_ema - long_ema
        signal = MACD.ewm(span=selling_span, adjust=False).mean()

        df['macd'] = MACD
        df['signal'] = signal

        for i in range(0, len(df.index)):
            close = df['Close'][i].round(2)
            df['buying_sma'] = df['Close'].rolling(window=buying_sma).mean()[i]

            if close > df['buying_sma'][i] and Strategies.pos == 0:
                Strategies.pos = 1
                Strategies.opening(i)

            elif df['macd'][i] < df['signal'][i] and Strategies.pos == 1:
                Strategies.pos = 0
                Strategies.closing(i)

            elif Strategies.pos == 1:
                Strategies.holding(i)
            else:
                Strategies.closed(i)

# ema buying strats
    @staticmethod
    def EMAandEMA(buying_ema, selling_ema):
        for i in range(0, len(df.index)):
            close = df['Close'][i].round(2)
            df['buying_ema'] = df.Close.ewm(span=buying_ema, adjust=False).mean()[i]
            df['selling_ema'] = df.Close.ewm(span=selling_ema, adjust=False).mean()[i]

            if close > df['buying_ema'][i] and Strategies.pos == 0:
                Strategies.pos = 1
                Strategies.opening(i)

            elif close < df['selling_ema'][i] and Strategies.pos == 1:
                Strategies.pos = 0
                Strategies.closing(i)

            elif Strategies.pos == 1:
                Strategies.holding(i)

            else:
                Strategies.closed(i)

    @staticmethod
    def EMAandSMA(buying_ema, selling_sma):
        for i in range(0, len(df.index)):
            close = df['Close'][i].round(2)
            df['buying_ema'] = df.Close.ewm(span=buying_ema, adjust=False).mean()[i]
            df['selling_ema'] = df['Close'].rolling(window=selling_sma).mean()[i]

            if close > df['buying_ema'][i] and Strategies.pos == 0:
                Strategies.pos = 1
                Strategies.opening(i)

            elif close < df['selling_sma'][i] and Strategies.pos == 1:
                Strategies.pos = 0
                Strategies.closing(i)

            elif Strategies.pos == 1:
                Strategies.holding(i)

            else:
                Strategies.closed(i)

    @staticmethod
    def EMAandMACD(buying_ema, selling_span):
        # macd strategy
        short_ema = df.Close.ewm(span=12, adjust=False).mean()
        long_ema = df.Close.ewm(span=26, adjust=False).mean()

        MACD = short_ema - long_ema
        signal = MACD.ewm(span=selling_span, adjust=False).mean()

        df['macd'] = MACD
        df['signal'] = signal

        for i in range(0, len(df.index)):
            close = df['Close'][i].round(2)
            df['buying_ema'] = df.Close.ewm(span=buying_ema, adjust=False).mean()[i]


            if close > df['buying_ema'][i] and Strategies.pos == 0:
                Strategies.pos = 1
                Strategies.opening(i)

            elif df['macd'][i] < df['signal'][i] and Strategies.pos == 1:
                Strategies.pos = 0
                Strategies.closing(i)

            elif Strategies.pos == 1:
                Strategies.holding(i)

            else:
                Strategies.closed(i)

# macd buying strats
    @staticmethod
    def MACDandMACD(buying_span, selling_span):
        # macd strategy
        short_ema = df.Close.ewm(span=12, adjust=False).mean()
        long_ema = df.Close.ewm(span=26, adjust=False).mean()

        MACD = short_ema - long_ema
        signal_buy = MACD.ewm(span=buying_span, adjust=False).mean()
        signal_sell = MACD.ewm(span=selling_span, adjust=False).mean()

        df['macd'] = MACD
        df['signal_buy'] = signal_buy
        df['signal_sell'] = signal_sell

        for i in range(0, len(df.index)):
            close = df['Close'][i].round(2)

            if df['signal_buy'][i] > df['macd'][i] and Strategies.pos == 0:
                Strategies.pos = 1
                Strategies.opening(i)

            elif df['signal_sell'][i] < df['macd'][i] and Strategies.pos == 1:
                Strategies.pos = 0
                Strategies.closing(i)

            elif Strategies.pos == 1:
                Strategies.holding(i)

            else:
                Strategies.closed(i)

    @staticmethod
    def MACDandSMA(buying_span, selling_sma):
        # macd strategy
        short_ema = df.Close.ewm(span=12, adjust=False).mean()
        long_ema = df.Close.ewm(span=26, adjust=False).mean()

        MACD = short_ema - long_ema
        signal= MACD.ewm(span=buying_span, adjust=False).mean()

        df['macd'] = MACD
        df['signal'] = signal

        for i in range(0, len(df.index)):
            close = df['Close'][i].round(2)
            df['selling_sma'] = df['Close'].rolling(window=selling_sma).mean()[i]

            if df['signal'][i] > df['macd'][i] and Strategies.pos == 0:
                Strategies.pos = 1
                Strategies.opening(i)

            elif close < df['selling_sma'][i] and Strategies.pos == 1:
                Strategies.pos = 0
                Strategies.closing(i)

            elif Strategies.pos == 1:
                Strategies.holding(i)

            else:
                Strategies.closed(i)

    @staticmethod
    def MACDandEMA(buying_span, selling_ema):
        # macd strategy
        short_ema = df.Close.ewm(span=12, adjust=False).mean()
        long_ema = df.Close.ewm(span=26, adjust=False).mean()

        MACD = short_ema - long_ema
        signal = MACD.ewm(span=buying_span, adjust=False).mean()

        df['macd'] = MACD
        df['signal'] = signal

        for i in range(0, len(df.index)):
            close = df['Close'][i].round(2)
            df['selling_ema'] = df.Close.ewm(span=selling_ema, adjust=False).mean()[i]

            if df['signal'][i] > df['macd'][i] and Strategies.pos == 0:
                Strategies.pos = 1
                Strategies.opening(i)

            elif close < df['selling_ema'][i] and Strategies.pos == 1:
                Strategies.pos = 0
                Strategies.closing(i)

            elif Strategies.pos == 1:
                Strategies.holding(i)

            else:
                Strategies.closed(i)

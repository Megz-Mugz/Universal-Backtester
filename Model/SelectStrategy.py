from Model.Strategies import Strategies

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
                buying = int(input('enter buying SMA length'))
                selling = int(input('enter selling SMA length'))
                Strategies.SMAandSMA(buying, selling)
            elif 'ema' in sell_choice.lower():
                buying_sma = int(input('enter buying SMA length'))
                selling_ema = int(input('enter selling EMA length'))
                Strategies.SMAandEMA(buying_sma, selling_ema)
            else:
                buying_sma = int(input('enter buying SMA length'))
                span = int(input('enter MACD span'))
                Strategies.SMAandMACD(buying_sma, span)

    @staticmethod
    def buy_ema():
        sell_choice = input('what indicator would you like to sell on? \n'
                            '1) SMA \n'
                            '2) EMA \n'
                            '3) MACD \n')
        if 'sma' in sell_choice.lower():
            buying_ema = int(input('enter length for buying ema'))
            selling_sma = int(input('enter length for selling sma'))
            Strategies.EMAandSMA(buying_ema, selling_sma)
        elif 'ema' in sell_choice.lower():
            short = int(input('enter length for buying ema'))
            long = int(input('enter length for selling ema'))
            Strategies.EMAandEMA(short, long)
        else:
            buying_ema = int(input('enter length for buying ema'))
            span = int(input('enter length for macd span'))
            Strategies.EMAandMACD(buying_ema, span)

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

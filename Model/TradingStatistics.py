from Model.Strategies import Strategies
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score
from Model.UserInputs import UserInputs

percent_change = []
wins = []
losses = []
principle_change = []

# provides trading analytics
class TradingStatistics:

# calculates wins & losses
    @staticmethod
    def success():
        if len(Strategies.buys) != len(Strategies.sells):
            del Strategies.buys[-1]

        for trade in range(len(Strategies.buys)):
            deci_pc = ((Strategies.sells[trade] - Strategies.buys[trade]) / Strategies.buys[trade])
            percent_change.append(deci_pc)
            pc = deci_pc * 100

            if pc < 0:
                losses.append(pc)
            else:
                wins.append(pc)

# takes initial investment and calculates return based on strategy
    @staticmethod
    def roi():
        initial_principle = UserInputs.initial_principle
        for change in range(0, len(percent_change)):
            np = initial_principle + (initial_principle * percent_change[change])
            initial_principle = np
            principle_change.append(np)

# prints stats
    @staticmethod
    def printers():
        og_principle = UserInputs.og_principle
        print('-------------------')
        print('-------------------')
        print('-------------------')
        print('Final Balance: ' + str('$') + str(principle_change[-1].round(2)))
        print('Return on Investment:' + str(((((principle_change[-1] - og_principle) / og_principle)*100).__round__(2))) + '%')
        print('-------------------')
        print('Total Trades:' + str(len(Strategies.buys)))
        print(('Success Rate:  ' + (str(((len(wins) / len(Strategies.buys)) * 100).__round__(2))) + str('%')))
        print('Total Wins: ' + str(len(wins)))
        print('Total Losses: ' + str(len(losses)))

    @staticmethod
    def equityCurve():
        plt.title(f'{UserInputs.ticker.upper()} on {UserInputs.tf.upper()} Equity Curve')
        plt.xlabel('Trades')
        plt.ylabel('Return on Investment')

        trades = []
        for k in range(len(principle_change)):
            trades.append(k)

        plt.plot(trades, principle_change, marker='o', markerfacecolor='red')

        # poly. regression
        mymodel = np.poly1d(np.polyfit(trades, principle_change, 5))
        myline = np.linspace(0, len(trades), len(principle_change))
        plt.plot(myline, mymodel(myline), color='green')
        print(f"R^2 Score: {r2_score(principle_change, mymodel(myline)).__round__(2)}")

        plt.legend(loc='best')
        plt.show()

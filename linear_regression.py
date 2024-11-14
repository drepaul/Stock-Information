import numpy as np
from datetime import datetime, timedelta
from stock_data import *

class LinearRegression:
    def __init__(self, x_data, y_data):
        self.x_data = x_data
        self.y_data = y_data
        self.days_arr = None

    def conv_date_to_int(self):
        start_date = self.x_data.min()
        self.days = np.array([(date - start_date).days for date in self.x_data])

        return self.days

    def linear_regression(self):
        days = self.conv_date_to_int()

        x_mean = np.mean(days)
        y_mean = np.mean(self.y_data)

        numerator = np.sum((days - x_mean) * (self.y_data - y_mean))
        denominator = np.sum((days - x_mean) ** 2)
        slope = numerator / denominator
        y_int = y_mean - slope * x_mean

        return slope, y_int


    def simple_moving_average(self, data, period):
        sma = []
        for i in range(period - 1, len(data)):
            win = data[i - period + 1: i + 1]
            win_avg = np.sum(win) / period
            sma.append(win_avg)

        return sma
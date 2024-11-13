import numpy as np
from datetime import datetime, timedelta
from stock_data import *

def conv_date_to_int(data):
    start_date = data.min()
    days = np.array([(date - start_date).days for date in data])

    return days


def linear_regression(x_data, y_data):
    days = conv_date_to_int(x_data)

    x_mean = np.mean(days)
    y_mean = np.mean(y_data)

    numerator = np.sum((days - x_mean) * (y_data - y_mean))
    denominator = np.sum((days - x_mean) ** 2)
    slope = numerator / denominator
    y_int = y_mean - slope * x_mean

    return slope, y_int


def simple_moving_average(data, period):
    sma = []
    for i in range(period - 1, len(data)):
        win = data[i - period + 1: i + 1]
        win_avg = np.sum(win) / period
        sma.append(win_avg)

    return sma
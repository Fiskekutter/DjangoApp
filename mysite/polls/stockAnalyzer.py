import math
import matplotlib as mp
import pandas as pd
import numpy as np


class stockAnalyzer():
    earnings = 0
    book_value = 0
    cash_flow = 0
    stock_price = 0
    dividend = 0
    volume = 0
    RSI_previous = {'gain': 123, 'loss': 123}
    
    
    def __init__():
        return 0
    
    
    def calc_intrisic_value(self):
        return 0
    
    def calc_book_value(self):
        return 0
    
    def calc_price_to_earnings(self):
        return 0
    
    def calc_bollinger_band(self):
        return 0
    
    #Look back is how many days the RSI is calculate over, diff_dict should have a loss and gain which contains the days where there was a loss/gain
    def calc_relative_strength_index(self, look_back, diff_dict):
        df = pd.from_dict(diff_dict, 'columns')
        average_gain = df.mean('gain')
        average_loss = df.mean('loss')
        
        
        average_gain = average_gain/look_back
        average_loss = average_loss/look_back
        calc = 100/(1+(average_gain/average_loss))
        RSI_step_one = 100 - calc
        
        
        if(self.RSI_previous['gain'].__eq__(123) or self.RSI_previous['loss'].__eq__(123)): 
            return 'Not Ready yet'
        
        x_ = self.RSI_previous['gain']*(look_back-1) + average_gain
        y_ = self.RSI_previous['loss']*(look_back-1) + average_loss
        
        RSI_step_two = 100 - (100/(1+(x_/y_)))
        
        self.RSI_previous['gain'] = average_gain
        self.RSI_previous['loss'] = average_loss
        
        return RSI_step_two
        
    
    def calc_moving_average(self, days):
        return 0
    
    def calc_MACD(self):
        return 0
    
    def calc_exponential_moving_average(self, days):
        return 0
    
        
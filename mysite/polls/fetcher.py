#Create class to collect google or youtube api
import pandas as pd
import matplotlib as plt
from .models import Stock, Stock_History
import requests
import numpy as np


class stock_api_data_collector_class():
    url = "something"
    prefix = "#232"
    #ticker = []
    start_date = '2010-01-01'
    end_date = '2016-12-31'
    data = {}
    
    def __init__(self):
        print('yes')
    
    def get_tickers(self):
        self.ticker.append()
    
    def get_stock_current_price(self, ticker):
        data = 0
        return data 
        
    def get_stock_data(self, ticker):
        self.data = self.transform_data(ticker)
    
    def get_stock_history_period(self, ticker, start_date, end_date):
        data = 0
        return data
    
    def get_stock_history_all(self, ticker):
        data = 0
        return data     
    
    def get_data(self, url):
        _headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        return pd.read_html(requests.get(url,headers = _headers).text)
    
    def transform_data(self, ticker):
        summary_data = self.get_data(f'https://finance.yahoo.com/quote/{ticker}?p={ticker}')
        data = [summary_data[0], summary_data[1]]
        data = pd.concat(summary_data)
        data.reset_index(drop=True, inplace=True)
        df = data.transpose()
        df.columns = df.iloc[0]
        df = df.drop(0)
        df = df.reset_index(drop=True)
        #return self.pop_assign_data(df.to_dict())
        return self.assign_data(df.to_dict())
        
    def historical(self, ticker):
        historiscal_url= f'https://finance.yahoo.com/quote/{ticker}/history?p={ticker}'
        historiscal_data = self.get_data(historiscal_url)
        data = historiscal_data[0]
        data = data.iloc[:-1 , :]
        data = data[data["Open"].str.contains("Dividend") == False]
        
    def assign_data(self, stock_info):
        stock_data = {'Previous Close': '', 
                      'Open': '', 
                      'Bid': '', 
                      'Ask': '', 
                      'Day\'s Range': '', 
                      '52 Week Range': '', 
                      'Volume': '', 
                      'Avg. Volume': '', 
                      'Market Cap': '', 
                      'Beta (5Y Monthly)': '', 
                      'PE Ratio (TTM)': '',
                      'EPS (TTM)': '',
                      'Earnings Date': '',
                      'Forward Dividend & Yield': '',
                      'Ex-Dividend Date': '', 
                      '1y Target Est': ''}
        for item in stock_data:
            stock_data[item] = stock_info[item][0]
        return stock_data
            
    def pop_assign_data(self, stock_info): #Not working
        for item in stock_info:
            item.update(item.pop(0, {}))
        return stock_info
        
    
#Create class to collect google or youtube api
import pandas as pd
import matplotlib as plt
from pandas_datareader import data
from .models import Stock, Stock_History

tickers = ['AAPL', 'MSFT', '^GSPC']

start_date = '2010-01-01'
end_date = '2016-12-31'

panel_data = data.DataReader('INPX', 'google', start_date, end_date)



class youtube_Api_Collector():
    url = "something"
    prefix = "#232"
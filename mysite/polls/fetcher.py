#Create class to collect google or youtube api
import pandas as pd
import matplotlib as plt
from .models import Stock, Stock_History
import requests
import numpy as np
from bs4 import BeautifulSoup
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
import os
import shutil



class stock_api_data_collector_class(): #Yahoo
    _headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    url = "something"
    prefix = "#232"
    ticker = []
    start_date = '2010-01-01'
    end_date = '2016-12-31'
    data = {}
    search_path = "C:\\Users\\45311\\Downloads\\"
    file_storage = "C:\\Users\\45311\\Documents\\Source\\DjangoApp\\mysite\\polls\\files\\"
    
    def __init__(self):
        self.get_tickers()
    
    def get_tickers(self):
        table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        df = table[0]
        dic = df.to_dict("list")
        self.ticker = dic["Symbol"]
    
    def get_stock_current_price(self, ticker):
        data = 0
        return data 
        
    def get_stock_data(self, ticker):
        self.data = self.transform_data(ticker)
    
    def get_stock_history_period(self, ticker, start_date, end_date):
        data = 0
        return data
         
    def get_current_stock_price(self, ticker):
        resp = requests.get(f'https://finance.yahoo.com/quote/{ticker}?p={ticker}', headers= self._headers)
        soup = BeautifulSoup(resp.content, "html.parser")
        value = soup.find_all('fin-streamer', class_="Fw(b) Fz(36px) Mb(-4px) D(ib)")
        value = value.__str__().split(" ")[-1].split('"')[1]
        return float(value)
    
    def get_data(self, url):
        return pd.read_html(requests.get(url,headers = self._headers).text)
    
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
        
    def historical(self, ticker): #only return 100 values because of html problems
        historiscal_url= f'https://finance.yahoo.com/quote/{ticker}/history?p={ticker}'
        historiscal_data = self.get_data(historiscal_url)
        data = historiscal_data[0]
        data = data.iloc[:-1 , :]
        data = data[data["Open"].str.contains("Dividend") == False]
        return data

    def html_scroller(self, ticker): #Works but is slow, use download_historical_data instead
        now = datetime.datetime.now()
        today = str(int(time.mktime(now.timetuple())))
        driver = webdriver.Firefox()
        driver.implicitly_wait(3)
        
        driver.get(f'https://finance.yahoo.com/quote/{ticker}/history?period1=0&period2={today}&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true')
        driver.find_element(By.XPATH, "/html/body/div/div/div/div/form/div[2]/div[2]/button").click()
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[4]/div/div/div[1]/div/div/div/div/div/section/button[2]").click()
        
        #element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[10719]/td[1]/span")
        #element = element.__str__().replace("<", '').replace(">",'')
        #driver.execute_script(f"{element}.scrollIntoView()")
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        
        long_xpath= "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[2]/table/tbody/tr[10719]/td[1]/span" #Too specific
        driver.implicitly_wait(0.1)
        check = True
        while(check):
            try:
                WebDriverWait(driver, 0.1).until(lambda x: x.find_element(By.XPATH, long_xpath).is_displayed())
            except(TimeoutException):
                driver.execute_script("window.scrollBy(0, 3000000)")
            else:
                check = False
            
            
        values = driver.find_elements(By.TAG_NAME, 'span')
        #soup = BeautifulSoup(driver.page_source, 'html.parser')
        #values = soup.find_all('span').__str__()
        #driver.quit()
        return values[0].__str__()
    
    def download_historical_data(self, ticker):
        now = datetime.datetime.now()
        today = str(int(time.mktime(now.timetuple())))
        driver = webdriver.Firefox()
        driver.implicitly_wait(5)
        driver.get(f'https://finance.yahoo.com/quote/{ticker}/history?period1=0&period2={today}&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true')
        self.html_find_data(driver)
        
        ticker = ticker.upper() + ".csv"
        time.sleep(2)
        self.copy_file_to_destination(self.search_path + ticker, self.file_storage + ticker)
        driver.close()
        
    def copy_file_to_destination(self, src_path, dst_path):
        if(not os.path.isfile(dst_path)):
            shutil.copy(src_path, dst_path)
        if(os.path.isfile(src_path)):
            os.remove(src_path)
        
    def html_find_data(self, driver):
        try:
            driver.find_element(By.XPATH, "/html/body/div/div/div/div/form/div[2]/div[2]/button").click() #cookies
        except(NoSuchElementException):
            pass
        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[4]/div/div/div[1]/div/div/div/div/div/section/button[2]").click() #popup
        except(NoSuchElementException):
            pass
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[1]/div[1]/div[1]/div/div/div").click() #Date popup
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[1]/div[1]/div[1]/div/div/div[2]/div/ul[2]/li[4]/button").click() #Max
        #driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/section/div[1]/div[1]/div[1]/div/div/div[2]/div/div[3]/button[1]").click() #done
        #driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[1]/div[1]/button").click() #apply
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[1]/div[2]/span[2]/a").click() #Download
        
    def get_stock_history_all(self, ticker):#Not Working right now
        now = datetime.datetime.now()
        today = str(int(time.mktime(now.timetuple())))
        #print(today)
        historiscal_url= f'https://finance.yahoo.com/quote/{ticker}/history?period1=0&period2={today}&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'
        historiscal_data = self.get_data(historiscal_url)
        data = historiscal_data[0]
        data = data.iloc[:-1 , :]
        data = data["Close*"]
        return data
        
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
        
        
class iextrading_fetcher(): #Not developed
    tickers = []
    url = "https://cloud.iexapis.com/stable/stock/aapl/quote?token=YOUR_TOKEN_HERE"
    
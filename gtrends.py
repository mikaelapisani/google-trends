#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 14:46:16 2019

@author: mikaelapisanileal
"""
from pytrends.request import TrendReq
import pandas as pd
from os import path

class GTrends:
    def __init__(self, encoding, tz, timeout_connect, timeout_read, retries, backoff_factor, geo):
        #initialize google trends connector
        self.pytrends = TrendReq(hl=encoding, 
                                 tz=tz,
                                 timeout=(timeout_connect, timeout_read),
                                 retries=retries,
                                 backoff_factor=backoff_factor)
        self.geo = geo
        
    def set_log(self, log):
        self.log = log

        
    #download file for ticker, category_name and time frame
    #if file already exists, do not download again
    def download_file(self, ticker, category_name, frame, local_path, monthly=False):
        try:
            if (path.exists(local_path)):
                return True
            self.pytrends.build_payload([ticker], cat=category_name, 
                           timeframe=frame, 
                           geo=self.geo, gprop='')
            self.log.info('Downloading data for ticker %s, category %s, frame %s' 
                          %(ticker, category_name, frame))
            data = self.pytrends.interest_over_time()
            df = pd.DataFrame(data)
            if (df.shape[0]==0):
                self.log.info('Empty file for ticker %s, category %s, frame %s' 
                          %(ticker, category_name, frame))
                return True
            if 'isPartial' in df.columns:
                df.drop('isPartial', axis=1, inplace=True)
                df.reset_index(level=0, inplace=True)
            df['ticker'] = ticker
            if (monthly):
                df['date'] = pd.to_datetime(df['date'])
                df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m'))
            df.to_csv(local_path, index=False)
            return True
        except Exception as ex:
            self.log.error('There has been an error downloading tracker %s, category %s, frame %s\n%s',
                           ticker, category_name, frame, ex)
            return False
    
    
    #for each ticker, download data monthly and daily for each category
    def import_data(self, tickers_path, year_from, year_until,categories, 
                    data_folder_monthly, data_folder_daily):
        lines = open(tickers_path).readlines()[1:]
        year_range = range(int(year_from),int(year_until))
        download_all = True
        for ticker in lines:
            ticker = ticker.rstrip('\n')
            self.log.info('Process ticker %s' %(ticker))
            for category in categories:
                category_type = category.split(':')
                category_name = category_type[0]
                category_type = category_type[1]
                if (category_type=='monthly'):
                    #download monthly data for all the year ranges
                    download_all = download_all and self.download_file(ticker, category_name, 
                                  year_from + '-01-01 ' + 
                                  year_until + '-12-31',
                                  data_folder_monthly + ticker + '_' 
                                  + category_name + '_monthly.csv', True)
                else:
                    for year in year_range:
                        #download first daily file for year
                        download_all = download_all and self.download_file(ticker, category_name, 
                                  str(year) + '-01-01 ' + str(year) + '-06-30',
                                  data_folder_daily + ticker + '_' +
                                  category_name + '_1_daily.csv')
                        
                        #download second daily file for year
                        download_all = download_all and self.download_file(ticker, category_name, 
                                  str(year) + '-07-01 ' + str(year) + '-12-31',
                                  data_folder_daily + ticker + '_' +
                                  category_name + '_2_daily.csv')
        return download_all
  
                        
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                
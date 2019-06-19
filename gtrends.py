#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 15:54:47 2019

@author: mikaelapisanileal
"""

#pytrends: https://github.com/GeneralMills/pytrends

import logging 
import sys
import getopt
import pandas as pd


from pytrends.request import TrendReq
from config import Config
from dropbox_handler import DropboxHandler
import files_manager


class GTrends:
    def __init__(self, config):
        
        #set config
        self.config = config
        logging.basicConfig(format='%(levelname)s:%(asctime)s - %(message)s')
        self.log = logging.getLogger()
        self.log.setLevel(logging.getLevelName(self.config.log_level))
        
        #initialize google trends connector
        self.pytrends = TrendReq(hl=self.config.encoding, 
                                 tz=self.config.tz,
                                 timeout=(self.config.gtrends_timeout_connect, 
                                          self.config.gtrends_timeout_read),
                                 retries=self.config.retries,
                                 backoff_factor=self.config.backoff_factor)

        #initialize dropbox connector
        self.dbx = DropboxHandler(self.config.access_token, 
                                  self.config.dropbox_timeout, 
                                  self.config.dropbox_chunck)


   
    #check if daily file exists in dropbox
    # if not exists, download from google trends and upload to dropbox
    def process_monthly(self, ticker, frame, category_name):
        self.log.info('Process monthly for ticker:%s and category:%s', ticker, category_name)
        dest_path = self.config.dropbox_folder_upload + ticker + '/'
        #assumption: if file for index 0 exists -> all month has been processed
        #then we don't process this data
        if (self.dbx.file_exists(dest_path, dest_path + ticker + '_' + category_name + '_0_monthly.csv')): 
            return;
            
        self.pytrends.build_payload([ticker],cat=category_name, 
                           timeframe=frame, 
                           geo=self.config.geo, gprop='')
        data = self.pytrends.interest_over_time()
        df = pd.DataFrame(data)
        df.reset_index(level=0, inplace=True)
        df.drop('isPartial', axis=1, inplace=True)
        df['date'] = pd.to_datetime(df['date'])
        df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m'))
        #save data to dropbox
        files_manager.save_data(self.config.data_folder,
                                ticker + '_' + category_name,
                                '_monthly.csv',
                                self.config.dropbox_folder_upload + ticker + '/',df, 
                                self.config.output_size_mb,0, dbx)
        return df
 
    # check if daily files exists in dropbox
    # if not exists, download from google trends and upload to dropbox
    def process_daily(self, df, index, ticker, category_name, frame):
        dest_path = self.config.dropbox_folder_upload + ticker + '/'
        
        #assumption: if file for index 0 exists -> all daily data for this 
        #frame has been processed. Then we don't process this frame
        if (self.dbx.file_exists(dest_path, ticker + '_' + category_name + '_0_daily.csv')):
            return;
            
        self.pytrends.build_payload([ticker], cat=category_name, 
                       timeframe=frame, 
                       geo=self.config.geo, gprop='')
        data = self.pytrends.interest_over_time()
        df_aux = pd.DataFrame(data)
        df_aux.drop('isPartial', axis=1, inplace=True)
        df_aux.reset_index(level=0, inplace=True)
        
        # check if reach limit threshold for file size
        # if reach threshold, upload data to dropbox
        if (files_manager.check_chunks(self.config.output_size_mb, df,df_aux)):
                index = files_manager.save_data(self.config.data_folder, 
                                               ticker + '_' + category_name,
                                               '_daily.csv',
                                               self.config.dropbox_folder_upload + ticker + '/',df, 
                                               self.config.output_size_mb,index, dbx)
                df = df_aux
        else:
            df.append(df_aux)
        return (df, index)
   

    def process_data(self):
        #download tickers file from dropbox
        tickers_path = self.config.data_folder + 'tickers.csv'
        self.dbx.download_file(self.config.tickers_path, tickers_path)
        
        lines = open(tickers_path).readlines()[1:]
        
        year_range = range(int(self.config.year_from),int(self.config.year_until))
        
        #for each ticker download data from GTrends and upload to dropbox
        for ticker in lines:
            ticker = ticker.rstrip('\n')
            #create folder in dropbox for ticker if not exists
            ticker_folder = self.config.dropbox_folder_upload + ticker
            if (not self.dbx.folder_exists(ticker_folder)):
                self.dbx.create_folder(ticker_folder)
            #for each category in config, download and upload data
            for category in self.config.categories:
                category_type = category.split(':')
                category_name = category_type[0]
                category_type = category_type[1]
                #if the category type is montly -> download only 1 file for all the years
                if (category_type=='monthly'):
                    self.process_monthly(ticker, self.config.year_from + '-01-01 ' +
                                        self.config.year_until + '-12-31',
                                        category_name)
                        
                else:#if daily download 2 files framed January-June and July-December
                    df = pd.DataFrame()
                    index = 0
                    for year in year_range:
                        daily_time_frame_1 = str(year) + '-01-01 ' + str(year) + '-06-30'
                        (df,index) = self.process_daily(df, index, ticker, category_name, 
                                                  category_type, daily_time_frame_1)
          
                        daily_time_frame_2 = str(year) + '-07-01 ' + str(year) + '-12-31'
                        (df,index) = self.process_daily(df, index, ticker, category_name, 
                                                  category_type, daily_time_frame_2)
                        
                    #save last chunk if there is something left
                    if (df.shape[0]>0):
                        self.log.info('Saving last chunck')
                        files_manager.save_data(self.config.data_folder, 
                                                ticker + '_' + category_name, 
                                                 ticker_folder + '/',
                                                 '_daily.csv',
                                                 self.config.dropbox_folder_upload + ticker + '/'
                                                 df, self.config.output_size_mb, 
                                                 index, self.dbx)  
                       
                        
                       
def info():
    print('python gtrends.py -c config.properties')        

def main(argv):
    config_path = ''
    try:
        opts, args = getopt.getopt(argv,'hc:',['config='])
    except getopt.GetoptError:
        info()
        sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         info()
         sys.exit()
      elif opt in ('-c', '--config'):
         config_path = arg
    config = Config(config_path)
    gt = GTrends(config)
    gt.process_data()
   
if __name__ == "__main__":
    main(sys.argv[1:])


#config=Config('/Users/mikaelapisanileal/Desktop/config2.properties')
#from dropbox_handler import DropboxHandler
#dbx = DropboxHandler(config.access_token, config.dropbox_timeout, config.dropbox_chunck)



#TODO: change create folder per category NOT per ticker


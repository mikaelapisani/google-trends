#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 15:44:38 2019

@author: mikaelapisanileal
"""
from gtrends import GTrends
from config import Config
from process import Processor
from dropbox_handler import DropboxHandler

import sys
import getopt
import logging
from os import path

def info():
    print('Importing data: python main.py --config=config.properties --import=true')        
    print('Processing data: python main.py --config=config.properties --process=true')        

def main(argv):
    config_path = ''
    import_data = False
    process_data = False
    category = ''
    try:
        opts, args = getopt.getopt(argv,'hi:c:p:',['config=','import=', 'process='])
    except getopt.GetoptError:
        info()
        sys.exit(2)
    
    for opt, arg in opts:
      if opt == '-h':
         info()
         sys.exit()
      elif opt in ('-c', '--config'):
         config_path = arg
      elif opt in ('-i','--import'):
         import_data = bool(arg)
      elif opt in ('-p','--process'):
          process_data = bool(arg)

    
    try:
        config = Config(config_path)
        
        #set logging
        logging.basicConfig(format='%(levelname)s:%(asctime)s - %(pathname)s:%(lineno)d: %(message)s')
        log = logging.getLogger()
        log.setLevel(logging.getLevelName(config.log_level))
    except Exception as ex:
        print('There has been an error while initializing configuration.\n%s' %(ex))
        sys.exit(1)
    
    try:
        dbx = DropboxHandler(config.access_token, config.dropbox_timeout, config.dropbox_chunck)
        dbx.set_log(log)
    except Exception as ex:
        log.error('There has been an error while initializing dropbox handler.\n%s' %(ex))
        sys.exit(1)
    try:
        #import data from Google trends
        if (import_data):
            #download tickers file
            if (not path.exists(config.tickers_folder)):
                dbx.download_file(config.tickers_path, config.tickers_folder)
            
            #download gtrends data
            gt = GTrends(config.encoding, config.tz, config.gtrends_timeout_connect, 
                         config.gtrends_timeout_read, config.retries, config.backoff_factor, 
                         config.geo, dbx)
            gt.set_log(log)
            download_all = gt.import_data(config.tickers_folder, config.year_from, config.year_until,
                       config.categories, config.data_folder_monthly, config.data_folder_daily,
                       config.data_folder_monthly_dropbox, config.data_folder_daily_dropbox)
            print('download_all=%s' % str(download_all))
    except Exception as ex:
        log.error('There has been an error while importing data.\n%s' %(ex))
        sys.exit(1)
      
    try:    
        #process data and upload to dropbox    
        if(process_data):
            p = Processor(config.prefix, config.output_size_mb, dbx)
            p.set_log(log)
            for category in config.categories:
                category_type = category.split(':')
                category_name = category_type[0]
                category_type = category_type[1]
                if (category_type=='monthly'):
                    p.TL_data(config.data_folder_monthly_dropbox, config.dropbox_folder_upload_monthly, 
                              config.tmp_folder_monthly, config.result_folder_monthly, 'monthly.csv', category_name)
                else:
                    p.TL_data(config.data_folder_daily_dropbox, config.dropbox_folder_upload_daily, 
                              config.tmp_folder_daily, config.result_folder_daily, 'daily.csv', category_name)
            
    except Exception as ex:
        log.error('There has been an error while processing data.\n%s' %(ex))
        sys.exit(1)

    sys.exit(0)
   
if __name__ == "__main__":
    main(sys.argv[1:])
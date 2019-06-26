#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 12:01:20 2019

@author: mikaelapisanileal
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 08:40:31 2019

@author: mikaelapisanileal
"""

from properties.p import Property


class Config:
    def __init__(self, path):
        prop = Property()
        config = prop.load_property_files(path)
        self.log_level = config['log_level']
        self.access_token = config['access_token']
        self.output_size_mb=int(config['output_size_mb'])
        self.tickers_path=config['tickers_path']
        self.dropbox_folder_upload=config['dropbox_folder_upload']
        self.dropbox_chunck=int(config['dropbox_chunck'])
        self.dropbox_timeout=float(config['dropbox_timeout'])
        self.tickers_folder=config['tickers_folder']
        self.data_folder_monthly=config['data_folder_monthly']
        self.data_folder_daily=config['data_folder_daily']
        self.data_folder_monthly_dropbox=config['data_folder_monthly_dropbox']
        self.data_folder_daily_dropbox=config['data_folder_daily_dropbox']
        self.result_folder=config['result_folder']
        self.encoding=config['encoding']
        self.tz=int(config['tz'])
        self.categories=config['categories'].split(',')
        self.year_from=config['year_from']
        self.year_until=config['year_until']
        self.geo=config['geo']
        self.retries=int(config['retries'])
        self.backoff_factor=int(config['backoff_factor'])
        self.gtrends_timeout_connect=int(config['gtrends_timeout_connect'])
        self.gtrends_timeout_read=int(config['gtrends_timeout_read'])
        self.prefix=config['prefix']

        

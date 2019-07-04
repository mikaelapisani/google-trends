#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 14:45:32 2019

@author: mikaelapisanileal
"""

import pandas as pd
from files_manager import FilesManager
import os

class Processor:
    def __init__(self, prefix, output_size_mb, dbx):       
        #initialize dropbox connector
        self.dbx = dbx
        self.prefix = prefix
        self.files_manager = FilesManager(output_size_mb)
        
    def set_log(self, log):
        self.log = log
        self.files_manager.set_log(log)
        
    def TL_data(self, data_folder_dropbox, dropbox_folder_upload, data_folder, 
                result_folder, sufix, category):
        filenames = self.dbx.list_files(data_folder_dropbox + category)
        final_df = pd.DataFrame()
        index = 0
        dropbox_path = dropbox_folder_upload + category 
        if (not self.dbx.folder_exists(dropbox_path)):
            self.log.info('Create folder ' + dropbox_path)
            self.dbx.create_folder(dropbox_path)
            
        #for each file, append until reach threashold
        for filename in filenames:
            path = data_folder_dropbox + category + '/' + filename
            local_path = data_folder + filename
            self.dbx.download_file(path, local_path)
            df = pd.read_csv(local_path)
            if (df.shape[0]==0):
                continue
            
            ticker = df['ticker'][0]
            df['count'] = df[ticker]
            df.drop(ticker, axis=1,inplace=True)
            
            if (self.files_manager.check_chunks(final_df,df)):
                self.log.info('Uploading chunk:%d', index)
                #sort values by date before saving the file
                final_df.sort_values(by=['date'], inplace=True, ascending=False)
                index = self.files_manager.save_data(result_folder,
                                    self.prefix,
                                    sufix,
                                dropbox_folder_upload + category + '/',final_df, 
                                index, self.dbx)
                final_df = df
            else:
                final_df = final_df.append(df)
            os.remove(local_path)
        
        #save last chunck
        if (final_df.shape[0]>0):
            self.log.info('Saving last chunck')
            final_df.sort_values(by=['date'], inplace=True, ascending=False)
            self.files_manager.save_data(result_folder, 
                                    self.prefix,
                                     sufix,
                                     dropbox_folder_upload+ category + '/',
                                     final_df, index, self.dbx) 

        
   
        

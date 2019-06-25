#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 14:45:32 2019

@author: mikaelapisanileal
"""
import glob
import pandas as pd
from files_manager import FilesManager

class Processor:
    def __init__(self, prefix, output_size_mb, dbx):       
        #initialize dropbox connector
        self.dbx = dbx
        self.prefix = prefix
        self.files_manager = FilesManager(output_size_mb)
        
    def set_log(self, log):
        self.log = log
        self.files_manager.set_log(log)
        
    def TL_data(self, data_folder, dropbox_folder_upload, result_folder, sufix):
        filenames = glob.glob(data_folder + '*.csv')
        dfs = [pd.read_csv(filename) for filename in filenames]
        final_df = pd.DataFrame()
        index = 0
        #for each df, append until reach threashold
        for df in dfs:
            if (df.shape[0]==0):
                continue
            
            if (self.files_manager.check_chunks(final_df,df)):
                self.log.info('Uploading chunk:%d', index)
                #sort values by date before saving the file
                final_df.sort_values(by=['date'], inplace=True, ascending=False)
                index = self.files_manager.save_data(result_folder,
                                    self.prefix,
                                    sufix,
                                dropbox_folder_upload,final_df, 
                                index, self.dbx)
                final_df = df
            else:
                final_df = final_df.append(df)
        
        #save last chunck
        if (final_df.shape[0]>0):
            self.log.info('Saving last chunck')
            final_df.sort_values(by=['date'], inplace=True, ascending=False)
            self.files_manager.save_data(result_folder, 
                                    self.prefix,
                                     sufix,
                                     dropbox_folder_upload,
                                     final_df, index, self.dbx) 

        
   
        

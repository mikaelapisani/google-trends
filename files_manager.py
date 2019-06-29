#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 15:42:18 2019

@author: mikaelapisanileal
"""
import os
import numpy as np

import math

def upload_file(file_from, file_to, dbx):
    upload = False
    try:
       dbx.upload_file(file_from, file_to)
       upload = True
    except Exception as err:
        print('ERROR: Failed to upload %s to %s\n%s' %(file_from, file_to, err))
    if upload:
       os.remove(file_from)
           
class FilesManager():
    def __init__(self, output_size_mb):
        self.output_size_mb = output_size_mb
        
    def set_log(self, log):
        self.log = log

    #get amount of chunks based on output_size_gb
    def get_chunks(self, df):
        mem_usage_1 = (round(df.memory_usage(deep=True).sum() / 1024 ** 2, 2))
        return math.trunc(mem_usage_1/self.output_size_mb)
   
    #check if appending the two datasets the size is bigger than output_size_gb
    def check_chunks(self, df1, df2):
        mem_usage_1 = (round(df1.memory_usage(deep=True).sum() / 1024 ** 2, 2))
        mem_usage_2 = (round(df2.memory_usage(deep=True).sum() / 1024 ** 2, 2))
        chunks = math.trunc((mem_usage_1 + mem_usage_2)/self.output_size_mb)
        return (chunks > 0)

    
    #save dataframe into file and upload to dropbox
    #in case of error in upload, the local file would not be deleted
    def upload_file(self, local_folder, filename, dropbox_folder, df, dbx):
        file_from = local_folder + filename
        file_to = dropbox_folder + filename
        df.to_csv(file_from, index=False)
        upload_file(file_from, file_to, dbx)
       

    #devide data into chunks and upload to dropbox    
    def save_data(self, local_folder, prefix, sufix, dropbox_folder, df, idx, dbx):
        chunks = self.get_chunks(df)
        if (chunks==0):
            self.upload_file(local_folder, prefix + '_' + str(idx) + '_' + sufix,
                             dropbox_folder, df, dbx)
            idx=idx+1
        else:
            for df_chunk in np.array_split(df, chunks):
                self.upload_file(local_folder, prefix + '_' + str(idx) + '_' + sufix, 
                                 dropbox_folder, df_chunk, dbx)
                idx=idx+1
        return idx 


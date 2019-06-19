#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 15:42:18 2019

@author: mikaelapisanileal
"""
import os
import numpy as np

import math

#get amount of chunks based on output_size_gb
def get_chunks(output_size_mb, df):
    mem_usage_1 = (round(df.memory_usage(deep=True).sum() / 1024 ** 2, 2))
    return math.trunc(mem_usage_1/output_size_mb)
   
#check if appending the two datasets the size is bigger than output_size_gb
def check_chunks(output_size_mb, df1, df2):
    mem_usage_1 = (round(df1.memory_usage(deep=True).sum() / 1024 ** 2, 2))
    mem_usage_2 = (round(df2.memory_usage(deep=True).sum() / 1024 ** 2, 2))
    chunks = math.trunc((mem_usage_1 + mem_usage_2)/output_size_mb)
    return (chunks > 0)

#save dataframe into file and upload to dropbox
#in case of error in upload, the local file would not be deleted
def upload_file(local_folder, filename, dropbox_folder, df, dbx):
    file_from = local_folder + filename
    file_to = dropbox_folder + filename
    df.to_csv(file_from, index=False)
   
    upload = True
    try:
       dbx.upload_file(file_from, file_to)
    except Exception as err:
        print('ERROR: Failed to upload %s to %s\n%s' %(file_from, file_to, err))
        upload = False
    if upload:
       os.remove(file_from)

#devide data into chunks and upload to dropbox    
def save_data(local_folder, filename, sufix, dropbox_folder, df, output_size_mb, idx, dbx):
    chunks = get_chunks(output_size_mb, df)
    if (chunks==0):
        upload_file(local_folder, filename + '_' + str(idx) + sufix, dropbox_folder, df, dbx)
        idx=idx+1
    else:
        for chunk in np.array_split(df, chunks):
            upload_file(local_folder, filename + '_' + str(idx) + sufix, dropbox_folder, chunk, dbx)
            idx=idx+1
    return idx 

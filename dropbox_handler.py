#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 11:52:41 2019

@author: mikaelapisanileal
"""

import dropbox
import os

class DropboxHandler:
    def __init__(self, access_token, timeout, dropbox_chunck):
        self.access_token = access_token
        self.timeout = timeout
        self.CHUNK_SIZE = dropbox_chunck
        self.dbx = dropbox.Dropbox(self.access_token, timeout=self.timeout)

    def list_files(self, folder_path):
        files = []
        for entry in self.dbx.files_list_folder(folder_path).entries:
            files.append(entry.name)
        return files
         
    def download_file(self, filepath, localname):
        self.dbx.files_download_to_file(localname, filepath)    


    def upload_file(self, file_from, file_to):
        f = open(file_from, 'rb')
        file_size = os.path.getsize(file_from)
        upload_session_start_result = self.dbx.files_upload_session_start(f.read(self.CHUNK_SIZE))
        cursor = dropbox.files.UploadSessionCursor(session_id=upload_session_start_result.session_id,
                                           offset=f.tell())
        commit = dropbox.files.CommitInfo(path=file_to)
        
        while f.tell() <= file_size:
            if ((file_size - f.tell()) <= self.CHUNK_SIZE):
                self.dbx.files_upload_session_finish(f.read(self.CHUNK_SIZE),
                                                cursor,
                                                commit)
                break
            else:
                self.dbx.files_upload_session_append(f.read(self.CHUNK_SIZE),
                                                cursor.session_id,
                                                cursor.offset)
                cursor.offset = f.tell()
                
    def list_dirs(self, folder_path):
        folders = []
        for entry in self.dbx.files_list_folder(folder_path).entries:
            if isinstance(entry, dropbox.files.FolderMetadata):
                folders.append(entry.name)
        return folders
    
    def create_folder(self, folder_path):
        self.dbx.files_create_folder(folder_path)
    
    def list_recursive(self, folder_path):
        files = []
        for entry in self.dbx.files_list_folder(folder_path).entries:
            if isinstance(entry, dropbox.files.FolderMetadata):
                files = files + self.list_recursive(folder_path + '/' + entry.name)
            else:
                files.append((folder_path, entry.name))
        return files
    
    def folder_exists(self, path):
        try:
            self.dbx.files_get_metadata(path)
            return True
        except:
            return False
    
    def file_exists(self, folder_path, filename):
        result = self.dbx.files_search(folder_path, filename)
        return (len(result.matches)!=0)

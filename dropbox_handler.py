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
    
    def set_log(self, log):
        self.log = log
        
    def list_files(self, folder_path):
        try:
            files = []
            result = self.dbx.files_list_folder(folder_path)
            more = True
            while(more):
                more = result.has_more
                for entry in result.entries:
                    files.append(entry.name)
                result = self.dbx.files_list_folder_continue(result.cursor)
                
            return files
        except Exception as ex:
            self.log.error('Error while listing files for path%s.\n%s' %(folder_path, ex))
            raise ex
        
         
    def download_file(self, filepath, localname):
        try:
            self.dbx.files_download_to_file(localname, filepath)
        except Exception as ex:
            self.log.error('Error while downloading files from %s to %s.\n%s' %(filepath, localname, ex))
            raise ex


    def upload_file(self, file_from, file_to):
        try:
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
        except Exception as ex:
            self.log.error('Error while uploading file from %s to %s.\n%s' %(file_from, file_to, ex))
            raise ex

                
    def list_dirs(self, folder_path):
        try:
            folders = []
            for entry in self.dbx.files_list_folder(folder_path).entries:
                if isinstance(entry, dropbox.files.FolderMetadata):
                    folders.append(entry.name)
            return folders
        except Exception as ex:
            self.log.error('Error while listing dirs for path %s.\n%s' %(folder_path, ex))
            raise ex
    
    def create_folder(self, folder_path):
        try:
            self.dbx.files_create_folder(folder_path)
        except Exception as ex:
            self.log.error('Error while creating folder %s.\n%s' %(folder_path, ex))
            raise ex
    
    def list_recursive(self, folder_path):
        try:
            files = []
            for entry in self.dbx.files_list_folder(folder_path).entries:
                if isinstance(entry, dropbox.files.FolderMetadata):
                    files = files + self.list_recursive(folder_path + '/' + entry.name)
                else:
                    files.append((folder_path, entry.name))
            return files
        except Exception as ex:
            self.log.error('Error while listing recursive files in folder %s.\n%s' %(folder_path, ex))
            raise ex
    
    def folder_exists(self, path):
        try:
            self.dbx.files_get_metadata(path)
            return True
        except:
            return False
    
    def file_exists(self, folder_path, filename):
        try:
            result = self.dbx.files_search(folder_path, filename)
            return (len(result.matches)!=0)
        except Exception as ex:
            self.log.error('Error while checking if file %s exists in %s.\n%s' %(filename, folder_path, ex))
            raise ex
    
    def delete_file(self, filepath):
        try:
            self.dbx.files_delete(filepath)
        except Exception as ex:
            self.log.error('Error while deleting file %s.\n%s' %(filepath, ex))
            raise ex
  





#!/usr/bin/python
# vim: set fileencoding=UTF-8 :
"""
mindmapunzip

Just a helping script to unpack multiple .mmap (zip) files from certain subdirectories.
"""

import os, zipfile, re

folders = ["Viikko1","Viikko2","Viikko3","Viikko4","Viikko5","Viikko6final"]
extension = ".mmap"

print "week;user;item"
def handle(folder,item):
    os.chdir(folder)
    file_name = os.path.abspath(item) # get full path of files
    user = re.sub(r'^(\d+)_.*$',r'\1',item)
    if not os.path.exists(user):
        os.makedirs(user)
    zip_ref = zipfile.ZipFile(file_name) # create zipfile object
    zip_ref.extractall(user) # extract file to dir
    zip_ref.close() # close file
    print('"%s";"%s";"%s"'%(folder,user,item)) #,file_name
    os.chdir("..")

for folder in folders:
    for item in os.listdir(folder):
        if item.endswith(extension):
            handle(folder,item)


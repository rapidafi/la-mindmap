#!/usr/bin/python
# vim: set fileencoding=UTF-8 :
"""
mindmapunzip

Just a helping script to unpack multiple .mmap (zip) files from certain subdirectories.
"""

import os, sys, getopt
import zipfile, re

def getheader():
    print "week;user;item"

def handle(folder,item):
    os.chdir(folder)
    file_name = os.path.abspath(item) # get full path of files
    user = re.sub(r'^([^_]+)[_.].*$',r'\1',item)
    if not os.path.exists(user):
        os.makedirs(user)
    zip_ref = zipfile.ZipFile(file_name) # create zipfile object
    zip_ref.extractall(user) # extract file to dir
    zip_ref.close() # close file
    print('"%s";"%s";"%s"'%(folder,user,item)) #,file_name
    os.chdir("..")

def process(folders,extension):
    for folder in folders:
        for item in os.listdir(folder):
            if item.endswith(extension):
                handle(folder,item)

def usage():
    print """
    Usage:

    mindmapunzip -W|--weeks week1,week2,week3... [-e|--extension .ext] [-d|--debug]
    """

def main(argv):
    debug = False
    weeks = None
    extension = ".mmap"

    try:
        opts, args = getopt.getopt(argv,"W:w:e:d",["weeks=","extension=","debug"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-W", "-w", "--weeks"): weeks = arg.split(",")
        elif opt in ("-e", "--extension"): extension = arg
        elif opt in ("-d", "--debug"): debug = True
    if not weeks:
        print "You must give subdirectory names for looping. Exiting"
        usage()
        sys.exit(2)

    if debug: print "weeks",weeks
    print getheader()

    process(weeks,extension)

if __name__ == "__main__":
    main(sys.argv[1:])

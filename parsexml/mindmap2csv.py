#!/usr/bin/python
# vim: set fileencoding=UTF-8 :
"""
mindmap2csv

Output the results of certain subdirectory files, with the help of other
modules in this directory, to ready-named files.

NB! Does not actually provide CSV tool as results are already CSV-like.
"""
import os, sys, getopt
import re
#import ucsv as csv

import mindmapxmltopic, mindmapxmltree, mindmapxmlrelationship

# globally used filehandles
ftopic = None
ftree = None
frelship = None

def handle(folder,item):
    user = re.sub(r'^([^_]+)_.*$',r'\1',item)
    if not os.path.exists(folder+'\\'+user):
        print("USER DIRECTORY MISSING!",folder,user,item)
    #
    topiccsv = mindmapxmltopic.parse(folder,user)
    treecsv = mindmapxmltree.parse(folder,user)
    relshipcsv = mindmapxmlrelationship.parse(folder,user)
    ftopic.write(topiccsv)
    ftree.write(treecsv)
    frelship.write(relshipcsv)

def process(folders,extension):
    global ftopic, ftree, frelship

    ftopic = open('mindmaptopic.csv', 'w')
    ftree = open('mindmaptree.csv', 'w')
    frelship = open('mindmaprelationship.csv', 'w')

    ftopic.write(mindmapxmltopic.getheader())
    ftree.write(mindmapxmltree.getheader())
    frelship.write(mindmapxmlrelationship.getheader())

    for folder in folders:
        for item in os.listdir(folder):
            if item.endswith(extension):
                handle(folder,item)

    ftopic.close()
    ftree.close()
    frelship.close()

def usage():
    print """
    Usage:

    mindmap2csv -W|--weeks week1,week2,week3... [-e|--extension .ext] [-d|--debug]
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
    process(weeks,extension)

if __name__ == "__main__":
    main(sys.argv[1:])

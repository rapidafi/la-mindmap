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
fxptchlg = None
fhours = None
fimport = None

def csvq(items):
    ret = ""
    for row in items:
        i = 0
        for item in row:
            i = i + 1
            if i > 1: ret = ret + ";"
            if item is None:
                ret = ret
            elif isinstance(item,int):
                ret = ret + ("%s"%(item or ""))
            else:
                ret = ret + ("\"%s\""%((item or "").replace('"','""'))) #nb! for CSV replace "->""
        ret = ret + "\n"
    return ret

def handle(folder,item,debug):
    user = re.sub(r'^([^_]+)[_.].*$',r'\1',item)
    if not os.path.exists(folder+'/'+user):
        print("USER DIRECTORY MISSING!",folder,user,item)

    if debug: print("user",user)
    
    topiccsv = csvq(mindmapxmltopic.parse(folder,user))
    treecsv = csvq(mindmapxmltree.parse(folder,user))
    relshipcsv = csvq(mindmapxmlrelationship.parse(folder,user))
    if sys.version_info.major >= 3:
        ftopic.write(topiccsv)
        ftree.write(treecsv)
        frelship.write(relshipcsv)
    else:
        ftopic.write(topiccsv.encode('utf-8'))
        ftree.write(treecsv.encode('utf-8'))
        frelship.write(relshipcsv.encode('utf-8'))

def process(folders,extension,debug):
    global ftopic, ftree, frelship, fxptchlg, fhours, fimport

    if sys.version_info.major >= 3:
        ftopic = open('mindmaptopic.csv', 'w', encoding='utf-8')
        ftree = open('mindmaptree.csv', 'w', encoding='utf-8')
        frelship = open('mindmaprelationship.csv', 'w', encoding='utf-8')
    else:
        ftopic = open('mindmaptopic.csv', 'w')#, encoding='utf-8')
        ftree = open('mindmaptree.csv', 'w')
        frelship = open('mindmaprelationship.csv', 'w')

    ftopic.write(csvq(mindmapxmltopic.getheader()))
    ftree.write(csvq(mindmapxmltree.getheader()))
    frelship.write(csvq(mindmapxmlrelationship.getheader()))

    for folder in folders:
        for item in os.listdir(folder):
            if item.endswith(extension):
                handle(folder,item,debug)

    ftopic.close()
    ftree.close()
    frelship.close()

    # make tree csv unique by topic3oid
    # TODO this should be somewhere else!
    """
    ftree = open('mindmaptree.csv', 'r')
    uniq = set([])
    header = ""
    lnum = 0
    for line in ftree.readlines():
        lnum = lnum + 1
        incl = re.sub(r'^[^;]*;[^;]*;[^;]*;[^;]*;[^;]*;(.*)$', r'\1', line.rstrip("\n"))
        if lnum>1: # skip header line
            uniq.add(incl)
        else:
            header = incl
    ftree.close()
    ftree = open('mindmaptree.csv', 'w')
    ftree.write(header+"\n")
    for u in uniq:
        ftree.write(u+"\n")
    ftree.close()
    """

def usage():
    print("""
    Usage:

    mindmap2csv -W|--weeks week1,week2,week3... [-e|--extension .ext] [-d|--debug]
    """)

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
        print("You must give subdirectory names for looping. Exiting")
        usage()
        sys.exit(2)

    if debug: print("weeks",weeks)
    process(weeks,extension,debug)

if __name__ == "__main__":
    main(sys.argv[1:])

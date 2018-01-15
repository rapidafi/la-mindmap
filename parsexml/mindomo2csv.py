#!/usr/bin/python
# vim: set fileencoding=UTF-8 :
"""
mindomo2csv

Output the results of certain subdirectory files, with the help of other
modules in this directory, to ready-named files.

NB! Does not actually provide CSV tool as results are already CSV-like.
"""
import os, sys, getopt
import re
#import ucsv as csv

import mindomoxmlmap, mindomoxmltopic, mindomoxmlhierarchy, mindomoxmlrelation
import mindomoxmluser
#import mindomoxmlexpectchallenge, mindomoxmlhoursused, mindomoxmlimportance

# globally used filehandles
fmap = None
ftopic = None
fhierarchy = None
frelship = None
fuser = None
fxptchlg = None
fhours = None
fimport = None

def handle(folder,item,debug):
    user = re.sub(r'^([^_]+)[_.].*$',r'\1',item)
    if not os.path.exists(folder+'\\'+user):
        print("USER DIRECTORY MISSING!",folder,user,item)

    if debug: print("user",user)
    
    mapcsv = mindomoxmlmap.parse(folder,user)
    topiccsv = mindomoxmltopic.parse(folder,user)
    hierarchycsv = mindomoxmlhierarchy.parse(folder,user)
    relshipcsv = mindomoxmlrelation.parse(folder,user)
    usercsv = mindomoxmluser.parse(folder,user)
    #xptchlgcsv = mindomoxmlexpectchallenge.parse(folder,user)
    #hourscsv = mindomoxmlhoursused.parse(folder,user)
    #importcsv = mindomoxmlimportance.parse(folder,user)
    fmap.write(mapcsv)
    ftopic.write(topiccsv)
    fhierarchy.write(hierarchycsv)
    frelship.write(relshipcsv)
    fuser.write(usercsv)
    #fxptchlg.write(xptchlgcsv)
    #fhours.write(hourscsv)
    #fimport.write(importcsv)

def process(folders,extension,debug):
    global fmap, ftopic, fhierarchy, frelship, fuser, fxptchlg, fhours, fimport

    fmap = open('mindomomap.csv', 'w', encoding='utf-8')
    ftopic = open('mindomotopic.csv', 'w', encoding='utf-8')
    fhierarchy = open('mindomohierarchy.csv', 'w', encoding='utf-8')
    frelship = open('mindomorelation.csv', 'w', encoding='utf-8')
    fuser = open('mindomousers.csv', 'w', encoding='utf-8')
    #fxptchlg = open('mindomoexpectchallenge.csv', 'w', encoding='utf-8')
    #fhours = open('mindomohoursused.csv', 'w', encoding='utf-8')
    #fimport = open('mindomoimportance.csv', 'w', encoding='utf-8')

    fmap.write(mindomoxmlmap.getheader())
    ftopic.write(mindomoxmltopic.getheader())
    fhierarchy.write(mindomoxmlhierarchy.getheader())
    frelship.write(mindomoxmlrelation.getheader())
    fuser.write(mindomoxmluser.getheader())
    #fxptchlg.write(mindomoxmlexpectchallenge.getheader())
    #fhours.write(mindomoxmlhoursused.getheader())
    #fimport.write(mindomoxmlimportance.getheader())

    for folder in folders:
        for item in os.listdir(folder):
            if item.endswith(extension):
                handle(folder,item,debug)

    fmap.close()
    ftopic.close()
    fhierarchy.close()
    frelship.close()
    fuser.close()
    #fxptchlg.close()
    #fhours.close()
    #fimport.close()

    # make tree csv unique by topic3oid
    # TODO this should be somewhere else!
    """
    ftree = open('mindomotree.csv', 'r')
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
    ftree = open('mindomotree.csv', 'w')
    ftree.write(header+"\n")
    for u in uniq:
        ftree.write(u+"\n")
    ftree.close()
    """

def usage():
    print("""
    Usage:

    mindomo2csv -W|--weeks week1,week2,week3... [-e|--extension .ext] [-d|--debug]
    """)

def main(argv):
    debug = False
    weeks = None
    extension = ".mom"

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

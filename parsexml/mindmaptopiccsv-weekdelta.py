#!/usr/bin/python
# vim: set fileencoding=UTF-8 :
"""
mindmaptopiccsv-weekdelta

With a given CSV file find MindMap Topics per user+topic
and find differences in them on a weekly basis.
"""
import os, sys, getopt
import re
import csv

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

def process(file,debug):
    # read in CSV data, set up default value for delta (status)
    fweeks = open(file, 'r')
    csvr = csv.DictReader(fweeks, delimiter=';', quotechar='"')
    topics = []
    lnum = 0
    for t in csvr:
        lnum = lnum + 1
        n = t
        n["status"] = "NOT AVAILABLE" # default that will be tried to replace
        if t["topicEmotion"] == "EMOTION NOT SELECTED" or t["topicEmotion"] == "":
            if t["topicCompetence"] == "COMPETENCE NOT SELECTED" or t["topicCompetence"] == "":
                if t["topicDifficulty"] == "DIFFICULTY NOT SELECTED" or t["topicDifficulty"] == "":
                    if t["topicCalloutText"] == "":
                        n["status"] = "NOT STARTED"

        topics.append(n)
    fweeks.close()

    # loop data basically twice finding previous row for each row (user+week basis)
    updatedTopics = []
    # t = lookup (no change), n = new values, p = previous week data (for lookup, no change)
    for t in topics:
        #print(t)
        n = t # copy as unchanged
        previousfound = False
        # something has been done at some point
        if t["status"] != "NOT STARTED":
            weeknumber = int(t["week"].lstrip("week"))
            if weeknumber == 1:
                if n["status"] != "NOT STARTED":
                    n["status"] = "NEW THIS WEEK"
            else:
                # can look back to [p]revious week
                for p in topics:
                    if p["user"] == t["user"] and p["topicOid"] == t["topicOid"]:
                        if p["week"] == "week"+str((weeknumber-1)):
                            previousfound = True
                            #print("last week: "+ p["week"] +";"+ p["user"] +";"+ p["topicOid"] +";"+ p["topicEmotion"] +";"+ p["topicCompetence"] +";"+ p["topicDifficulty"] +";"+ p["status"])
                            if p["status"] == "NOT STARTED":
                                n["status"] = "NEW THIS WEEK"
                            else:
                                if p["topicEmotion"] == n["topicEmotion"] and p["topicCompetence"] == n["topicCompetence"] and p["topicDifficulty"] == n["topicDifficulty"] and p["topicCalloutText"] == n["topicCalloutText"]:
                                    n["status"] = "NO CHANGE THIS WEEK"
                                else:
                                    n["status"] = "CHANGED THIS WEEK"
                            break # no need to continue loop, or is there (todo)?
        # if unseen and still in default value
        if not previousfound and n["status"] == "NOT AVAILABLE":
            n["status"] = "NEW THIS WEEK"
        # copy new values (values only!)
        updatedTopics.append([n["week"],n["user"],n["documentCreated"],n["documentLastModified"],n["documentVersion"],
            n["topicOid"],n["topicLevel"],n["topicPlainText"],n["topicEmotion"],n["topicCompetence"],n["topicDifficulty"],n["topicCalloutText"],n["status"]])

    ftopic = None
    if sys.version_info.major >= 3:
        ftopic = open('mindmaptopicWITHSTATUS.csv', 'w', encoding='utf-8')
    else:
        ftopic = open('mindmaptopicWITHSTATUS.csv', 'w')#, encoding='utf-8')
    ftopic.write(csvq([["week","user","documentCreated","documentLastModified","documentVersion",
        "topicOid","topicLevel","topicPlainText","topicEmotion","topicCompetence","topicDifficulty","topicCalloutText","status"]]))
    ftopic.write(csvq(updatedTopics))
    ftopic.close()

def usage():
    print("""
    Usage:

    mindmaptopiccsv-weekdelta -f|--file file [-d|--debug]
    """)

def main(argv):
    debug = False
    file = None

    try:
        opts, args = getopt.getopt(argv,"f:d",["file=","debug"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-f", "--file"): file = arg
        elif opt in ("-d", "--debug"): debug = True
    if not file:
        print("You must give a file. Exiting")
        usage()
        sys.exit(2)

    if debug: print("file",file)
    process(file,debug)

if __name__ == "__main__":
    main(sys.argv[1:])

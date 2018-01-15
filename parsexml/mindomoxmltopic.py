#!/usr/bin/python
# vim: set fileencoding=UTF-8 :
"""
mindomoxmltopic

Go thru given XML-file and parse and find certain information from it.
Return or output result as CSV-like data.
"""

import sys, os, getopt
import mindomoxml as mm

def getheader():
    ret = "id;text;taskCompletition;symbol;topicLevel;mapid;userid"
    ret = ret + "\n"
    return ret

def v(value):
    return "%s"%(value or "")

def t(text):
    return "%s"%("\"%s\""%(text) if text else "")

# for module usage pass arguments
def parse(week,user):
    root = mm.getroot(week,user)

    (mapid,name,authorId,creationDate,modificationDate) = mm.getdocinfo(root)
    ret = ""
    # "root" topics (level=0) first
    for topics in root.findall('.//mo:topics',mm.ns):
        for topic in topics.findall('./mo:topic',mm.ns):
            (topicid,topictext) = mm.gettopic(topic)
            taskCompletition = mm.gettaskcompletion(topic)
            symbol = mm.gettopicsymbol(topic)
            topicLevel = 0
            userid = None #TODO
            ret = ret + ("%s;%s;%s;%s;%s;%s;%s\n"%
                  (t(topicid),t(topictext),v(taskCompletition),t(symbol),v(topicLevel),t(mapid),t(userid))
                  )
            # below "root" topics are subtopics
            elements = mm.subtopic(topic,0,[])
            for e in elements:
                (topicid,topictext,taskCompletition,symbol,topicLevel,parents) = e
                userid=None #TODO
                ret = ret + ("%s;%s;%s;%s;%s;%s;%s\n"%
                      (t(topicid),t(topictext),v(taskCompletition),t(symbol),v(topicLevel),t(mapid),t(userid))
                      )
    return ret

def main(argv):
    week = None
    user = None
    debug = False

    try:
        opts, args = getopt.getopt(argv,"w:u:d",["week=","user=","debug"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-w", "--week"): week = arg
        elif opt in ("-u", "--user"): user = arg
        elif opt in ("-d", "--debug"): debug = True
    if not week or not user:
        print("Mandatory arguments missing. Exiting.")
        sys.exit(2)

    print(getheader()+parse(week,user))

if __name__ == "__main__":
    main(sys.argv[1:])

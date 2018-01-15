#!/usr/bin/python
# vim: set fileencoding=UTF-8 :
"""
mindomoxmlhierarchy

Go thru given XML-file and parse and find certain information from it.
Return or output result as CSV-like data.
"""

import sys, os, getopt
import mindomoxml as mm

def getheader():
    ret = "level1id;level1text;level2id;level2text;level3id;level3text;level4id;level4text"
    ret = ret + "\n"
    return (ret)

def t(text):
    return "%s"%(text or "")

# for module usage pass arguments
def parse(week,user):
    root = mm.getroot(week,user)

    ret = ""
    # "root" topics (level=0) first
    for topics in root.findall('.//mo:topics',mm.ns):
        for topic in topics.findall('./mo:topic',mm.ns):
            #(topic0id,topic0text) = mm.gettopic(topic)
            # below "root" topics are subtopics
            elements = mm.subtopic(topic,0,[])
            for e in elements:
                (topic3id,topic3text,taskCompletition,symbol,topiclevel,parents) = e
                # possibly rethink this next structure:
                # this is due to changing from topiclevel==3 only to include all levels also
                if topiclevel>=3:
                    (topic0id,topic0text) = parents[2]
                    (topic1id,topic1text) = parents[1]
                    (topic2id,topic2text) = parents[0]
                elif topiclevel==2:
                    (topic0id,topic0text) = parents[1]
                    (topic1id,topic1text) = parents[0]
                    (topic2id,topic2text) = (topic3id,topic3text)
                    (topic3id,topic3text) = (None,None)
                elif topiclevel==1:
                    (topic0id,topic0text) = parents[0]
                    (topic1id,topic1text) = (topic3id,topic3text)
                    (topic2id,topic2text) = (None,None)
                    (topic3id,topic3text) = (None,None)

                ret = ret + ("\"%s\";\"%s\";\"%s\";\"%s\";\"%s\";\"%s\";\"%s\";\"%s\"\n"%
                          (t(topic0id),t(topic0text),t(topic1id),t(topic1text),t(topic2id),t(topic2text),t(topic3id),t(topic3text))
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

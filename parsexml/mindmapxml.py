#!/usr/bin/python
# vim: set fileencoding=UTF-8 :
"""
mindmapxml

Parse given XML-file and give access to certain information in it.
"""

import sys, os, getopt
import xml.etree.ElementTree as ET

# "globals"
ns = {'ap': 'http://schemas.mindjet.com/MindManager/Application/2003'}

def getroot(week,user):
    tree = ET.parse('./'+week+'/'+user+'/Document.xml')
    return tree.getroot()

def gettopic(topic):
    topicoid = topic.attrib["OId"]
    topicplaintext = None
    for topictext in topic.findall('./ap:Text',ns):
        if "PlainText" in topictext.attrib:
            topicplaintext = topictext.attrib["PlainText"]
    return (topicoid,topicplaintext)

"""
Choose icon by type parameter

Hard coded keys to icons (below in code) for types: Emotion, Competence and Difficulty
"""
def gettopicicon(topic,type):
    topicicontype = None
    # NB! This probably could be generated from data as well!
    typeoptions = None
    if type == "Emotion":
        typeoptions = {
            "6Up4AwAAAAAAAAAAAAAAAA==" : "Excited",
            "LrKgqwAAAAAAAAAAAAAAAA==" : "Relaxed",
            "W0bzbgAAAAAAAAAAAAAAAA==" : "Neutral",
            "uD9XcgAAAAAAAAAAAAAAAA==" : "Bored",
            "sWwXLwAAAAAAAAAAAAAAAA==" : "Anxious",
            "H8m8PQAAAAAAAAAAAAAAAA==" : "EMOTION NOT SELECTED"
        }
    if type == "Competence":
        typeoptions = {
            "6Xuk0QAAAAAAAAAAAAAAAA==" : "1 Low",
            "h3McqAAAAAAAAAAAAAAAAA==" : "2 Medium low",
            "/0FSQQAAAAAAAAAAAAAAAA==" : "3 Medium",
            "hFp+eQAAAAAAAAAAAAAAAA==" : "4 Medium high",
            "bMuCqAAAAAAAAAAAAAAAAA==" : "5 High",
            "JQCptwAAAAAAAAAAAAAAAA==" : "COMPETENCE NOT SELECTED"
        }
    if type == "Difficulty":
        typeoptions = {
            "hKU7wQAAAAAAAAAAAAAAAA==" : "1 Easy",
            "BbriQgAAAAAAAAAAAAAAAA==" : "2 Easier than average",
            "q6llvAAAAAAAAAAAAAAAAA==" : "3 Average",
            "0O4tDwAAAAAAAAAAAAAAAA==" : "4 Harder than average",
            "i8x9wgAAAAAAAAAAAAAAAA==" : "5 Hard",
            "exNH7QAAAAAAAAAAAAAAAA==" : "DIFFICULTY NOT SELECTED"
        }

    for topicicon in topic.findall('./ap:IconsGroup/ap:Icons/ap:Icon',ns):
        if "IconSignature" in topicicon.attrib:
            if topicicon.attrib["IconSignature"] in typeoptions:
                topicicontype = typeoptions.get(topicicon.attrib["IconSignature"],"ICON ERROR!")
    return (topicicontype)

def gettopiccallouttext(topic):
    topiccallouttext = None
    for topictext in topic.findall('./ap:FloatingTopics/ap:Topic/ap:Text',ns):
        # if there is already some text (meaning multiple callout texts) catenate w/ newline
        if topiccallouttext: topiccallouttext = topiccallouttext + "\n"
        if "PlainText" in topictext.attrib:
            topiccallouttext = topictext.attrib["PlainText"]
    return (topiccallouttext)

def getparents(parents):
    # collect all the parents to same line, reversed!
    ret = []
    for p in reversed(parents):
        ret.append(gettopic(p))
    return ret

def subtopic(parenttopic,topiclevel,parents):
    topiclevel = topiclevel + 1
    parents.append(parenttopic)
    ret = []
    for topic in parenttopic.findall('./ap:SubTopics/ap:Topic',ns):
        if 1==1: #topiclevel == 3:
            (topicoid,topicplaintext) = gettopic(topic)
            ret.append((topicoid,topicplaintext,topiclevel,gettopicicon(topic,"Emotion"),gettopicicon(topic,"Competence"),gettopicicon(topic,"Difficulty"),gettopiccallouttext(topic),getparents(parents)))
        # recursively loop subtopics and defuse list in list
        for e in subtopic(topic,topiclevel,list(parents)):
            ret.append(e)
    return ret

def getdocinfo(root):
    documentcreated = None
    documentlastmodified = None
    documentversion = None
    for docgroup in root.findall('.//ap:DocumentGroup',ns):
        documentcreated = docgroup.find('.//ap:DateTimeStamps',ns).attrib["Created"]
        documentlastmodified = docgroup.find('.//ap:DateTimeStamps',ns).attrib["LastModified"]
        documentversion = docgroup.find('.//ap:Version',ns).attrib["Major"]
    return (documentcreated, documentlastmodified, documentversion)

# only module usage
def main(argv):
    print("Used as a module only. Exiting.")
    sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])

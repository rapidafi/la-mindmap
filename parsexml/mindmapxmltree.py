#!/usr/bin/python
# vim: set fileencoding=UTF-8 :
"""
mindmapxmltree

Go thru given XML-file and parse and find certain information from it.
Return or output result as CSV-like data.
"""

import sys, os, getopt
import xml.etree.ElementTree as ET

# "globals"
ns = {'ap': 'http://schemas.mindjet.com/MindManager/Application/2003'}

def getheader():
    ret = "week;user;documentCreated;documentLastModified;documentVersion"
    ret = ret + ";topic3Oid;topic3PlainText;topic2Oid;topic2PlainText;topic1Oid;topic1PlainText;topic0Oid;topic0PlainText"
    ret = ret + "\n"
    return (ret).encode('utf-8')

def gettopic(topic):
    topicoid = topic.attrib["OId"]
    topicplaintext = None

    for topictext in topic.findall('./ap:Text',ns):
        topicplaintext = topictext.attrib["PlainText"]
    
    return (";\"%s\";\"%s\""%(topicoid,topicplaintext))

def getparents(parents):
    # collect all the parents to same line, reversed!
    ret = ""
    for p in reversed(parents):
        ret = ret + gettopic(p)
    return ret
    
def subtopic(firstcolumns,parenttopic,topiclevel,parents):
    topiclevel = topiclevel + 1
    parents.append(parenttopic)
    ret = ""
    for topic in parenttopic.findall('./ap:SubTopics/ap:Topic',ns):
        if topiclevel == 3:
            ret = ret + firstcolumns
            ret = ret + gettopic(topic)
            ret = ret + getparents(parents)
            ret = ret + "\n"

        ret = ret + subtopic(firstcolumns,topic,topiclevel,list(parents))
    return ret

# for module usage pass arguments
def parse(pweek,puser):
    week = pweek
    user = puser

    tree = ET.parse('.\\'+week+'\\'+user+'\\Document.xml')
    root = tree.getroot()

    for docgroup in root.findall('.//ap:DocumentGroup',ns):
        documentcreated = docgroup.find('.//ap:DateTimeStamps',ns).attrib["Created"]
        documentlastmodified = docgroup.find('.//ap:DateTimeStamps',ns).attrib["LastModified"]
        documentversion = docgroup.find('.//ap:Version',ns).attrib["Major"]
    firstcolumns = ("%s;%s;%s;%s;%s"%(week,user,documentcreated,documentlastmodified,documentversion))
    ret = ""
    for onetopic in root.findall('.//ap:OneTopic',ns):
        for topic in onetopic.findall('./ap:Topic',ns):
            ret = ret + subtopic(firstcolumns,topic,0,[])
            # floating topics also (MSc for BSc)
            for floatingtopics in topic.findall('./ap:FloatingTopics',ns):
                for fttopic in floatingtopics.findall('./ap:Topic',ns):
                    ret = ret + subtopic(firstcolumns,fttopic,0,[])
    return ret.encode('utf-8')

def main(argv):
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
        sys.exit(2)

    print getheader()+parse(week,user)

if __name__ == "__main__":
    main(sys.argv[1:])

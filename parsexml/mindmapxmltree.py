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

week = None
user = None

documentcreated = None
documentlastmodified = None
documentversion = None

def getheader():
    return ("week;user;documentCreated;documentLastModified;documentVersion;topic3Oid;topic3PlainText;topic2Oid;topic2PlainText;topic1Oid;topic1PlainText;topic0Oid;topic0PlainText\n").encode('utf-8')

def gettopic(topic,parents):
    global week,user,documentcreated,documentlastmodified,documentversion

    topicoid = topic.attrib["OId"]
    topicplaintext = None

    for topictext in topic.findall('./ap:Text',ns):
        topicplaintext = topictext.attrib["PlainText"]
    
    # collect all the parents to same line diff columns, reversed!
    pstr = ""
    for p in reversed(parents):
        pstr = pstr+";\""+p.attrib["OId"]+"\""
        for topictext in p.findall('./ap:Text',ns):
            pstr = pstr+";\""+topictext.attrib["PlainText"]+"\""

    return ("%s;%s;%s;%s;%s;\"%s\";\"%s\"%s\n"%
          (week,user,documentcreated,documentlastmodified,documentversion,
           topicoid,topicplaintext,pstr)
          ).encode('utf-8')
    
def subtopic(parenttopic,topiclevel,parents):
    global week,user,documentcreated,documentlastmodified,documentversion

    topiclevel = topiclevel + 1
    parents.append(parenttopic)
    ret = ""
    for topic in parenttopic.findall('./ap:SubTopics/ap:Topic',ns):
        if topiclevel == 3:
            ret = ret + gettopic(topic,parents)
        ret = ret + subtopic(topic,topiclevel,list(parents))
    return ret

# for module usage pass arguments
def parse(pweek,puser):
    global week,user,documentcreated,documentlastmodified,documentversion
    week = pweek
    user = puser

    tree = ET.parse('.\\'+week+'\\'+user+'\\Document.xml')
    root = tree.getroot()

    ret = ""
    for docgroup in root.findall('.//ap:DocumentGroup',ns):
        documentcreated = docgroup.find('.//ap:DateTimeStamps',ns).attrib["Created"]
        documentlastmodified = docgroup.find('.//ap:DateTimeStamps',ns).attrib["LastModified"]
        documentversion = docgroup.find('.//ap:Version',ns).attrib["Major"]
    for onetopic in root.findall('.//ap:OneTopic',ns):
        for topic in onetopic.findall('./ap:Topic',ns):
            ret = ret + subtopic(topic,0,[])
    return ret


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

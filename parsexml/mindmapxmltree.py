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
    return (topicoid,topicplaintext)

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
        if topiclevel == 3:
            (topicoid,topicplaintext) = gettopic(topic)
            ret.append((topicoid,topicplaintext,topiclevel,getparents(parents)))
        # recursively loop subtopics and defuse list in list
        for e in subtopic(topic,topiclevel,list(parents)):
            ret.append(e)
    return ret

# for module usage pass arguments
def parse(week,user):
    tree = ET.parse('.\\'+week+'\\'+user+'\\Document.xml')
    root = tree.getroot()

    for docgroup in root.findall('.//ap:DocumentGroup',ns):
        documentcreated = docgroup.find('.//ap:DateTimeStamps',ns).attrib["Created"]
        documentlastmodified = docgroup.find('.//ap:DateTimeStamps',ns).attrib["LastModified"]
        documentversion = docgroup.find('.//ap:Version',ns).attrib["Major"]
    ret = ""
    for onetopic in root.findall('.//ap:OneTopic',ns):
        for topic in onetopic.findall('./ap:Topic',ns):
            elements = subtopic(topic,0,[])
            # floating topics also (MSc for BSc)
            for floatingtopics in topic.findall('./ap:FloatingTopics',ns):
                for fttopic in floatingtopics.findall('./ap:Topic',ns):
                    elements = elements + subtopic(fttopic,0,[])

            for e in elements:
                (topic3oid,topic3plaintext,topiclevel,parents) = e
                (topic2oid,topic2plaintext) = parents[0]
                (topic1oid,topic1plaintext) = parents[1]
                (topic0oid,topic0plaintext) = parents[2]
                ret = ret + ("%s;%s;%s;%s;%s;\"%s\";\"%s\";\"%s\";\"%s\";\"%s\";\"%s\";\"%s\";\"%s\"\n"%
                          (week,user,documentcreated,documentlastmodified,documentversion,
                           topic3oid,topic3plaintext,topic2oid,topic2plaintext,topic1oid,topic1plaintext,topic0oid,topic0plaintext)
                          )
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
        print "Mandatory arguments missing. Exiting."
        sys.exit(2)

    print getheader()+parse(week,user)

if __name__ == "__main__":
    main(sys.argv[1:])

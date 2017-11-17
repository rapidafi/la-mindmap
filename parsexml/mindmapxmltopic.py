#!/usr/bin/python
# vim: set fileencoding=UTF-8 :
"""
mindmapxmltopic

Go thru given XML-file and parse and find certain information from it.
Return or output result as CSV-like data.
"""

import sys, os, getopt
import xml.etree.ElementTree as ET

# "globals"
ns = {'ap': 'http://schemas.mindjet.com/MindManager/Application/2003'}

def getheader():
    ret = "week;user;documentCreated;documentLastModified;documentVersion"
    ret = ret + ";topicOid;topicLevel;topicPlainText;topicTaskPercentage;topicIconType"
    ret = ret + "\n"
    return ret.encode('utf-8')

def gettopic(topic):
    topicoid = topic.attrib["OId"]
    topicplaintext = None
    for topictext in topic.findall('./ap:Text',ns):
        topicplaintext = topictext.attrib["PlainText"]
    return (topicoid,topicplaintext)

def gettopicpercentage(topic):
    topictaskpercentage = None
    for topictask in topic.findall('./ap:Task',ns):
        topictaskpercentage = topictask.attrib["TaskPercentage"]
    return (topictaskpercentage)

def gettopicicon(topic):
    topicicontype = None
    for topicicon in topic.findall('./ap:IconsGroup/ap:Icons/ap:Icon',ns):
        topicicontype = topicicon.attrib["IconType"]
    return (topicicontype)
    
def subtopic(parenttopic,topiclevel):
    topiclevel = topiclevel + 1
    ret = []
    for topic in parenttopic.findall('./ap:SubTopics/ap:Topic',ns):
        if topiclevel == 3:
            (topicoid,topicplaintext) = gettopic(topic)
            ret.append((topicoid,topicplaintext,topiclevel,gettopicpercentage(topic),gettopicicon(topic)))
        # recursively loop subtopics and defuse list in list
        for e in subtopic(topic,topiclevel):
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
            elements = subtopic(topic,0)
            for e in elements:
                (topicoid,topicplaintext,topiclevel,topicpercentage,topicicon) = e
                ret = ret + ("%s;%s;%s;%s;%s;\"%s\";%s;\"%s\";%s;%s\n"%
                      (week,user,documentcreated,documentlastmodified,documentversion,
                       topicoid,topiclevel,topicplaintext,topicpercentage,topicicon)
                      )
    return ret.encode('utf-8')


def main(argv):
    debug = False
    week = None
    user = None

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

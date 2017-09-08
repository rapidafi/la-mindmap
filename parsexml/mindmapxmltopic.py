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

week = None
user = None

documentcreated = None
documentlastmodified = None
documentversion = None

def getheader():
    return ("week;user;documentCreated;documentLastModified;documentVersion;topicOid;topicLevel;topicPlainText;topicTaskPercentage;topicIconType\n").encode('utf-8')

def gettopic(topic,topiclevel):
    topicoid = topic.attrib["OId"]
    topicplaintext = None
    topictaskpercentage = "0"
    topicicontype = "SmileyNeutral"

    for topictext in topic.findall('./ap:Text',ns):
        topicplaintext = topictext.attrib["PlainText"]
    for icon in topic.findall('./ap:IconsGroup/ap:Icons/ap:Icon',ns):
        topicicontype = icon.attrib["IconType"]
        topicicontype = topicicontype.replace("urn:mindjet:","")
    for task in topic.findall('./ap:Task',ns):
        topictaskpercentage = task.attrib["TaskPercentage"]
        
    return ("%s,%s;%s;%s;%s;\"%s\";%s;\"%s\";%s;%s\n"%
          (week,user,documentcreated,documentlastmodified,documentversion,
           topicoid,topiclevel,topicplaintext,topictaskpercentage,topicicontype)
          ).encode('utf-8')
    
def subtopic(parenttopic,topiclevel):
    global week,user,documentcreated,documentlastmodified,documentversion

    topiclevel = topiclevel + 1
    ret = ""
    for topic in parenttopic.findall('./ap:SubTopics/ap:Topic',ns):
        if topiclevel == 3:
            ret = ret + gettopic(topic,topiclevel)
        ret = ret + subtopic(topic,topiclevel)
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
            ret = ret + subtopic(topic,0)

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

#!/usr/bin/python
# vim: set fileencoding=UTF-8 :
"""
mindmapxmlhoursused

Go thru given XML-file and parse and find certain information from it.
Return or output result as CSV-like data.
"""

import sys, os, getopt
import xml.etree.ElementTree as ET

# "globals"
ns = {'ap': 'http://schemas.mindjet.com/MindManager/Application/2003'}

def getheader():
    ret = "week;user;documentCreated;documentLastModified;documentVersion"
    ret = ret + ";topicOid;topicPlainText;topicIconType;Priority;Percentage"
    ret = ret + "\n"
    return (ret).encode('utf-8')

def gettopic(topic):
    topicoid = topic.attrib["OId"]
    topicplaintext = None
    for topictext in topic.findall('./ap:Text',ns):
        topicplaintext = topictext.attrib["PlainText"]
    return (topicoid,topicplaintext)

def gettopicicon(topic):
    topicicontype = None
    for topicicon in topic.findall('./ap:IconsGroup/ap:Icons/ap:Icon',ns):
        topicicontype = topicicon.attrib["IconType"]
    return (topicicontype)

def getpriority(topic):
    taskpriority = None
    taskpercentage = None
    for task in topic.findall('./ap:Task',ns):
        if "TaskPriority" in task.attrib:
            taskpriority = task.attrib["TaskPriority"]
        if "TaskPercentage" in task.attrib:
            taskpercentage = task.attrib["TaskPercentage"]
    return (taskpriority,taskpercentage)

def getprioritymarker(root,priority):
    taskprioritymarkername = None
    for taskprioritymarker in root.findall('.//ap:TaskPriorityMarker',ns):
        for taskpriority in taskprioritymarker.findall('./ap:TaskPriority',ns):
            if "TaskPriority" in taskpriority.attrib:
                if priority == taskpriority.attrib["TaskPriority"]:
                    taskprioritymarkername = taskprioritymarker.find('./ap:Name',ns).attrib["Name"]
    return (taskprioritymarkername)

# for module usage pass arguments
def parse(week,user):
    tree = ET.parse('.\\'+week+'\\'+user+'\\Document.xml')
    root = tree.getroot()

    for docgroup in root.findall('.//ap:DocumentGroup',ns):
        documentcreated = docgroup.find('.//ap:DateTimeStamps',ns).attrib["Created"]
        documentlastmodified = docgroup.find('.//ap:DateTimeStamps',ns).attrib["LastModified"]
        documentversion = docgroup.find('.//ap:Version',ns).attrib["Major"]
    ret = ""
    for topic in root.findall('.//ap:Topic',ns):
        (priority,percentage) = getpriority(topic)
        if priority:
            (topicoid,topicplaintext) = gettopic(topic)
            ret = ret + ("%s;%s;%s;%s;%s;\"%s\";\"%s\";\"%s\";\"%s\";%s\n"%
                (week,user,documentcreated,documentlastmodified,documentversion,
                 topicoid,topicplaintext,gettopicicon(topic),getprioritymarker(root,priority),percentage))

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

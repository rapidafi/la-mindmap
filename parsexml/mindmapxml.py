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
    tree = ET.parse('.\\'+week+'\\'+user+'\\Document.xml')
    return tree.getroot()

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
            ret.append((topicoid,topicplaintext,topiclevel,gettopicpercentage(topic),gettopicicon(topic),getparents(parents)))
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
    print "Used as a module only. Exiting."
    sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])

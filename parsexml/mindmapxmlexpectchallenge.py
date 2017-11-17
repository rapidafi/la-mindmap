#!/usr/bin/python
# vim: set fileencoding=UTF-8 :
"""
mindmapxmlexpectchallenge

Go thru given XML-file and parse and find certain information from it.
Return or output result as CSV-like data.
"""

import sys, os, getopt
import xml.etree.ElementTree as ET

# "globals"
ns = {'ap': 'http://schemas.mindjet.com/MindManager/Application/2003'}

def getheader():
    ret = "week;user;documentCreated;documentLastModified;documentVersion"
    ret = ret + ";topicOid;topicPlainText;topicPercentage;topic1Oid;topic1PlainText;topic1Percentage;topic1Icon;topic0Oid;topic0PlainText"
    ret = ret + "\n"
    return (ret).encode('utf-8')

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
    for topic in root.findall('.//ap:OneTopic/ap:Topic',ns):
        (toid,ttext) = gettopic(topic)
        (tpercentage) = gettopicpercentage(topic)
        (ticon) = gettopicicon(topic)
        for fttopic in topic.findall('./ap:FloatingTopics/ap:Topic',ns):
            # path to Expectations and ...challenges
            for atopic in fttopic.findall('./ap:SubTopics/ap:Topic',ns):
                (aoid,atext) = gettopic(atopic)
                (apercentage) = gettopicpercentage(atopic)
                (aicon) = gettopicicon(atopic)
                # one way (opiskelija1)
                for btopic in atopic.findall('./ap:FloatingTopics/ap:Topic',ns):
                    (boid,btext) = gettopic(btopic)
                    (bpercentage) = gettopicpercentage(btopic)
                    (bicon) = gettopicicon(btopic)
                    ret = ret + firstcolumns
                    ret = ret + ";\"%s\";\"%s\""%(boid,btext)
                    ret = ret + ";\"%s\""%(bpercentage) # task percentage
                    ret = ret + ";\"%s\";\"%s\""%(aoid,atext)
                    ret = ret + ";\"%s\""%(apercentage) # parent percentage
                    ret = ret + ";\"%s\""%(aicon)
                    ret = ret + ";\"%s\";\"%s\""%(toid,ttext)
                    ret = ret + "\n"
                # alternative way with enormous hierarchy and false location of written text (opiskelija2)
                for btopic in atopic.findall('./ap:SubTopics/ap:Topic',ns):
                    (boid,btext) = gettopic(btopic)
                    (bpercentage) = gettopicpercentage(btopic)
                    (bicon) = gettopicicon(btopic)
                    #TODO: fixme: b and c are actually parent topics which replace fttopic and atopic above in this scenario (only c is interesting, though)
                    for ctopic in btopic.findall('./ap:SubTopics/ap:Topic',ns):
                        (coid,ctext) = gettopic(ctopic)
                        (cpercentage) = gettopicpercentage(ctopic)
                        (cicon) = gettopicicon(ctopic)
                        for dtopic in ctopic.findall('./ap:FloatingTopics/ap:Topic',ns):
                            (doid,dtext) = gettopic(dtopic)
                            (dpercentage) = gettopicpercentage(dtopic)
                            (dicon) = gettopicicon(dtopic)
                            #TODO: do we want to gather the false way written texts?
                            # if not, choose this:
                            """
                            ret = ret + firstcolumns
                            ret = ret + ";\"%s\";\"%s\""%(doid,dtext)
                            ret = ret + ";%s"%(dpercentage) # task percentage
                            ret = ret + ";\"%s\";\"%s\""%(coid,ctext)
                            ret = ret + ";%s"%(cpercentage) # parent percentage
                            ret = ret + ";\"%s\""%(cicon)
                            ret = ret + ";\"%s\";\"%s\""%(toid,ttext)
                            ret = ret + "\n"
                            #"""
                            # if we do want to support the wrong way, choose this:
                            #"""
                            # append by gathering texts from subtopics of dtopic
                            for etopic in dtopic.findall('./ap:SubTopics/ap:Topic',ns):
                                for topictext in etopic.findall('./ap:Text',ns):
                                    dtext = dtext + topictext.attrib["PlainText"] + ", "
                            ret = ret + firstcolumns
                            ret = ret + ";\"%s\";\"%s\""%(doid,dtext)
                            ret = ret + ";%s"%(dpercentage) # task percentage
                            ret = ret + ";\"%s\";\"%s\""%(coid,ctext)
                            ret = ret + ";%s"%(cpercentage) # parent percentage
                            ret = ret + ";\"%s\""%(cicon)
                            ret = ret + ";\"%s\";\"%s\""%(toid,ttext)
                            ret = ret + "\n"
                            #"""

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

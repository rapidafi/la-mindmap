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
    ret = ret + ";topicOid;topicPlainText;topic1Oid;topic1PlainText;topic0Oid;topic0PlainText"
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
        for fttopic in topic.findall('./ap:FloatingTopics/ap:Topic',ns):
            # path to Expectations and ...challenges
            for atopic in fttopic.findall('./ap:SubTopics/ap:Topic',ns):
                # one way (opiskelija1)
                for btopic in atopic.findall('./ap:FloatingTopics/ap:Topic',ns):
                    ret = ret + firstcolumns
                    ret = ret + gettopic(btopic)
                    #ret = ret + getparents(list([topic,fttopic,atopic]))
                    ret = ret + getparents(list([topic,atopic]))
                    #ret = ret + gettopic(topic)
                    ret = ret + "\n"
                # alternative way with enormous hierarchy and false location of written text (opiskelija2)
                for btopic in atopic.findall('./ap:SubTopics/ap:Topic',ns):
                    # gather b, c and d topic texts as one but presumably b and c are actually parent topics which should replace fttopic and atopic above
                    #btext = "None"
                    #for topictext in btopic.findall('./ap:Text',ns):
                    #    btext = topictext.attrib["PlainText"]
                    for ctopic in btopic.findall('./ap:SubTopics/ap:Topic',ns):
                        #ctext = "None"
                        #for topictext in ctopic.findall('./ap:Text',ns):
                        #    ctext = topictext.attrib["PlainText"]
                        for dtopic in ctopic.findall('./ap:FloatingTopics/ap:Topic',ns):
                            ret = ret + firstcolumns
                            #ret = ret + gettopic(btopic)+extratopictext
                            #topicoid = dtopic.attrib["OId"]
                            topicoid = None
                            dtext = "None"
                            for topictext in dtopic.findall('./ap:Text',ns):
                                dtext = topictext.attrib["PlainText"]
                            # gather texts from subtopics of dtopic
                            for etopic in dtopic.findall('./ap:SubTopics/ap:Topic',ns):
                                topicoid = etopic.attrib["OId"]
                                for topictext in etopic.findall('./ap:Text',ns):
                                    dtext = dtext + topictext.attrib["PlainText"] + ", "
                            #ret = ret + (";\"%s\";\"%s\""%(topicoid,dtext+" / "+ctext+" / "+btext))
                            ret = ret + (";\"%s\";\"%s\""%(topicoid,dtext))

                            #ret = ret + getparents(list([topic,fttopic,atopic]))
                            #ret = ret + getparents(list([topic,btopic,ctopic]))
                            ret = ret + getparents(list([topic,ctopic]))
                            #ret = ret + gettopic(topic)
                            ret = ret + "\n"
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

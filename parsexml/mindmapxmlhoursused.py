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

week = None
user = None

documentcreated = None
documentlastmodified = None
documentversion = None

def getheader():
    return ("week;user;documentCreated;documentLastModified;documentVersion;topicOid;topicPlainText;customPropertyName;number\n").encode('utf-8')

def gettopic(topic):
    topicoid = topic.attrib["OId"]
    topicplaintext = None

    for topictext in topic.findall('./ap:Text',ns):
        topicplaintext = topictext.attrib["PlainText"]
    
    return (topicoid,topicplaintext)

def getcustomproperty(topic):
    # only return value when there's hours used information
    for custompropertiesbusinessdata in topic.findall('./ap:BusinessDataGroup/ap:CustomPropertiesBusinessData',ns):
        for customproperty in custompropertiesbusinessdata.findall('./ap:CustomPropertyGroup/ap:CustomProperty',ns):
            custompropertyname = customproperty.attrib["CustomPropertyName"]
            for custompropertyvalue in customproperty.findall('./ap:CustomPropertyValue',ns):
                number = custompropertyvalue.attrib["Number"]
                return (custompropertyname,number)
    return (None,None)

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

    # get any and all topics
    for topic in root.findall('.//ap:Topic',ns):
        (prop,number) = getcustomproperty(topic)
        if prop:
            (topicoid,topicplaintext) = gettopic(topic)
            ret = ret + ("%s;%s;%s;%s;%s;\"%s\";\"%s\";\"%s\";\"%s\"\n"%
                (week,user,documentcreated,documentlastmodified,documentversion,
                 topicoid,topicplaintext,prop,number))

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

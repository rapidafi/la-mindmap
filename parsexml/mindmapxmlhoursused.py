#!/usr/bin/python
# vim: set fileencoding=UTF-8 :
"""
mindmapxmlhoursused

Go thru given XML-file and parse and find certain information from it.
Return or output result as CSV-like data.
"""

import sys, os, getopt
import mindmapxml as mm

def getheader():
    ret = [["week","user","documentCreated","documentLastModified","documentVersion",
        "topicOid","topicPlainText","customPropertyName","number"]]
    return ret

def getcustomproperty(topic):
    # only return value when there's hours used information
    for custompropertiesbusinessdata in topic.findall('./ap:BusinessDataGroup/ap:CustomPropertiesBusinessData',mm.ns):
        for customproperty in custompropertiesbusinessdata.findall('./ap:CustomPropertyGroup/ap:CustomProperty',mm.ns):
            custompropertyname = customproperty.attrib["CustomPropertyName"]
            for custompropertyvalue in customproperty.findall('./ap:CustomPropertyValue',mm.ns):
                number = custompropertyvalue.attrib["Number"]
                return (custompropertyname,number)
    return (None,None)

# for module usage pass arguments
def parse(week,user):
    root = mm.getroot(week,user)

    (documentcreated,documentlastmodified,documentversion) = mm.getdocinfo(root)
    ret = []
    # get any and all topics
    for topic in root.findall('.//ap:Topic',mm.ns):
        (prop,number) = getcustomproperty(topic)
        if prop:
            (topicoid,topicplaintext) = mm.gettopic(topic)
            ret.append([week,user,documentcreated,documentlastmodified,documentversion,
                 topicoid,topicplaintext,prop,number])
    return ret

def main(argv):
    week = None
    user = None
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
        print("Mandatory arguments missing. Exiting.")
        sys.exit(2)

    print(getheader()+parse(week,user))

if __name__ == "__main__":
    main(sys.argv[1:])

#!/usr/bin/python
# vim: set fileencoding=UTF-8 :
"""
mindmapxmlrelationship

Go thru given XML-file and parse and find certain information from it.
Return or output result as CSV-like data.
"""

import sys, os, getopt
import mindmapxml as mm

def getheader():
    ret = "week;user;documentCreated;documentLastModified;documentVersion"
    ret = ret + ";topicOid;relTopicOid;plainText"
    ret = ret + "\n"
    return (ret).encode('utf-8')

# for module usage pass arguments
def parse(week,user):
    root = mm.getroot(week,user)

    (documentcreated,documentlastmodified,documentversion) = mm.getdocinfo(root)
    ret = ""
    for relationships in root.findall('.//ap:Relationships',mm.ns):
        for relationship in relationships.findall('./ap:Relationship',mm.ns):
            topicoid = None
            reltopicoid = None
            for objref in relationship.findall('./ap:ConnectionGroup[@Index="0"]/ap:Connection/ap:ObjectReference',mm.ns):
                topicoid = objref.attrib["OIdRef"]
            for objref in relationship.findall('./ap:ConnectionGroup[@Index="1"]/ap:Connection/ap:ObjectReference',mm.ns):
                reltopicoid = objref.attrib["OIdRef"]

            for topic in relationship.findall('./ap:FloatingTopics/ap:Topic',mm.ns):
                (realtopicoid,topicplaintext) = mm.gettopic(topic)
                # realtopicoid is the topics actual own oid (not interested...)
                ret = ret + ("%s;%s;%s;%s;%s;\"%s\";\"%s\";\"%s\"\n"%
                      (week,user,documentcreated,documentlastmodified,documentversion,
                      topicoid,reltopicoid,topicplaintext))

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

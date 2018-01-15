#!/usr/bin/python
# vim: set fileencoding=UTF-8 :
"""
mindmapxmltopic

Go thru given XML-file and parse and find certain information from it.
Return or output result as CSV-like data.
"""

import sys, os, getopt
import mindmapxml as mm

def getheader():
    ret = [["week","user","documentCreated","documentLastModified","documentVersion",
        "topicOid","topicLevel","topicPlainText","topicTaskPercentage","topicIconType"]]
    return ret

# for module usage pass arguments
def parse(week,user):
    root = mm.getroot(week,user)

    (documentcreated,documentlastmodified,documentversion) = mm.getdocinfo(root)
    ret = []
    for onetopic in root.findall('.//ap:OneTopic',mm.ns):
        for topic in onetopic.findall('./ap:Topic',mm.ns):
            elements = mm.subtopic(topic,0,[])
            for e in elements:
                (topicoid,topicplaintext,topiclevel,topicpercentage,topicicon,parents) = e
                ret.append([week,user,documentcreated,documentlastmodified,documentversion,
                       topicoid,topiclevel,topicplaintext,topicpercentage,topicicon])
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

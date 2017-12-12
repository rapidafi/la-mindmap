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
    ret = "week;user;documentCreated;documentLastModified;documentVersion"
    ret = ret + ";topicOid;topicPlainText;topicIconType;Priority;Percentage"
    ret = ret + "\n"
    return (ret).encode('utf-8')

# for module usage pass arguments
def parse(week,user):
    root = mm.getroot(week,user)

    (documentcreated,documentlastmodified,documentversion) = mm.getdocinfo(root)
    ret = ""
    for topic in root.findall('.//ap:Topic',mm.ns):
        (priority,percentage) = mm.getpriority(topic)
        if priority:
            (topicoid,topicplaintext) = mm.gettopic(topic)
            ret = ret + ("%s;%s;%s;%s;%s;\"%s\";\"%s\";\"%s\";\"%s\";%s\n"%
                (week,user,documentcreated,documentlastmodified,documentversion,
                 topicoid,topicplaintext,mm.gettopicicon(topic),mm.getprioritymarker(root,priority),percentage))

    return ret.encode('utf-8')

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
        print "Mandatory arguments missing. Exiting."
        sys.exit(2)

    print getheader()+parse(week,user)

if __name__ == "__main__":
    main(sys.argv[1:])

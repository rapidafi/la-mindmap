#!/usr/bin/python
# vim: set fileencoding=UTF-8 :
"""
mindomoxmlrelations

Go thru given XML-file and parse and find certain information from it.
Return or output result as CSV-like data.
"""

import sys, os, getopt
import mindomoxml as mm

def getheader():
    return [["id","fromId","toId","label","mapid","userid"]]

# for module usage pass arguments
def parse(week,user):
    root = mm.getroot(week,user)

    (mapid,name,authorId,creationDate,modificationDate) = mm.getdocinfo(root)
    ret = []
    for relation in root.findall('./mo:relations/mo:relation',mm.ns):
        (topicid,fromId,toId,label,userid) = (None,None,None,None,None)
        if "id" in relation.attrib: topicid = relation.attrib["id"]
        if "fromId" in relation.attrib: fromId = relation.attrib["fromId"]
        if "toId" in relation.attrib: toId = relation.attrib["toId"]
        if "label" in relation.attrib: label = relation.attrib["label"]
        userid = None #TODO

        ret.append([topicid,fromId,toId,label,mapid,userid])
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

#!/usr/bin/python
# vim: set fileencoding=UTF-8 :
"""
mindomoxmlmap

Go thru given XML-file and parse and find certain information from it.
Return or output result as CSV-like data.
"""

import sys, os, getopt
import mindomoxml as mm

def getheader():
    ret = "id,name,authorId,creationDate,modificationDate"
    ret = ret + "\n"
    return ret

def t(text):
    return "%s"%("\""+text+"\"" or "")

# for module usage pass arguments
def parse(week,user):
    root = mm.getroot(week,user)

    (id,name,authorId,creationDate,modificationDate) = mm.getdocinfo(root)
    return ("%s;%s;%s;%s;%s\n"%(t(id),t(name),t(authorId),t(creationDate),t(modificationDate)))

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

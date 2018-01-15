#!/usr/bin/python
# vim: set fileencoding=UTF-8 :
"""
mindomoxmluser

Go thru given XML-file and parse and find certain information from it.
Return or output result as CSV-like data.
"""

import sys, os, getopt
import mindomoxml as mm

def getheader():
    ret = "userID;firstName;lastName;userName"
    ret = ret + "\n"
    return (ret)

def t(text):
    return "\"%s\""%(text or "")

# for module usage pass arguments
def parse(week,user):
    root = mm.getroot(week,user)

    ret = ""
    for user in root.findall('./mo:mapUsers/mo:mapUser',mm.ns):
        (userID,firstName,lastName,userName) = (None,None,None,None)
        if "userID" in user.attrib: userID = user.attrib["userID"]
        if "firstName" in user.attrib: firstName = user.attrib["firstName"]
        if "lastName" in user.attrib: lastName = user.attrib["lastName"]
        if "userName" in user.attrib: userName = user.attrib["userName"]

        ret = ret + ("%s;%s;%s;%s\n"%(t(userID),t(firstName),t(lastName),t(userName)))

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

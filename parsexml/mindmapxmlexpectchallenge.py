#!/usr/bin/python
# vim: set fileencoding=UTF-8 :
"""
mindmapxmlexpectchallenge

Go thru given XML-file and parse and find certain information from it.
Return or output result as CSV-like data.
"""

import sys, os, getopt
import mindmapxml as mm

def getheader():
    ret = "week;user;documentCreated;documentLastModified;documentVersion"
    ret = ret + ";topicOid;topicPlainText;topicPercentage;topic1Oid;topic1PlainText;topic1Percentage;topic1Icon;topic0Oid;topic0PlainText"
    ret = ret + "\n"
    return (ret).encode('utf-8')

# for module usage pass arguments
def parse(week,user):
    root = mm.getroot(week,user)

    (documentcreated,documentlastmodified,documentversion) = mm.getdocinfo(root)
    firstcolumns = ("%s;%s;%s;%s;%s"%(week,user,documentcreated,documentlastmodified,documentversion))
    ret = ""
    for topic in root.findall('.//ap:OneTopic/ap:Topic',mm.ns):
        (toid,ttext) = mm.gettopic(topic)
        (tpercentage) = mm.gettopicpercentage(topic)
        (ticon) = mm.gettopicicon(topic)
        for fttopic in topic.findall('./ap:FloatingTopics/ap:Topic',mm.ns):
            # path to Expectations and ...challenges
            for atopic in fttopic.findall('./ap:SubTopics/ap:Topic',mm.ns):
                (aoid,atext) = mm.gettopic(atopic)
                (apercentage) = mm.gettopicpercentage(atopic)
                (aicon) = mm.gettopicicon(atopic)
                # one way (opiskelija1)
                for btopic in atopic.findall('./ap:FloatingTopics/ap:Topic',mm.ns):
                    (boid,btext) = mm.gettopic(btopic)
                    (bpercentage) = mm.gettopicpercentage(btopic)
                    (bicon) = mm.gettopicicon(btopic)
                    ret = ret + firstcolumns
                    ret = ret + ";\"%s\";\"%s\""%(boid,btext)
                    ret = ret + ";\"%s\""%(bpercentage) # task percentage
                    ret = ret + ";\"%s\";\"%s\""%(aoid,atext)
                    ret = ret + ";\"%s\""%(apercentage) # parent percentage
                    ret = ret + ";\"%s\""%(aicon)
                    ret = ret + ";\"%s\";\"%s\""%(toid,ttext)
                    ret = ret + "\n"
                # alternative way with enormous hierarchy and false location of written text (opiskelija2)
                for btopic in atopic.findall('./ap:SubTopics/ap:Topic',mm.ns):
                    (boid,btext) = mm.gettopic(btopic)
                    (bpercentage) = mm.gettopicpercentage(btopic)
                    (bicon) = mm.gettopicicon(btopic)
                    #TODO: fixme: b and c are actually parent topics which replace fttopic and atopic above in this scenario (only c is interesting, though)
                    for ctopic in btopic.findall('./ap:SubTopics/ap:Topic',mm.ns):
                        (coid,ctext) = mm.gettopic(ctopic)
                        (cpercentage) = mm.gettopicpercentage(ctopic)
                        (cicon) = mm.gettopicicon(ctopic)
                        for dtopic in ctopic.findall('./ap:FloatingTopics/ap:Topic',mm.ns):
                            (doid,dtext) = mm.gettopic(dtopic)
                            (dpercentage) = mm.gettopicpercentage(dtopic)
                            (dicon) = mm.gettopicicon(dtopic)
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
                            for etopic in dtopic.findall('./ap:SubTopics/ap:Topic',mm.ns):
                                for topictext in etopic.findall('./ap:Text',mm.ns):
                                    dtext = dtext + topictext.attrib["PlainText"].replace('"','""') #nb! for CSV replace "->""
                                    dtext = dtext + ", "
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

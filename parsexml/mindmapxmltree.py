#!/usr/bin/python
# vim: set fileencoding=UTF-8 :
"""
mindmapxmltree

Go thru given XML-file and parse and find certain information from it.
Return or output result as CSV-like data.
"""

import sys, os, getopt
import mindmapxml as mm

def getheader():
    ret = [[#"week","user","documentCreated","documentLastModified","documentVersion",
          "topic3Oid","topic3PlainText","topic2Oid","topic2PlainText","topic1Oid","topic1PlainText","topic0Oid","topic0PlainText"]]
    return ret

# for module usage pass arguments
def parse(week,user):
    root = mm.getroot(week,user)

    (documentcreated,documentlastmodified,documentversion) = mm.getdocinfo(root)
    ret = []
    for onetopic in root.findall('.//ap:OneTopic',mm.ns):
        for topic in onetopic.findall('./ap:Topic',mm.ns):
            elements = mm.subtopic(topic,0,[])
            # floating topics also (MSc for BSc)
            for floatingtopics in topic.findall('./ap:FloatingTopics',mm.ns):
                for fttopic in floatingtopics.findall('./ap:Topic',mm.ns):
                    elements = elements + mm.subtopic(fttopic,0,[])

            for e in elements:
                (topic3oid,topic3plaintext,topiclevel,topicemotion,topiccompetence,topicdifficulty,topiccallouttext,parents) = e
                # possibly rethink this next structure:
                # this is due to changing from topiclevel==3 only to include all levels also
                if topiclevel>=3:
                    (topic0oid,topic0plaintext) = parents[2]
                    (topic1oid,topic1plaintext) = parents[1]
                    (topic2oid,topic2plaintext) = parents[0]
                elif topiclevel==2:
                    (topic0oid,topic0plaintext) = parents[1]
                    (topic1oid,topic1plaintext) = parents[0]
                    (topic2oid,topic2plaintext) = (topic3oid,topic3plaintext)
                    (topic3oid,topic3plaintext) = (None,None)
                elif topiclevel==1:
                    (topic0oid,topic0plaintext) = parents[0]
                    (topic1oid,topic1plaintext) = (topic3oid,topic3plaintext)
                    (topic2oid,topic2plaintext) = (None,None)
                    (topic3oid,topic3plaintext) = (None,None)

                ret.append([#week,user,documentcreated,documentlastmodified,documentversion,
                           topic3oid,topic3plaintext,topic2oid,topic2plaintext,topic1oid,topic1plaintext,topic0oid,topic0plaintext])
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

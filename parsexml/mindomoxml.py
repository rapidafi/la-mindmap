#!/usr/bin/python
# vim: set fileencoding=UTF-8 :
"""
mindomoxml

Parse given XML-file and give access to certain information in it.
"""

import sys, os, getopt
import xml.etree.ElementTree as ET

# "globals"
ns = {'mo': 'http://schemas.mindomo.com/application/version-2.7'}

def getroot(week,user):
    tree = ET.parse('./'+week+'/'+user+'/Document.xml')
    return tree.getroot()

def gettopic(topic):
    topicid = topic.attrib["id"]
    topictext = topic.find('./mo:text',ns).text
    return (topicid,topictext)

def gettopicsymbol(topic):
    topicsymbolnumber = None
    topicsymbolsmiley = None
    for topicsymbol in topic.findall('./mo:symbols/mo:symbol',ns):
        if "number_" in topicsymbol.text:
            topicsymbolnumber = topicsymbol.text.replace("number_","")
        if "smiley_" in topicsymbol.text:
            topicsymbolsmiley = topicsymbol.text.replace("smiley_","")
    return (topicsymbolnumber,topicsymbolsmiley)

def getparents(parents):
    # collect all the parents to same line, reversed!
    ret = []
    for p in reversed(parents):
        ret.append(gettopic(p))
    return ret

def subtopic(parenttopic,topiclevel,parents):
    topiclevel = topiclevel + 1
    parents.append(parenttopic)
    ret = []
    for topic in parenttopic.findall('./mo:subTopics/mo:topic',ns):
        (topicid,topictext) = gettopic(topic)
        (symbolnumber,symbolsmiley) = gettopicsymbol(topic)
        ret.append((topicid,topictext,symbolnumber,symbolsmiley,topiclevel,getparents(parents)))
        # recursively loop subtopics and defuse list in list
        for e in subtopic(topic,topiclevel,list(parents)):
            ret.append(e)
    return ret

def getdocinfo(root):
    id = root.attrib["id"]
    name = root.find('./mo:name',ns).text
    authorId = root.find('./mo:author',ns).text
    creationDate = root.find('./mo:creationDate',ns).text
    modificationDate = root.find('./mo:modificationDate',ns).text

    return (id,name,authorId,creationDate,modificationDate)

# only module usage
def main(argv):
    print("Used as a module only. Exiting.")
    sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])

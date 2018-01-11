#!/usr/bin/python
# vim: set fileencoding=UTF-8 :
"""
mindmapxmlgen

Generate base XML-file.
"""

import sys, os, getopt
from xml.etree import ElementTree as ET
from xml.dom import minidom
import random, base64
from zipfile import ZipFile, ZIP_DEFLATED

# "globals"
ns = {
    "ap": "http://schemas.mindjet.com/MindManager/Application/2003",
    "cor": "http://schemas.mindjet.com/MindManager/Core/2003",
    "pri": "http://schemas.mindjet.com/MindManager/Primitive/2003",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance"
}
ap = ns['ap'] #comfort
cor = ns['cor']
pri = ns['pri']
xsi = ns['xsi']
ET.register_namespace('ap',ap)
ET.register_namespace('cor',cor)
ET.register_namespace('pri',pri)
ET.register_namespace('xsi',xsi)

"""Return a random string with given length consisting of predefined characters.
"""
def randomid(len=16,debug=False):
    chars="1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/"
    ret = ""
    for i in range(0, len):
        ret+=random.choice(chars)
        if debug: print(i, ret)
    return base64.b64encode(bytearray(ret,'ascii')).decode()

"""Add a Topic under given parent element.
"""
def addtopic(parent,plaintext):
    topic = ET.SubElement(parent, '{%s}Topic'%(ap))
    topic.set("OId",randomid())
    #NB! Placeholder!
    subtopics = ET.SubElement(topic, '{%s}SubTopics'%(ap))
    text = ET.SubElement(topic, '{%s}Text'%(ap))
    text.set("PlainText",plaintext)
    text.set("ReadOnly","false")
    font = ET.SubElement(text, '{%s}Font'%(ap))
    return topic

"""Return a pretty-printed XML string for the Element.
"""
def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

"""M A I N
"""
def main(argv):
    makezip = False
    zipfile = "mindmapxmlgen.mmap"
    documentfile = "Document.xml"
    debug = False

    try:
        opts, args = getopt.getopt(argv,"Zz:f:d",["makezip","zipfile=","documentfile=","debug"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-Z", "--makezip"): makezip = True
        elif opt in ("-z", "--zipfile"): zipfile = arg
        elif opt in ("-f", "--documentfile"): documentfile = arg
        elif opt in ("-d", "--debug"): debug = True

    root = ET.Element('{%s}Map'%(ap))
    root.set("OId",randomid())
    ##root.set("xmlns:ap","http://schemas.mindjet.com/MindManager/Application/2003")

    onetopic = ET.SubElement(root, '{%s}OneTopic'%(ap))

    topic0 = addtopic(onetopic, "Koneenrakennus ja mekaniikka")
    for subtopics0 in topic0.findall('.//ap:SubTopics',ns):
        topic1 = addtopic(subtopics0, "Oppiaine 1")
        for subtopics1 in topic1.findall('.//ap:SubTopics',ns):
            topic2 = addtopic(subtopics1,"Kurssi 1")
            for subtopics2 in topic2.findall('.//ap:SubTopics',ns):
                addtopic(subtopics2,"Sisältö 1")
                addtopic(subtopics2,"Sisältö 2")
            topic2 = addtopic(subtopics1, "Kurssi 2")
            for subtopics2 in topic2.findall('.//ap:SubTopics',ns):
                addtopic(subtopics2, "Sisältö 3")
                addtopic(subtopics2, "Sisältö 4")
        topic1 = addtopic(subtopics0, "Oppiaine 2")
        for subtopics1 in topic1.findall('.//ap:SubTopics',ns):
            topic2 = addtopic(subtopics1,"Kurssi 3")
            for subtopics2 in topic2.findall('.//ap:SubTopics',ns):
                addtopic(subtopics2,"Sisältö 5")
                addtopic(subtopics2,"Sisältö 6")
            topic2 = addtopic(subtopics1, "Kurssi 4")
            for subtopics2 in topic2.findall('.//ap:SubTopics',ns):
                addtopic(subtopics2, "Sisältö 7")
                addtopic(subtopics2, "Sisältö 8")

    if debug: print(prettify(root))

    if makezip:
        print("writing to file:",documentfile)
        f = open(documentfile, 'w', encoding='utf-8')
        #f.write(ET.tostring(root).decode('utf-8'))
        f.write(prettify(root))
        f.close()

        print("zipping to file:",zipfile)
        with ZipFile(zipfile,'w',compression=ZIP_DEFLATED) as z:
            if debug: print("zipping:",documentfile)
            z.write(documentfile)

if __name__ == "__main__":
    main(sys.argv[1:])

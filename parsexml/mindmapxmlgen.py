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
    #"cst": "http://schemas.mindjet.com/MindManager/UpdateCompatibility/2004",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance"
}
#xsi:schemaLocation="http://schemas.mindjet.com/MindManager/Application/2003 http://schemas.mindjet.com/MindManager/Application/2003 http://schemas.mindjet.com/MindManager/Core/2003 http://schemas.mindjet.com/MindManager/Core/2003 http://schemas.mindjet.com/MindManager/Delta/2003 http://schemas.mindjet.com/MindManager/Delta/2003 http://schemas.mindjet.com/MindManager/Primitive/2003 http://schemas.mindjet.com/MindManager/Primitive/2003"
#print(ns)
#print(ns['ap'])
ap = ns['ap'] #comfort
cor = ns['cor']
pri = ns['pri']
#cst = ns['cst']
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
    #topic.set("Gen","0000000000000000")
    #topic.set("Dirty","0000000000000001")
    #NB! Placeholder!
    subtopics = ET.SubElement(topic, '{%s}SubTopics'%(ap))
    #topicviewgroup = ET.SubElement(topic, '{%s}TopicViewGroup'%(ap))
    #topicviewgroup.set("ViewIndex","0")
    text = ET.SubElement(topic, '{%s}Text'%(ap))
    text.set("PlainText",plaintext)
    text.set("ReadOnly","false")
    #text.set("Dirty","0000000000000000")
    font = ET.SubElement(text, '{%s}Font'%(ap))

    # return
    return topic

"""Return a pretty-printed XML string for the Element.
"""
def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

############################################################################

def main(argv):
    templatedir = "template0/"
    documentfile = "Document.xml"
    zipfile = "mindmapxmlgen.mmap"
    makezip = False
    debug = False

    try:
        opts, args = getopt.getopt(argv,"t:f:z:Zd",["templatedir=","documentfile=","zipfile=","makezip","debug"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-t", "--templatedir"): templatedir = arg
        elif opt in ("-f", "--documentfile"): documentfile = arg
        elif opt in ("-z", "--zipfile"): zipfile = arg
        elif opt in ("-Z", "--makezip"): makezip = True
        elif opt in ("-d", "--debug"): debug = True

    root = ET.Element('{%s}Map'%(ap))
    root.set("OId",randomid())
    ##root.set("xmlns:ap","http://schemas.mindjet.com/MindManager/Application/2003")

    onetopic = ET.SubElement(root, '{%s}OneTopic'%(ap))

    """
    Tutkinto
    - Oppiaine 1
    -- Kurssi 1
    --- Sisältö 1
    --- Sisältö 2
    -- Kurssi 2
    --- Sisältö 3
    --- Sisältö 4
    - Oppiaine 2
    -- Kurssi 3
    --- Sisältö 5
    --- Sisältö 6
    -- Kurssi 4
    --- Sisältö 7
    --- Sisältö 8
    """

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
        xsddir='xsd/'
        backgroundfile='bin/background.png'
        print("writing to file:",documentfile)
        f = open(documentfile, 'w', encoding='utf-8')
        #f.write(ET.tostring(root).decode('utf-8'))
        f.write(prettify(root))
        f.close()

        print("zipping to file:",zipfile)
        with ZipFile(zipfile,'w',compression=ZIP_DEFLATED) as z:
            if debug: print("zipping:",documentfile)
            z.write(documentfile)
            #for fn in os.listdir(templatedir+xsddir):
            #    if os.path.isfile(templatedir+xsddir+fn):
            #        if debug: print("zipping:",templatedir+xsddir+fn)
            #        z.write(filename=templatedir+xsddir+fn,arcname=xsddir+fn)
            #if debug: print("zipping:",templatedir+backgroundfile)
            #z.write(filename=templatedir+backgroundfile,arcname=backgroundfile)

if __name__ == "__main__":
    main(sys.argv[1:])

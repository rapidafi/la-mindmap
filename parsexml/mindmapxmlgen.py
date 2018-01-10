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
#xsi:schemaLocation="http://schemas.mindjet.com/MindManager/Application/2003 http://schemas.mindjet.com/MindManager/Application/2003 http://schemas.mindjet.com/MindManager/Core/2003 http://schemas.mindjet.com/MindManager/Core/2003 http://schemas.mindjet.com/MindManager/Delta/2003 http://schemas.mindjet.com/MindManager/Delta/2003 http://schemas.mindjet.com/MindManager/Primitive/2003 http://schemas.mindjet.com/MindManager/Primitive/2003"
#print(ns)
#print(ns['ap'])
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

"""Return a pretty-printed XML string for the Element.
"""
def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

############################################################################

def main(argv):
    debug = False
    makezip = False

    try:
        opts, args = getopt.getopt(argv,"zd",["zip","debug"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-z", "--zip"): makezip = True
        elif opt in ("-d", "--debug"): debug = True

    #if debug: print("TEST RANDOM/OID GEN:",randomid(debug=debug))

    comment = ET.Comment('Concept Map Analytics: MindMap XML Generated')
    root = ET.Element('{%s}Map'%(ap))
    root.append(comment)


    custom = ET.SubElement(root, '{%s}Custom'%(cor))
    #custom.text = 'This child contains text & more.'
    #custom.set("Dirty","0000000000000001")
    custom.set("OId",randomid())
    custom.set("Uri","http://schemas.mindjet.com/MindManager/UpdateCompatibility/2004")
    custom.set("Index","0")
    #child_with_tail = ET.SubElement(root, '{%s}child_with_tail'%(ap))
    #child_with_tail.text = 'This child has regular text.'
    #child_with_tail.tail = 'And "tail" text.'

    onetopic = ET.SubElement(root, '{%s}OneTopic'%(ap))
    #onetopic.attrib = 'This & that'

    topic0 = ET.SubElement(onetopic, '{%s}Topic'%(ap))
    topic0.set("OId",randomid())

    subtopics0 = ET.SubElement(topic0, '{%s}SubTopics'%(ap))
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
    if(1==1):
        topic1 = ET.SubElement(subtopics0, '{%s}Topic'%(ap))
        topic1.set("OId",randomid())
        subtopics1 = ET.SubElement(topic1, '{%s}SubTopics'%(ap))
        if(2==2):
            topic2 = ET.SubElement(subtopics1, '{%s}Topic'%(ap))
            topic2.set("OId",randomid())
            subtopics2 = ET.SubElement(topic2, '{%s}SubTopics'%(ap))
            if(3==3):
                topic3 = ET.SubElement(subtopics2, '{%s}Topic'%(ap))
                topic3.set("OId",randomid())
                text = ET.SubElement(topic3, '{%s}Text'%(ap))
                text.set("PlainText","Sisältö 1: Tämän luennon opiskeluun käyttämäni aika")
                text.set("ReadOnly","false")
                font = ET.SubElement(text, '{%s}Font'%(ap))
            if(3==3):
                topic3 = ET.SubElement(subtopics2, '{%s}Topic'%(ap))
                topic3.set("OId",randomid())
                text = ET.SubElement(topic3, '{%s}Text'%(ap))
                text.set("PlainText","Sisältö 2: Tämän luennon opiskeluun käyttämäni aika")
                text.set("ReadOnly","false")
                font = ET.SubElement(text, '{%s}Font'%(ap))
            text = ET.SubElement(topic2, '{%s}Text'%(ap))
            text.set("PlainText","Kurssi 1")
            text.set("ReadOnly","false")
            font = ET.SubElement(text, '{%s}Font'%(ap))
        if(2==2):
            topic2 = ET.SubElement(subtopics1, '{%s}Topic'%(ap))
            topic2.set("OId",randomid())
            subtopics2 = ET.SubElement(topic2, '{%s}SubTopics'%(ap))
            if(3==3):
                topic3 = ET.SubElement(subtopics2, '{%s}Topic'%(ap))
                topic3.set("OId",randomid())
                text = ET.SubElement(topic3, '{%s}Text'%(ap))
                text.set("PlainText","Sisältö 3: Tämän luennon opiskeluun käyttämäni aika")
                text.set("ReadOnly","false")
                font = ET.SubElement(text, '{%s}Font'%(ap))
            if(3==3):
                topic3 = ET.SubElement(subtopics2, '{%s}Topic'%(ap))
                topic3.set("OId",randomid())
                text = ET.SubElement(topic3, '{%s}Text'%(ap))
                text.set("PlainText","Sisältö 4: Tämän luennon opiskeluun käyttämäni aika")
                text.set("ReadOnly","false")
                font = ET.SubElement(text, '{%s}Font'%(ap))
            text = ET.SubElement(topic2, '{%s}Text'%(ap))
            text.set("PlainText","Kurssi 2")
            text.set("ReadOnly","false")
            font = ET.SubElement(text, '{%s}Font'%(ap))
        text = ET.SubElement(topic1, '{%s}Text'%(ap))
        text.set("PlainText","Oppiaine 1")
        text.set("ReadOnly","false")
        font = ET.SubElement(text, '{%s}Font'%(ap))
    if(1==1):
        topic1 = ET.SubElement(subtopics0, '{%s}Topic'%(ap))
        topic1.set("OId",randomid())
        subtopics1 = ET.SubElement(topic1, '{%s}SubTopics'%(ap))
        if(2==2):
            topic2 = ET.SubElement(subtopics1, '{%s}Topic'%(ap))
            topic2.set("OId",randomid())
            subtopics2 = ET.SubElement(topic2, '{%s}SubTopics'%(ap))
            if(3==3):
                topic3 = ET.SubElement(subtopics2, '{%s}Topic'%(ap))
                topic3.set("OId",randomid())
                text = ET.SubElement(topic3, '{%s}Text'%(ap))
                text.set("PlainText","Sisältö 5: Tämän luennon opiskeluun käyttämäni aika")
                text.set("ReadOnly","false")
                font = ET.SubElement(text, '{%s}Font'%(ap))
            if(3==3):
                topic3 = ET.SubElement(subtopics2, '{%s}Topic'%(ap))
                topic3.set("OId",randomid())
                text = ET.SubElement(topic3, '{%s}Text'%(ap))
                text.set("PlainText","Sisältö 6: Tämän luennon opiskeluun käyttämäni aika")
                text.set("ReadOnly","false")
                font = ET.SubElement(text, '{%s}Font'%(ap))
            text = ET.SubElement(topic2, '{%s}Text'%(ap))
            text.set("PlainText","Kurssi 3")
            text.set("ReadOnly","false")
            font = ET.SubElement(text, '{%s}Font'%(ap))
        text = ET.SubElement(topic1, '{%s}Text'%(ap))
        text.set("PlainText","Oppiaine 2")
        text.set("ReadOnly","false")
        font = ET.SubElement(text, '{%s}Font'%(ap))
        if(2==2):
            topic2 = ET.SubElement(subtopics1, '{%s}Topic'%(ap))
            topic2.set("OId",randomid())
            subtopics2 = ET.SubElement(topic2, '{%s}SubTopics'%(ap))
            if(3==3):
                topic3 = ET.SubElement(subtopics2, '{%s}Topic'%(ap))
                topic3.set("OId",randomid())
                text = ET.SubElement(topic3, '{%s}Text'%(ap))
                text.set("PlainText","Sisältö 7: Tämän luennon opiskeluun käyttämäni aika")
                text.set("ReadOnly","false")
                font = ET.SubElement(text, '{%s}Font'%(ap))
            if(3==3):
                topic3 = ET.SubElement(subtopics2, '{%s}Topic'%(ap))
                topic3.set("OId",randomid())
                text = ET.SubElement(topic3, '{%s}Text'%(ap))
                text.set("PlainText","Sisältö 8: Tämän luennon opiskeluun käyttämäni aika")
                text.set("ReadOnly","false")
                font = ET.SubElement(text, '{%s}Font'%(ap))
            text = ET.SubElement(topic2, '{%s}Text'%(ap))
            text.set("PlainText","Kurssi 4")
            text.set("ReadOnly","false")
            font = ET.SubElement(text, '{%s}Font'%(ap))

    text = ET.SubElement(topic0, '{%s}Text'%(ap))
    text.set("PlainText","Koneenrakennus ja mekaniikka")
    text.set("ReadOnly","false")
    font = ET.SubElement(text, '{%s}Font'%(ap))

    #print(ET.tostring(root).decode('utf-8'))
    if debug: print(prettify(root))

    if makezip:
        file="Document.xml"
        zipfile="mindmapxmlgen.mmap"
        print("writing to file:",file)
        f = open(file, 'w', encoding='utf-8')
        f.write(prettify(root))
        f.close()

        print("zipping to file:",zipfile)
        with ZipFile(zipfile,'w',compression=ZIP_DEFLATED) as z:
            z.write(file)

if __name__ == "__main__":
    main(sys.argv[1:])

#!/usr/bin/python
# vim: set fileencoding=UTF-8 :
"""
mindmap2csv

Output the results of certain subdirectory files, with the help of other
modules in this directory, to ready-named files.

NB! Does not actually provide CSV tool as results are already CSV-like.
"""
import os, re
#import ucsv as csv

folders = ["Viikko1","Viikko2","Viikko3","Viikko4","Viikko5","Viikko6final"]
extension = ".mmap"

def handle(folder,item):
    user = re.sub(r'^(\d+)_.*$',r'\1',item)
    if not os.path.exists(folder+'\\'+user):
        print("USER DIRECTORY MISSING!",folder,user,item)
    #
    import mindmapxmltopic, mindmapxmltree
    topiccsv = mindmapxmltopic.parse(folder,user)
    treecsv = mindmapxmltree.parse(folder,user)
    ftopic.write(topiccsv)
    ftree.write(treecsv)

ftopic = open('mindmaptopic.csv', 'w')
ftree = open('mindmaptree.csv', 'w')

ftopic.write(("week,user;documentCreated;documentLastModified;documentVersion;topicOid;topicLevel;topicPlainText;topicTaskPercentage;topicIconType\n").encode('utf-8'))
ftree.write(("week;user;documentCreated;documentLastModified;documentVersion;topic3Oid;topic3PlainText;topic2Oid;topic2PlainText;topic1Oid;topic1PlainText;topic0Oid;topic0PlainText\n").encode('utf-8'))

for folder in folders:
    for item in os.listdir(folder):
        if item.endswith(extension):
            handle(folder,item)

ftopic.close()
ftree.close()
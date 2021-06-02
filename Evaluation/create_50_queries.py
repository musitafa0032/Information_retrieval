import os
import sys
import xml.etree.cElementTree as ET
import subprocess
import re
import nltk
from nltk.corpus import stopwords
import string

def create_query_file(topics_path, mapping_file, index_folder, file_to_write):
    doc_numbers = subprocess.check_output("awk '{print $1}' " +  mapping_file, shell = True) # get the topics that have qrel files
    doc_numbers = doc_numbers.decode("utf-8").split("\n")[1:-1]
    stopw = stopwords.words('swedish')

    with open(topics_path, 'r', encoding = "utf-8") as f:
        x = f.read().split('</TOP>')
        nrs = []
        titles = []
        for item in x:
            try:
                nr = re.search(r'<TOPNO>(.*?)</TOPNO>', item).group(1)
                title = re.search(r'<TITLE>(.*?)</TITLE>', item).group(1).strip().lower()
                if nr and title:
                    nrs.append(nr)
                    titles.append(title)
            except:
                pass
    topics = 0
    root2 = ET.Element("parameters")
    ET.SubElement(root2, "index").text = index_folder
    ET.SubElement(root2, "trecFormat").text = "true"
    for nr, q in zip(nrs, titles):
        if nr in doc_numbers and topics < 50:
            q = q.replace('/', ' ').replace(',', '').replace('.', '').replace('!', '').replace('?','').replace('- ', ' ')
            q = [w for w in q.split() if w not in stopw] 
            query = ET.SubElement(root2, "query")
            ET.SubElement(query, "number").text = nr 
            ET.SubElement(query, "text").text = "#combine(" + ' '.join(q) + ")"
            topics += 1
    tree2 = ET.ElementTree(root2)
    tree2.write(file_to_write, encoding = "utf-8")



if __name__ == "__main__":

    topics_path = sys.argv[1]
    mapping_file = sys.argv[2]
    index_folder = sys.argv[3]
    file_to_write = sys.argv[4]

    create_query_file(topics_path, mapping_file, index_folder, file_to_write)

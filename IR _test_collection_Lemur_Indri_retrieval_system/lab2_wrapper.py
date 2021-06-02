import os
import sys
import xml.etree.cElementTree as ET
import subprocess

collection_path = sys.argv[1]
corpus_class = sys.argv[2]
field_name = sys.argv[3]
assessment_file = sys.argv[4]

#Untar data
os.system("mkdir /tmp/ir_data_xyz")
os.system("tar -xf " + collection_path + " -C /tmp/ir_data_xyz/")
os.system("mkdir /tmp/ir_data_index_xyz")

#Create parameters file for index
root = ET.Element("parameters")
ET.SubElement(root, "index").text = "/tmp/ir_data_index_xyz"
ET.SubElement(root, "memory").text = "2G"
corpus = ET.SubElement(root, "corpus")
ET.SubElement(corpus, "path").text = "/tmp/ir_data_xyz"
ET.SubElement(corpus, "class").text = corpus_class
stemmer = ET.SubElement(root, "stemmer")
ET.SubElement(stemmer, "name").text = "krovetz"
field = ET.SubElement(root, "field")
ET.SubElement(field, "name").text = field_name
tree = ET.ElementTree(root)
tree.write("my_index_parameters_xyz.xml")

os.system("IndriBuildIndex my_index_parameters_xyz.xml")

query = input("Please enter your task number followed by a comma and then your query in the " +
              "Indri Query Language format. Example: '201,#combine(silicon valley)' " +
              "If you want to finish, type 'exit' instead.\n")
while query != 'exit':
    task, q = query.split(',')
    root2 = ET.Element("parameters")
    ET.SubElement(root2, "index").text = "/tmp/ir_data_index_xyz"
    queryx = ET.SubElement(root2, "query")
    ET.SubElement(queryx, "number").text = task
    ET.SubElement(queryx, "text").text = q
    ET.SubElement(root2, "trecFormat").text = "true"
    tree2 = ET.ElementTree(root2)
    tree2.write("my_query_xyz.xml")
  
    os.system("IndriRunQuery my_query_xyz.xml > my_rankings_xyz.trec")
    magazine = subprocess.check_output("head -1 my_rankings_xyz.trec | awk '{print $3}'| cut -c-2", shell = True)
    magazine = magazine.decode("utf-8").strip()
    os.system(f"grep {magazine} {assessment_file} > my_qrel_file_xyz.txt") # get only lines for the right data set
    os.system("trec_eval -q -m official my_qrel_file_xyz.txt my_rankings_xyz.trec")
    query = input("Please enter your task number followed by a comma and then your query in the " +
              "Indri Query Language format. Example: '201,#combine(silicon valley)' " +
              "If you want to finish, type 'exit' instead.\n")

#Remove created directories when the used has chosen to exit
os.system("rm -r /tmp/ir_data_xyz")
os.system("rm -r /tmp/ir_data_index_xyz")
os.system("rm my_query_xyz.xml")
os.system("rm my_rankings_xyz.trec")
os.system("rm my_qrel_file_xyz.txt")
os.system("rm my_index_parameters_xyz.xml")

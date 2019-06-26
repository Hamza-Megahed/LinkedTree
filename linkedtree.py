#!/usr/bin/python3

#===============================================================================
#  Name        : linkedtree.py
#  Author      : Hamza
#  Version     : v1.0
#  Description : Build a tree of domains and sub-domains
#===============================================================================

from treelib import Tree
import tldextract
import subprocess
import os

path='' # path to list of domains and sub-domians
file= open(path)
lines = file.read().splitlines()
    
tree = Tree()

tree.create_node("name of root node", "ID of root node")  # root node
for url in lines:

    domain=""
    subdomain=""
    domain = tldextract.extract(url).domain  
    subdomain = tldextract.extract(url).subdomain
    if not (tree.contains(domain)):
        tree.create_node(domain, domain, parent="ID of root node") #Add domains to root node
    if subdomain:    
        tree.create_node(subdomain, subdomain+domain, parent=domain) #Add sub-domains to domain node



file.close()

tree.show(line_type="ascii-emv") #show data as stdout

tree.to_graphviz(filename="tree_graphviz") #dump tree as graphviz
#dot  xxx -Tps -o test.ps -Grankdir=LR #left to right 
subprocess.call(["dot", "tree_graphviz", "-Tps", "-o" ,"output.ps" ,"-Grankdir=LR"]) #Grankdir=LR option to build tree from left to right
#convert -flatten -density 150 -geometry 100% test.ps test.png
subprocess.call(["convert" ,"-flatten" ,"-density" ,"150" ,"-geometry" ,"100%" ,"output.ps" ,
                 "tree_graphviz.png"],stderr=subprocess.DEVNULL) #convert graphviz to png 
# rm -rf tree_graphviz output.ps
subprocess.call(["rm", "-rf", "tree_graphviz", "output.ps"]) #clear files


if os.path.exists("output.txt"): #dump tree as text file
    subprocess.call(["rm", "-rf", "output.txt"])
tree.save2file('output.txt',line_type="ascii-emv")
with open('output.json', 'w') as f: #dump tree as json form
    f.write(tree.to_json(with_data=True))



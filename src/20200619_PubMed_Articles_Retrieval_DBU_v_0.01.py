# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 16:16:31 2020

@author: divak
"""


import pandas as pd
import numpy as np
import Biopython as Bio
from Bio import Entrez
import time
time.sleep(3)
# =============================================================================
# Defining function to search the pubmed
# =============================================================================
def search(query):
    Entrez.email = "divakarbuddha.pharmacy@gmail.com"
    handle = Entrez.esearch(db="pubmed", sort="relevance", retmax = "1000", retmode = "xml", term = query)
    results = Entrez.read(handle)
    return results
# =============================================================================
# Definting fetch function to fetch details of each pubmed ID
# =============================================================================
def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = "divakarbuddha.pharmacy@gmail.com"
    handle = Entrez.efetch(db="pubmed", retmode = "xml", id = ids)
    results2 = Entrez.read(handle)
    return results2
# =============================================================================
# All in one code to search pubmed and fetch the records
# =============================================================================
if __name__ == '__main__':
    time.sleep(1)
    results = search("chronic pain advanced treatment options today")
    time.sleep(0.5)
    id_list = results["IdList"]
    time.sleep(1)
    papers = fetch_details(id_list)
    for i, paper in enumerate(papers):
        print (i+1, paper)
        
        
        print("%d) %s" % (i+1, paper["MedLineCitation"]["Article"]["ArticleTitle"]))
        
    import json
    print(json.dumps(papers[0], indent =2, separators=(',', ':')))
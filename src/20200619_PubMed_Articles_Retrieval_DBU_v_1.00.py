# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 16:16:31 2020

@author: Divakar Buddha
"""


import pandas as pd
import numpy as np
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
    handle = Entrez.efetch(db="pubmed", retmode = "json", id = ids)
    results2 = Entrez.read(handle)
    return results2
# =============================================================================
# All in one code to search pubmed and fetch the records
# =============================================================================
if __name__ == '__main__':
    # time.sleep(1)
    results = search("chronic pain advanced treatment options today")
    # time.sleep(0.5)
    id_list = results["IdList"]
    papers = fetch_details(id_list)
    
    
list3 = ["26225261", "28401480", "7924119"]    
details_final = fetch_details(list3)
    # for each in papers:
    #     print(each)
    # for i, paper in enumerate(papers):
    #     print(i)
    #     print (i+1, paper)
# results9 = search("QSPainRelief")
# print(len(results9["Count"]))        
# print(results9["IdList"])       
        # print("%d) %s" % (i+1, paper["MedLineCitation"]["Article"]["ArticleTitle"]))
        
    # import json
    # print(json.dumps(papers[0], indent =2, separators=(',', ':')))
    
    
    # reference: https://marcobonzanini.com/2015/01/12/searching-pubmed-with-python/
    #reference 
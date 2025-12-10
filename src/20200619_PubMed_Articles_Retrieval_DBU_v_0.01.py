# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 11:36:36 2020

@author: divak
"""
# =============================================================================
# Trial 1: EntrezPy
# =============================================================================

# import entrezpy
# import entrezpy.conduit
# w = entrezpy.conduit.Conduit('divakarbuddha.pharmacy@gmail.com')
# fetch_rate_constants= w.new_pipeline()
# sid = fetch_rate_constants.add_search({'db':'pubmed', 'term': 'pain', 'rettype':'count'})
# fid = fetch_rate_constants.add_fetch({'retmax':1000, 'retmode':'text', 'rettype':'abstract'}, dependency=sid)
# final = w.run(fetch_rate_constants)
# final.result
# =============================================================================
# Trial 1 end: EntrezPy
# =============================================================================

# fetch_influenza = w.new_pipeline()
# sid = fetch_influenza.add_search({'db' : 'nucleotide', 'term' : 'H3N2 [organism] AND HA', 'rettype':'count', 'sort' : 'Date Released', 'mindate': 2000, 'maxdate':2019, 'datetype' : 'pdat'})
# fid = fetch_influenza.add_fetch({'retmax' : 10, 'retmode' : 'text', 'rettype': 'fasta'}, dependency=sid)
# w.run(fetch_influenza)
# =============================================================================
# Trial 2: 
# =============================================================================
# pip install biopython
from Bio import Entrez
# Defining the function search to fetch xml output containing the intial search results
# pip install pandas
import pandas as pd
# empty = pd.DataFrame()
# empty_list = []
def search(query):
    Entrez.email = "divakarbuddha.pharmacy@gmail.com"
    handle = Entrez.esearch(db="pubmed", sort="relevance", retmax = "1000", retmode = "xml", term = query)
    results = Entrez.read(handle)
    # global empty_list = []
    # empty_list.append(results["IdList"])
    # empty.append(results, ignore_index=True)
    return results
# Defining the fetch function to fetch the required details
def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = "divakarbuddha.pharmacy@gmail.com"
    # handle = Entrez.efetch(db, keywords)
    handle = Entrez.efetch(db="pubmed", retmode = "xml", id = ids)
    results2 = Entrez.read(handle)
    return results2

search("chronic pain advanced treatment options today")
results["IdList"]
fetch_details(id_list)
__main__
if __name__ == '__main__':
    results = search("chronic pain advanced treatment options today")
    id_list = results["IdList"]
    papers = fetch_details(id_list)
    for i, paper in enumerate(papers):
        print("%d) %s" % (i+1, paper["MedLineCitation"]["Article"]["ArticleTitle"]))
        
    import json
    print(json.dumps(papers[0], indent =2, separators=(',', ':')))
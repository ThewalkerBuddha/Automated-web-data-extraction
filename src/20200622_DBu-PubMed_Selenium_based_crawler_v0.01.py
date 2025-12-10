# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 14:58:55 2020

@author: divak
"""
# =============================================================================
# Crawler to access the abstracts for multiple keyword search results; since
# the Entre based python code is not working properly (API)
# =============================================================================
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# =============================================================================
# Dependencies
# =============================================================================
# pip install selenium
# pip install progressbar
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import sys
import os
import time
import datetime
import requests
from requests import get
from random import randint
import pandas as pd
import numpy as np
import re
import progressbar as Status
from progressbar import AnimatedMarker
from progressbar import Timer
import math
# =============================================================================
# Selenium Driver settings for smooth crawling
# =============================================================================
Capacity = DesiredCapabilities.CHROME
Capacity["pageLoadStrategy"] = "none"
Normal_capacity = DesiredCapabilities.CHROME
Normal_capacity["pageLoadStrategy"] = "normal"
My_options = webdriver.ChromeOptions()
prefs = ({"profile.managed_default_content_settings.images": 2, "disk-cache-size": 4096})
My_options.add_experimental_option("prefs", prefs)
My_options.add_argument("headless")#to load pages faster without opening every pafe in new windo
My_options.add_experimental_option('excludeSwitches', ['enable-logging'])#disabling the Devtools listening message
# =============================================================================
# Defining functions to test multiple conditions
# =============================================================================
# def any_of_the_conditions_fulfilled(*expected_conditions):
#     def any_of_conditions(driver):
#         for each_any in expected_conditions:
#             try:
#                 outcome_any = each_any(driver)
#                 if outcome_any:
#                     return outcome_any
#             except WebDriverException:
#                 pass
#         return False
#     return any_of_conditions
# def all_of_the_conditions_fulfilled(*expected_conditions):
#     def all_of_conditions(driver):
#         results = []
#         for each_all in expected_conditions:
#             try:
#                 outcome_all = each_all(driver)
#                 if not outcome_all:
#                     return False
#                 results.append(outcome_all)
#             except WebDriverException:
#                 return False
#         return results
#     return all_of_conditions
# def None_of_the_conditions_fulfilled(*expected_conditions):
#     def None_of_conditions(driver):
#         for each_none in expected_conditions:
#             try:
#                 outcome_none = each_none(driver)
#                 if outcome_none:
#                     return False
#             except WebDriverException:
#                 pass
#         return True
#     return None_of_conditions

# =============================================================================
# Loading keywords to be entered into the pubmed search tab
# =============================================================================

buddy = webdriver.Chrome("C:/BrowserDrivers/chromedriver")
buddy.get("https://pubmed.ncbi.nlm.nih.gov/")

buddy.find_element_by_xpath('//*[@id="account_login"]').click()
buddy.find_element_by_xpath('//*[@id="auth-options"]/div/div/a[4]').click()
username = buddy.find_element_by_xpath('//*[@id="id_username"]')
password = buddy.find_element_by_xpath('//*[@id="id_password"]')
username.send_keys("divakarbuddha")
password.send_keys("D124333r@#")
keep_logged = buddy.find_element_by_xpath('//*[@id="ncbi-auth-form"]/div/form/div[3]/label').click()
submit = buddy.find_element_by_xpath('//*[@id="ncbi-auth-form"]/div/form/div[4]/input[2]').click()


search_bar = buddy.find_element_by_xpath('//*[@id="id_term"]')
search_bar.send_keys('Agomelatine AND [("Association rate constant" OR "Kon") OR ("binding kinetics" OR "binding association rate constant" OR "binding rate constant" OR "binding rate constants")]')
Search = buddy.find_element_by_xpath('//*[@id="search-form"]/div[1]/div[1]/div/button/span').click()


# Getting numb
nr_results = buddy.find_element_by_xpath('//*[@class="value"]').text
search_results = int(nr_results.replace(",",""))
number_of_pages = search_results/200
iterations = math.ceil(number_of_pages)
iterations

updated_url = buddy.find_element_by_xpath('//meta[@property="og:url"]')
new_link = updated_url.get_attribute("content")

new2 = new_link+"&size=200&page="+str(1)

All_PMIDs = []

for every_page in range(1,iterations):
    page_number = str(every_page)
    to_be_parsed_link = new_link+"&size=200&page="+page_number
    buddy = webdriver.Chrome("C:/BroswerDrivers/chromedriver")
    buddy.get(to_be_parsed_link)
    All_IDs = buddy.find_elements_by_xpath('/html/head/meta[27]')
    list_4_IDs = []
    for each_id in All_IDs:
        id_value = each_id.get_attribute("content")
        list_4_IDs.append(id_value)
    for every_id in list_4_IDs:
        final_list = every_id.split(",")
    All_PMIDs.append(final_list)
        
# =============================================================================
# To have a glance of the data in the entrez dictionary file
# =============================================================================
k = []
v = []
for each in lm:
    k.append(each)
    v.append(lm[each])
DF = pd.DataFrame()
DF["Key"] = k
DF["value"] = v
DF.to_excel("output_.xlsx")

# =============================================================================
# From the IDs collected from scraping each, page data will be fetached using Entrez API    
# =============================================================================

from Bio import Entrez
def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = "divakarbuddha.pharmacy@gmail.com"
    handle = Entrez.efetch(db="pubmed", retmode = "xml", id = ids)
    results2 = Entrez.read(handle)
    return results2

data1 = fetch_details(final_lst)
for record in data1['PubmedArticle']:
    print(record['MedlineCitation']['PMID'])

View(data1)
data1['MedlineCitation']


PubMed_ID = []
URL = []
Authors = []
Affiliations = []
Language = []
NLM_ID = []
Country = []
Title = []
Journal = []
ISSN = []
Journal_volume = []
Journal_issue = []
Journal_Pages = []
Journal_Publication_Date = []
Abstract = []
Page_number = []
Article_Day = []
Article_Month = []
Article_Year = []




for record in data1['PubmedArticle']:
    try:
        PMD = record['MedlineCitation']['PMID']
    except:
        PMD = ""
    try:
        lnk = "https://www.ncbi.nlm.nih.gov/pubmed/"+PMD
    except:
        lnk =  "NA"
    try:
        Auth_1 = []
        Aff_1 = []        
        for every_1 in record['MedlineCitation']['Article']['AuthorList']:
            try:
                Aff = every_1['AffiliationInfo'][0]['Affiliation']
                print(Aff)
            except:
                Aff = "NA" 
            Aff_1.append(Aff)
            try:
                Auth_fore = every_1['ForeName']
                Auth_last = every_1['LastName']
                Auth_name = Auth_last + " " + Auth_fore
            except:
                Auth_name = "NA"
            Auth_1.append(Auth_name)
        
        Authors.append(Auth_1)
        Affiliations.append(Aff_1)
    except:
        ""
    try:
        Lang = record["MedlineCitation"]["Article"]["Language"]
    except:
        Lang = "NA"
    Language.append(Lang)
    try:
        NLM = record["MedlineCitation"]["MedlineJournalInfo"]["NlmUniqueID"]
    except:
        NLM = "NA"
    NLM_ID.append(NLM)        
    try:
        cntry = record["MedlineCitation"]["MedlineJournalInfo"]["Country"]
    except:
        cntry = "NA"
    Country.append(cntry)
    try:
        jrnl = record["MedlineCitation"]["Article"]["Journal"]["Title"]
    except:
        jrnl = "NA"
    Journal.append(jrnl)
    try:
        dt1 = record["MedlineCitation"]["Article"]["Journal"]["ISSN"]
        issn = dt1.strip(",")
    except:
        issn = "NA"
    ISSN.append(issn)
    try:
        vlm = record["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["Volume"]
    except:
        vlm = "NA"
    Journal_volume.append(vlm)
    try:
        issu = record["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["Issue"]
    except:
        issu = "NA"
    Journal_issue.append(issu)
    try:
        pg = record["MedlineCitation"]["Article"]["Pagination"]["MedlinePgn"]
    except:
        pg = "NA"
    Journal_Pages.append(pg)
    try:
        Pub_date = record["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"]
        yr = Article_Day["Year"]
        mnth = Article_Day["Month"]
        day = Article_Day["Day"]
        Date_published = yr +"-"+mnth+"-"+day
    except:
        Date_published = "NA"
    Journal_Publication_Date.append(Date_published)
    try:
        ttl = record["MedlineCitation"]["Article"]["ArticleTitle"]
    except:
        ttl = "NA"
    Title.append(ttl)
    try:
        Abs = record["MedlineCitation"]["Article"]["Abstract"]["AbstractText"]
    except:
        Abs = "Not Available"
    Abstract.append(Abs)
    
    try:
        Abs = record["MedlineCitation"]["Article"]

       

    


# Affl = record['MedlineCitation']['Article']['AuthorList'][0]['AffiliationInfo'][0]['Affiliation']
print(Authors)
print(Affiliations)

every_1
# =============================================================================
# To export abstract based text file
# =============================================================================

# option1 = buddy.find_element_by_id("save-results-panel-trigger").click()
# option_select = buddy.find_element_by_xpath('//*[@id="save-action-format"]/option[4]').click()
# option_final_select = buddy.find_element_by_xpath('//*[@id="save-action-panel-form"]/div[3]/button[1]').click()  # give the final output of abstracts of articles in each page
# values = buddy.find_elements_by_xpath('//*[@id="save-action-panel-form"]/div[1]/input[1]')
# =============================================================================

# =============================================================================
# API based search is giving less results than scraping hence making the entrez based search obsolete
# =============================================================================

# def search(query):
#     Entrez.email = "divakarbuddha.pharmacy@gmail.com"
#     handle = Entrez.esearch(db="pubmed", sort="relevance", retmax = "30000", retmode = "xml", term = query, idtype = "acc")
#     results = Entrez.read(handle)
#     return results

#   vals12 = search('Agomelatine AND [("Association rate constant" OR "Kon") OR ("binding kinetics" OR "binding association rate constant" OR "binding rate constant" OR "binding rate constants")]')  
# len(vals12['IdList'])
    
    



for record in data1['PubmedArticle']:
    print(record['MedlineCitation']['PMID'])





# =============================================================================
# 
# =============================================================================








# =============================================================================
# Driver path
# =============================================================================
# selenium driver location "C:/BrowserDrivers/chromedriver"
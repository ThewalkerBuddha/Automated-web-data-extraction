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

to_be_parsed_link = new_link+"&size=200&page="+page_number



# def remove_result_stat_chars(string):
#     split_string = string.split()
#     if (split_string[0]=="About"):
#         value = (split_string[1]).replace(",","")
#     else:
#         value = (split_string[0].replace(",",""))
#     return int(value)
# def Unique_dictionary_from_two_dictionaries (Dictionary1, Dictionary2):
#     for key in Dictionary1:
#         if key not in Dictionary2:
#             value = {key:Dictionary1[key]}
#             Dictionary2.update(value)
#     return Dictionary2
# =============================================================================
# Loading keywords to be entered into the pubmed search tab
# =============================================================================
# Give the path to the excel containingt he keywords list
buddy = webdriver.Chrome("C:/BrowserDrivers/chromedriver")
buddy.get("https://pubmed.ncbi.nlm.nih.gov/?term=chronic+pain&size=200")
# buddy.close
# =============================================================================
# To export abstract based text file
# =============================================================================

option1 = buddy.find_element_by_id("save-results-panel-trigger").click()
option_select = buddy.find_element_by_xpath('//*[@id="save-action-format"]/option[4]').click()
option_final_select = buddy.find_element_by_xpath('//*[@id="save-action-panel-form"]/div[3]/button[1]').click()  # give the final output of abstracts of articles in each page
values = buddy.find_elements_by_xpath('//*[@id="save-action-panel-form"]/div[1]/input[1]')
# =============================================================================
# 
# =============================================================================
val23 = buddy.find_elements_by_xpath('/html/head/meta[27]')
list90 = []
for each_n_every in val23:
    elem = each_n_every.get_attribute("content")
    list90.append(elem)

# values.text()

for each_item in list90:
    final_lst = each_item.split(",")

# final2 = []
# for each2 in final_lst:
#     final2.append(int(each2))
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
Affiliation = []
Language = []
NLM_ID = []
Country = []
Title = []
Journal = []
Journal_ISSN = []
Abstract = []
Page_number = []
Article_Day = []
Article_Month = []
Article_Year = []
Journal_volume = []
Journal_issue = []

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
        Affl = record["MedlineCitation"]["AffiliationInfo"]


for record in data1['PubmedArticle']:
    print(record['MedlineCitation']['PMID'])















# =============================================================================
# Driver path
# =============================================================================
# selenium driver location "C:/BrowserDrivers/chromedriver"
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


from os import getcwd, chdir
import os
os.chdir("E:/Divakar/WFH/01 QSPainRelief/DBu02/01 Literature Screening/01 Systematic Search")

# =============================================================================
# Functions to check if multiple conditions have been satisfied
# =============================================================================
def any_of_the_conditions_fulfilled(*expected_conditions):
    def any_of_conditions(driver):
        for each_any in expected_conditions:
            try:
                outcome_any = each_any(driver)
                if outcome_any:
                    return outcome_any
            except WebDriverException:
                pass
        return False
    return any_of_conditions
def all_of_the_conditions_fulfilled(*expected_conditions):
    def all_of_conditions(driver):
        results = []
        for each_all in expected_conditions:
            try:
                outcome_all = each_all(driver)
                if not outcome_all:
                    return False
                results.append(outcome_all)
            except WebDriverException:
                return False
        return results
    return all_of_conditions
def None_of_the_conditions_fulfilled(*expected_conditions):
    def None_of_conditions(driver):
        for each_none in expected_conditions:
            try:
                outcome_none = each_none(driver)
                if outcome_none:
                    return False
            except WebDriverException:
                pass
        return True
    return None_of_conditions
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
# Function to create a filename to be created for each drug + param search
# =============================================================================
def individual_filename(each_1, search_results):
    drg = (each_1.split("AND")[0]).replace('"','')
    Kon_list = list(range(0, search_results, 5))
    Koff_list = list(range(1, search_results, 5))
    KD_list = list(range(2, search_results, 5))
    MRT_list = list(range(3, search_results, 5))
    TMDD_list = list(range(4, search_results, 5))
    if (All_search_terms.index(each_1) in Kon_list):
        param = "Kon"
    elif (All_search_terms.index(each_1) in Koff_list):
        param = "Koff"
    elif (All_search_terms.index(each_1) in KD_list):
        param = "KD"
    elif (All_search_terms.index(each_1) in Kon_list):
        param = "MRT"
    else:
        param = "TMDD"
    filename = drg+"_ "+param
    return filename

# =============================================================================
# Loading keywords to be entered into the pubmed search tab
# =============================================================================
Search_strategy = pd.read_excel("E:/Divakar/WFH/01 QSPainRelief/DBu02/01 Literature Screening/01 Systematic Search/20220412_Literature_search_strategy_DBu_v_0.05.xlsx")
Search_strategy

terms = [x for x in Search_strategy["Search terms"] if str(x) !='nan']
drugs = [y for y in Search_strategy["Drugs"] if str(y) != 'nan']
short_term = [z for z in Search_strategy["Short term"] if str(z != 'nan')]

All_search_terms = []
# Creating all possible keyword to search for each drug i.e. 109 drugs X 5 key terms for search
for drg in drugs[107]:
    dg = drg
    print(dg)
    for trm in terms:
        p = drg+ " AND "+trm
        All_search_terms.append(p)
All_search_terms

from datetime import date
current = date.today()
dt = current.strftime('%Y%m%d')
# =============================================================================
# Opening the selenium, logging into pubmed account, locating the search bar
# =============================================================================

buddy = webdriver.Chrome("C:/BrowserDrivers/chromedriver") #desired_capabilities = Capacity, options = My_options)
buddy.get("https://pubmed.ncbi.nlm.nih.gov/")
time.sleep(randint(1,5))
buddy.find_element_by_xpath('//*[@id="account_login"]').click()
time.sleep(randint(2,7))
buddy.find_element_by_xpath('//*[@id="auth-options"]/div/div/a[8]').click()
condition1 = EC.element_to_be_clickable((By.XPATH, '//*[@id="id_username"]'))
condition2 = EC.element_to_be_clickable((By.XPATH, '//*[@id="id_password"]'))
WebDriverWait(buddy, 10).until(all_of_the_conditions_fulfilled(condition1, condition2))
username = buddy.find_element_by_xpath('//*[@id="id_username"]')
password = buddy.find_element_by_xpath('//*[@id="id_password"]')
username.send_keys("divakarbuddha")
password.send_keys("D124333r@#")
# keep_logged = buddy.find_element_by_xpath('//*[@id="ncbi-auth-form"]/div/form/div[3]/label').click()
submit = buddy.find_element_by_xpath('//*[@id="ncbi-auth-form"]/div/form/div[4]/input[2]').click()
time.sleep(randint(3,6))
buddy.find_element_by_xpath('//*[@id="opt-out-close"]/span').click()
# WebDriverWait(buddy, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id_term"]')))
# search_bar = buddy.find_element_by_xpath('//*[@id="id_term"]')

# =============================================================================
# Iterating the program over multiple key_word combinations
# =============================================================================
keyterm = []
Main_PMID = []

for each_1 in All_search_terms:
    time.sleep(randint(5,10))
    # if(All_search_terms.index(each_1) != 0):
    homepage = buddy.find_element_by_xpath('//*[@id="search-form"]/div[1]/a[1]')
    homepage.click()
    # else:
    #     ""
    search_bar = WebDriverWait(buddy, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="id_term"]')))
    search_bar.click()
    search_term = (each_1)
    search_bar.send_keys(search_term)
    Search = WebDriverWait(buddy, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search-form"]/div[1]/div[1]/div/button/span')))
    Search.click()
    # Getting numb
    try:
        last_page = buddy.find_element_by_xpath('//*[@id="search-results"]/section/div[1]/div/div[2]/div/h3')
        No_results = buddy.find_element_by_xpath('//*[@id="search-results"]/div[2]/div[1]/div[1]')
        if (last_page.text == '//*[@id="search-results"]/section/div[1]/div/div[2]/div/h3'):
            keyterm = [each_1]
            Main_PMID = ["results for this keyterm complete"]
            break
        elif (No_results.text == 'No results were found.'):
            keyterm = [each_1]
            Main_PMID = [""]
            break
        else:
            nr_results = buddy.find_element_by_xpath('//*[@class="value"]').text
            search_results = int(nr_results.replace(",",""))
            search_res1 = search_results+1
            number_of_pages = search_results/200
            pg_roundoff = math.ceil(number_of_pages)
            iterations = pg_roundoff + 1
            iterations
            
            updated_url = buddy.find_element_by_xpath('//meta[@property="og:url"]')
            new_link = updated_url.get_attribute("content")
            
            new2 = new_link+"&size=200&page="+str(1)
            # buddy.close()
            
            All_PMIDs = []
            Page_wise_PMIDs = []
            
            for every_page in range(1,iterations):
                if (every_page <= 1000):
                    time.sleep(randint(10,20))
                    page_number = str(every_page)
                    to_be_parsed_link = new_link+"&size=200&page="+page_number
                    # buddy = webdriver.Chrome("C:/BrowserDrivers/chromedriver")
                    buddy.get(to_be_parsed_link)
                    All_IDs = buddy.find_elements_by_xpath('/html/head/meta[29]')
                    list_4_IDs = []
                    for each_id in All_IDs:
                        id_value = each_id.get_attribute("content")
                        list_4_IDs.append(id_value)
                    for every_id in list_4_IDs:
                        final_list = every_id.split(",")
                    # Page_wise_PMIDs.append(final_list)
                    # All_PMIDs.pop(19)
                    All_PMIDs.append(final_list)
                    
                    ff = []
                    for j in All_PMIDs:
                        for k in j:
                            ff.append(k)
                    
                    filename = individual_filename(each_1, search_results)
                    # =============================================================================
                    #     Trial to get the information of keyword in the filename
                    # =============================================================================
                    Search_word = [search_term]*len(ff)
                    
                    Search_dataframe = pd.DataFrame()
                    Search_dataframe["Search_term"] = Search_word
                    Search_dataframe["PMIDs"] = ff 
                    Search_dataframe.to_excel(dt+"_"+filename+"_Search.xlsx")
                
                    keyterm.extend(p for p in Search_word)
                    Main_PMID.extend(q for q in ff)
                else:
                    break
    except NoSuchElementException:
        continue
all_search_interim = pd.DataFrame()
all_search_interim["keyterm"] = keyterm
all_search_interim["PMID"] = Main_PMID
all_search_interim.to_excel(dt+"DBu_All_keywords_search_interim_results.xlsx")
    
all_search_data = pd.DataFrame()
all_search_data["keyterm"] = keyterm
all_search_data["PMID"] = Main_PMID
all_search_data.to_excel(dt+"DBu_All_keywords_search_PMIDs.xlsx")
# =============================================================================
# Just so as not to loose data of the PMIDs, exporting the data as  chunks to excel sheet
# =============================================================================
n = 1000000
list_of_chunks = [all_search_interim[p:p+n] for p in range(0, all_search_interim.shape[0],n)]
str(list_of_chunks)

writer1 = pd.ExcelWriter('chunkwise_export_of_PMIDs_part1', engine = 'xlsxwriter')
writer2 = pd.ExcelWriter('chunkwise_export_of_PMIDs_part2', engine = 'xlsxwriter')
writer3 = pd.ExcelWriter('chunkwise_export_of_PMIDs_part3', engine = 'xlsxwriter')
writer4 = pd.ExcelWriter('chunkwise_export_of_PMIDs_part4', engine = 'xlsxwriter')
writer5 = pd.ExcelWriter('chunkwise_export_of_PMIDs_part5', engine = 'xlsxwriter')
writer6 = pd.ExcelWriter('chunkwise_export_of_PMIDs_part6', engine = 'xlsxwriter')
writer7 = pd.ExcelWriter('chunkwise_export_of_PMIDs_part7', engine = 'xlsxwriter')
writer8 = pd.ExcelWriter('chunkwise_export_of_PMIDs_part8', engine = 'xlsxwriter')
writer9 = pd.ExcelWriter('chunkwise_export_of_PMIDs_part9', engine = 'xlsxwriter')
writer10 = pd.ExcelWriter('chunkwise_export_of_PMIDs_part10', engine = 'xlsxwriter')
writer11 = pd.ExcelWriter('chunkwise_export_of_PMIDs_part11', engine = 'xlsxwriter')

for chunk in range(len(list_of_chunks)):
    value = chunk + 1
    print(value)
    data = list_of_chunks[chunk]
    if (value <= 10):
        # writer1 = pd.ExcelWriter('chunkwise_export_of_PMIDs_part1', engine = 'xlsxwriter')
        data.to_excel(writer1, sheet_name = 'Sheet'+str(value))
        # writer1.save()
        print("1 crore transacting")
    elif (10 < value <= 20):
        print("1 crore transactions complete")        
        writer1.save()
        # writer2 = pd.ExcelWriter('chunkwise_export_of_PMIDs_part2', engine = 'xlsxwriter')
        data.to_excel(writer2, sheet_name = 'Sheet'+str(value))
        # writer2.save()
        print("2 crore transacting")
    elif (20 < value <= 30):
        print("2 crore transactions complete")
        writer2.save()
        # writer3 = pd.ExcelWriter('chunkwise_export_of_PMIDs_part3', engine = 'xlsxwriter')
        data.to_excel(writer3, sheet_name = 'Sheet'+str(value))
        # writer3.save()
        print("3 crore transacting")
    elif (30 < value <= 40):
        print("3 crore transactions complete")  
        writer3.save()
        # writer4 = pd.ExcelWriter('chunkwise_export_of_PMIDs_part4', engine = 'xlsxwriter')
        data.to_excel(writer4, sheet_name = 'Sheet'+str(value))
        # writer4.save()
        print("4 crore transacting")
    elif (40 < value <= 50):
        print("4 crore transactions complete")
        writer4.save()
        # writer5 = pd.ExcelWriter('chunkwise_export_of_PMIDs_part5', engine = 'xlsxwriter')
        data.to_excel(writer5, sheet_name = 'Sheet'+str(value))
        # writer5.save()
        print("5 crore transacting")
    elif (50 < value <= 60):
        print("5 crore transactions complete")
        writer5.save()
        # writer6 = pd.ExcelWriter('chunkwise_export_of_PMIDs_part6', engine = 'xlsxwriter')
        data.to_excel(writer6, sheet_name = 'Sheet'+str(value))
        # writer6.save()
        print("6 crore transacting")
    elif (60 < value <= 70):
        print("6 crore transactions complete")
        writer6.save()
        # writer7 = pd.ExcelWriter('chunkwise_export_of_PMIDs_part7', engine = 'xlsxwriter')
        data.to_excel(writer7, sheet_name = 'Sheet'+str(value))
        # writer7.save()
        print("7 crore transacting")
    elif (70 < value <= 80):
        print("7 crore transactions complete")
        writer7.save()
        # writer8 = pd.ExcelWriter('chunkwise_export_of_PMIDs_part8', engine = 'xlsxwriter')
        data.to_excel(writer8, sheet_name = 'Sheet'+str(value))
        # writer8.save()
        print("8 crore transacting")
    elif (80 < value <= 90):
        print("8 crore transactions complete")
        writer8.save()
        # writer9 = pd.ExcelWriter('chunkwise_export_of_PMIDs_part9', engine = 'xlsxwriter')
        data.to_excel(writer9, sheet_name = 'Sheet'+str(value))
        # writer9.save()
        print("9 crore transacting")
    elif (90 < value <= 100):
        print("9 crore transactions complete")
        writer9.save()
        # writer10 = pd.ExcelWriter('chunkwise_export_of_PMIDs_part10', engine = 'xlsxwriter')
        data.to_excel(writer10, sheet_name = 'Sheet'+str(value))
        # writer10.save()
        print("10 crore transacting")
    elif (100 < value <= 110):
        print("10 crore transactions complete")
        writer10.save()
        # writer11 = pd.ExcelWriter('chunkwise_export_of_PMIDs_part11', engine = 'xlsxwriter')
        data.to_excel(writer11, sheet_name = 'Sheet'+str(value))
        # writer11.save()
        print("11th crore transactions going")
    else:
        pass
writer11.save()
# =============================================================================
# Creating a unique list of PMIDs
# =============================================================================
# all_unique_pmids = []
# for every_id in all_search_data["PMID"]:
#     if every_id not in all_unique_pmids:
#         all_unique_pmids.append(every_id)
        
# # =============================================================================
# # From the IDs collected from scraping each, page data will be fetched using Entrez API    
# # =============================================================================

# from Bio import Entrez
# def fetch_details(id_list):
#     ids = ','.join(id_list)
#     Entrez.email = "divakarbuddha.pharmacy@gmail.com"
#     Entrez.sleep_between_tries = 30
#     handle = Entrez.efetch(db="pubmed", retmode = "xml", id = ids)
#     results2 = Entrez.read(handle)
#     return results2

# # =============================================================================
# # fetching data for all PMIDs
# # =============================================================================

# data1 = fetch_details(all_unique_pmids)
# for record in data1['PubmedArticle']:
#     print(record['MedlineCitation']['PMID'])

#     # =============================================================================
#     # For each PMID record, pubmed data will be categorized
#     # =============================================================================
#     PubMed_ID = []
#     URL = []
#     Authors = []
#     Affiliations = []
#     Language = []
#     NLM_ID = []
#     Country = []
#     Title = []
#     Journal = []
#     ISSN = []
#     Journal_volume = []
#     Journal_issue = []
#     Journal_Pages = []
#     Journal_Publication_Date = []
#     Abstract = []
    
    
#     for record in data1['PubmedArticle']:
#         try:
#             PMD = record['MedlineCitation']['PMID']
#         except:
#             PMD = ""
#         try:
#             lnk = "https://www.ncbi.nlm.nih.gov/pubmed/"+PMD
#         except:
#             lnk =  "NA"
#         try:
#             Auth_1 = []
#             Aff_1 = []        
#             for every_1 in record['MedlineCitation']['Article']['AuthorList']:
#                 try:
#                     Aff = every_1['AffiliationInfo'][0]['Affiliation']
#                     print(Aff)
#                 except:
#                     Aff = "NA" 
#                 Aff_1.append(Aff)
#                 try:
#                     Auth_fore = every_1['ForeName']
#                     Auth_last = every_1['LastName']
#                     Auth_name = Auth_last + " " + Auth_fore
#                 except:
#                     Auth_name = "NA"
#                 Auth_1.append(Auth_name)
            
#             Authors.append(Auth_1)
#             Affiliations.append(Aff_1)
#         except:
#             ""
#         try:
#             Lang = record["MedlineCitation"]["Article"]["Language"]
#         except:
#             Lang = "NA"
#         Language.append(Lang)
#         try:
#             NLM = record["MedlineCitation"]["MedlineJournalInfo"]["NlmUniqueID"]
#         except:
#             NLM = "NA"
#         NLM_ID.append(NLM)        
#         try:
#             cntry = record["MedlineCitation"]["MedlineJournalInfo"]["Country"]
#         except:
#             cntry = "NA"
#         Country.append(cntry)
#         try:
#             jrnl = record["MedlineCitation"]["Article"]["Journal"]["Title"]
#         except:
#             jrnl = "NA"
#         Journal.append(jrnl)
#         try:
#             dt1 = record["MedlineCitation"]["Article"]["Journal"]["ISSN"]
#             issn = dt1.strip(",")
#         except:
#             issn = "NA"
#         ISSN.append(issn)
#         try:
#             vlm = record["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["Volume"]
#         except:
#             vlm = "NA"
#         Journal_volume.append(vlm)
#         try:
#             issu = record["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["Issue"]
#         except:
#             issu = "NA"
#         Journal_issue.append(issu)
#         try:
#             pg = record["MedlineCitation"]["Article"]["Pagination"]["MedlinePgn"]
#         except:
#             pg = "NA"
#         Journal_Pages.append(pg)
#         try:
#             Pub_date = record["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"]
#             yr = Pub_date["Year"]
#             mnth = Pub_date["Month"]
#             day = Pub_date["Day"]
#             Date_published = yr +"-"+mnth+"-"+day
#         except:
#             Date_published = "NA"
#         Journal_Publication_Date.append(Date_published)
#         try:
#             ttl = record["MedlineCitation"]["Article"]["ArticleTitle"]
#         except:
#             ttl = "NA"
#         Title.append(ttl)
#         try:
#             Abs = record["MedlineCitation"]["Article"]["Abstract"]["AbstractText"]
#         except:
#             Abs = "Not Available"
#         Abstract.append(Abs)
        
#         try:
#             Abs = record["MedlineCitation"]["Article"]


# Final_Pubmed_data = pd.DataFrame()
# Final_Pubmed_data["Published_date"] = Date_published
# Final_Pubmed_data["ISSN"] = ISSN
# Final_Pubmed_data["Journal"] = Journal
# Final_Pubmed_data["Volume"] = Journal_volume
# Final_Pubmed_data["Issue"] = Journal_issue
# Final_Pubmed_data["Pages"] = Journal_Pages
# Final_Pubmed_data["Language"] = Language
# Final_Pubmed_data["Country"] = Country
# Final_Pubmed_data["NLM_ID"] = NLM_ID
# Final_Pubmed_data["Authors"] = Authors
# Final_Pubmed_data["Affiliations"] = Affiliations
# Final_Pubmed_data["link"] = URL
# Final_Pubmed_data["PMID"] = PubMed_ID
# Final_Pubmed_data["Title"] = Title
# Final_Pubmed_data["Abstract"] = Abstract
# # Final_Pubmed_data["NCBI_keywords"] = 
# # Final_Pubmed_data["NCBI_MeSH-terms"] = 
# Final_Pubmed_data["Comments"] = ""




# writer2 = pd.ExcelWriter(dt+"DBu_Systemic_search_results.xlsx", engine="xlsxwriter")
# all_search_data.to_excel(writer2, Sheet_name = "Kwords_n_PMIDs")
# Final_Pubmed_data.to_excel(writer2, Sheet_name = "PubMed_results")
# writer2.save()


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








# =============================================================================
# Driver path
# =============================================================================
# selenium driver location "C:/BrowserDrivers/chromedriver"
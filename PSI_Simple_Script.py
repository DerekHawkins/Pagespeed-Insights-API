# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 11:43:52 2018

@author: derek.hawkins
"""

### Google PSI API 
### Use the following user agent as a technical source when siting this:
### For Desktop: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/72.0.3593.0 Safari/537.36
### For Mobile: Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MRA58N) AppleWebKit/537.36 
    ##(KHTML, like Gecko) Chrome/71.0.3559.0 Mobile Safari/537.36


import pandas as pd
import requests
import json
import time

key = ###Insert your Key Here###
### 1 column, First row must contain URL (in all caps) ###
speed_test_urls = pd.read_excel('C:/Users/Derek.Hawkins/Desktop/A Bunch of Excel Sheets/speed_test_api_dev.xlsx')
urls = speed_test_urls['URL'] 
data_list_mobile = []
data_list_desktop = []

for each in urls:
    url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url="
    url += each
    url += "&strategy=mobile"
    url += "&key="
    url += key
    call = requests.get(url)
    response = call.json()
    data = response["lighthouseResult"]['audits']['speed-index']
    speeddata = data['displayValue']
    data_list_mobile.append(speeddata)
    time.sleep(2)
    
for every in urls:
    urlDesktop = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url="
    urlDesktop += every
    urlDesktop += "&strategy=desktop"
    urlDesktop += "&key="
    urlDesktop += key
    call = requests.get(urlDesktop)
    response = call.json()
    dataDesktop = response["lighthouseResult"]['audits']['speed-index']
    speeddataDesktop = dataDesktop['displayValue']
    data_list_desktop.append(speeddataDesktop)
    time.sleep(2)

df = pd.DataFrame(data_list_mobile, columns=["Speed Index - Mobile"])
df["Speed Index - Desktop"] = data_list_desktop
df.to_csv(#insert your path here)
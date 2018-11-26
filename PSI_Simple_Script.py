# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 12:48:18 2018

@author: derek.hawkins
"""

import pandas as pd
import requests
import json
import time

### Google PSI API 
### Use the following user agent as a technical source when citing this:
### For Desktop: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/72.0.3593.0 Safari/537.36
### For Mobile: Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MRA58N) AppleWebKit/537.36 
    ##(KHTML, like Gecko) Chrome/71.0.3559.0 Mobile Safari/537.36



### Payload for API call, set up for DataFrame ###
key = #insert your key here. For assistance with generating key, consult this link https://developers.google.com/speed/docs/insights/v5/get-started
### 1 column, First row must contain URL (in all caps) ###
speed_test_urls = pd.read_excel('C:/Users/Derek.Hawkins/Desktop/A Bunch of Excel Sheets/speed_test_api_dev.xlsx')
urls = speed_test_urls["URL"]
check = "captchaResult"
data_list_mobile = []
data_list_desktop = []

### Speed Test for Mobile ###
for each in urls:
    payload = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url="
    payload += each
    payload += "&strategy=mobile"
    payload += "&key="
    payload += key
    call = requests.get(payload)
    response = call.json()
    if check in response:
        pass
    else:
        print("Error Found with the following URL: %s" % (each), ", remove or revise in your spreadsheet before continuing")
        break
    firstContent_mobile = str(response["lighthouseResult"]['audits']['first-contentful-paint']['displayValue'])
    timetoInteractive_mobile = str(response["lighthouseResult"]['audits']['interactive']['displayValue'])
    speedData_mobile = str(response["lighthouseResult"]['audits']['speed-index']['displayValue'])
    data_list_mobile.append((firstContent_mobile, timetoInteractive_mobile, speedData_mobile))
    time.sleep(2)

### Speed Test for Desktop ###   
for every in urls:
    urlDesktop = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url="
    urlDesktop += every
    urlDesktop += "&strategy=desktop"
    urlDesktop += "&key="
    urlDesktop += key
    call = requests.get(urlDesktop)
    response = call.json()
    if check in response:
        pass
    else:
        print("Error Found with the following URL: %s" % (each), ", remove or revise in your spreadsheet before continuing")
        break
    firstContent_desktop = str(response["lighthouseResult"]['audits']['first-contentful-paint']['displayValue'])
    speedData_desktop = str(response["lighthouseResult"]['audits']['speed-index']['displayValue'])
    timetoInteractive_desktop = str(response["lighthouseResult"]['audits']['interactive']['displayValue'])
    data_list_desktop.append((firstContent_desktop, timetoInteractive_desktop, speedData_desktop))
    time.sleep(2)


### Dataframe Developed ###
df_mobile = pd.DataFrame(data_list_mobile, columns=["First Content Paint - Mobile", "Time to Interactive - Mobile", "Speed Index - Mobile"])
df_desktop = pd.DataFrame(data_list_desktop, columns = ["First Content Paint - Desktop", "Time to Interactive - Desktop", "Speed Index - Desktop"]) 
pagespeed_report = pd.concat([df_mobile,df_desktop], axis=1)
pagespeed_report["URL"] = urls
#pagespeed_report.to_csv(#insert your path here)

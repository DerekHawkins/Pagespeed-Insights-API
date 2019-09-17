# Essentials #
import pandas as pd
import urllib
import requests
import time
import sys

# UI #
import easygui
from easygui import *


key = "Enter API Key Here"
check = "captchaResult"

service_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed/"
def speed_test_url(url, device):
    params = {
        "?url": url,
        'strategy': device,
        'key': key,
        }
    data = urllib.parse.urlencode(params, doseq=True)
    main_call = urllib.parse.urljoin(service_url, data)
    main_call = main_call.replace(r'%3F', r'?')
    return main_call

while 1:
    choices = ["Enter URLs Manually", "Upload File", "Close Program"]
    msg = "Welcome to the Site Speed Testing Tool How would you like to proceed?"
    reply = buttonbox(msg, choices=choices, title='Site Speed Testing Tool')

    if reply == 'Enter URLs Manually':
        value = textbox(msg="Enter your URLs for speed testing. URLs should contain 'https://' or 'http://' when entering. Make sure to submit one URL per line", title="Enter Urls", codebox=True, callback=None)
        if value == None:
            break
        else:
            my_list = value.split("\n")
            speed_test_urls = pd.DataFrame(my_list, columns=['URL'])
            speed_test_urls = speed_test_urls[speed_test_urls.URL != '']
    elif reply == 'Upload File':
        file = easygui.fileopenbox()
        speed_test_urls = pd.read_excel(file)
    elif reply == "Close Program":
        sys.exit(0)
    msgbox("Your files have been uploaded. Please wait as program runs.")
    speed_check = speed_test_urls["URL"]    
    msgbox("Mobile Speed Test Running. Please click Ok while the program runs in the background")
    data_list_mobile = []
    error_catch_m = []
    for m_check in speed_check:
        call = requests.get(speed_test_url(url=m_check, device='mobile'))
        response = call.json()
        if check in response:
            pass
        else:
            y = "Error Found with the following URL: %s" % (m_check), ", remove or revise in your spreadsheet"
            error_catch_m.append(y)
            continue
        firstContent_mobile = str(response["lighthouseResult"]['audits']['first-contentful-paint']['displayValue'])
        timetoInteractive_mobile = str(response["lighthouseResult"]['audits']['interactive']['displayValue'])
        speedData_mobile = str(response["lighthouseResult"]['audits']['speed-index']['displayValue'])
        data_list_mobile.append((firstContent_mobile, timetoInteractive_mobile, speedData_mobile))
        time.sleep(2)
    msgbox("Desktop Speed Test Running. Please click Ok while the program runs in the background")    
    data_list_desktop = []
    error_catch_dt = []
    for d_check in speed_check:
        call = requests.get(speed_test_url(url=d_check, device='desktop'))
        response = call.json()
        if check in response:
            pass
        else:
            x = "Error Found with the following URL: %s" % (d_check), ", remove or revise in your spreadsheet"
            error_catch_dt.append(x)
            continue
        firstContent_desktop = str(response["lighthouseResult"]['audits']['first-contentful-paint']['displayValue'])
        speedData_desktop = str(response["lighthouseResult"]['audits']['speed-index']['displayValue'])
        timetoInteractive_desktop = str(response["lighthouseResult"]['audits']['interactive']['displayValue'])
        data_list_desktop.append((firstContent_desktop, timetoInteractive_desktop, speedData_desktop))
        time.sleep(2)
    
    df_mobile = pd.DataFrame(data_list_mobile, columns=["First Content Paint - Mobile", "Time to Interactive - Mobile", "Speed Index - Mobile"])
    df_desktop = pd.DataFrame(data_list_desktop, columns = ["First Content Paint - Desktop", "Time to Interactive - Desktop", "Speed Index - Desktop"]) 
    pagespeed_report = pd.concat([df_mobile,df_desktop], axis=1)
    pagespeed_report = pagespeed_report.replace(" s", "", regex=True)
    pagespeed_report["URL"] = speed_check
    msgbox("Your speed test is complete. Please select an exisiting excel file or create a new file ending in .xlsx")
    pagespeed_report.to_excel(filesavebox(), index=False)

import requests
import pandas as pd
import html
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from datetime import timedelta
import time
import os
import json

def dateurlchanger(url, adddays, maxdate): # for webscraping, this url for scrapping massey has a date at the end, which changes for up to date scores e.g https://masseyratings.com/nba/games?dt=20201222
    dateofpage = url[-8:]
    date_time_obj = datetime.strptime(dateofpage, '%Y%m%d')
    maxd = datetime.strptime(maxdate, '%Y%m%d')
    if date_time_obj >= maxd:
        return 'UP TO DATE'
    else:
        date_time_obj1 = date_time_obj + timedelta(days=adddays) 
        date_time_obj1 = date_time_obj1.strftime('%Y%m%d')
        return url.replace(dateofpage, date_time_obj1)


def getnbafrommassey(urlstart, maxdate=(datetime.today().strftime('%Y%m%d'))): #needs the date to begin from and to put the url page to begin from, e.g = https://masseyratings.com/nba/games?dt=20210601
    SEP = os.sep
    projectpath = os.path.dirname(os.getcwd())
    json_fullpath = projectpath + SEP + "data" + SEP + "masseyscrap.json"
    df = pd.read_json(json_fullpath)
    dicc = df.to_dict('series') 
    massey = 0
    url = urlstart
    while massey == 0:
        time.sleep(5) # i tried reducing the time but causes problems when scrapping
        chrome_driver_path = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\90.0.4430.212\\chromedriver.exe' # havent been able to place driver in project 
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(executable_path = chrome_driver_path, options = options)
        url = dateurlchanger(url, 1, maxdate)
        if url == 'UP TO DATE':
            massey +=1
            print("UP TO DATE")
        else:
            driver.get(url)
            time.sleep(5)
            try:
                menu_lateral = driver.find_element_by_xpath('/html/body/div[5]/div[1]/table')
            except:
                massey+1
            time.sleep(5)
            gamerows = menu_lateral.find_elements_by_tag_name('tr')
            u = list(range(1,(len(gamerows)+1)))
            time.sleep(3)
            for i in u:
                gamedicc = {}
                try:
                    gameid = driver.find_element_by_xpath('/html/body/div[5]/div[1]/table/tbody/tr['+str(i)+']/td[1]/a').get_attribute('href')
                    time.sleep(1)
                    gamedate = driver.find_element_by_xpath('/html/body/div[5]/div[1]/table/tbody/tr['+str(i)+']/td[1]').text
                    teams = driver.find_element_by_xpath('/html/body/div[5]/div[1]/table/tbody/tr['+str(i)+']/td[2]').text
                    prediction = driver.find_element_by_xpath('/html/body/div[5]/div[1]/table/tbody/tr['+str(i)+']/td[5]').text
                    winpred = driver.find_element_by_xpath('/html/body/div[5]/div[1]/table/tbody/tr['+str(i)+']/td[6]').text
                    time.sleep(1)
                    score = driver.find_element_by_xpath('/html/body/div[5]/div[1]/table/tbody/tr['+str(i)+']/td[4]').text
                except:
                    pass
                gamedicc['Game Date'] = gamedate
                gamedicc['Teams'] = teams
                gamedicc['Prediction'] = prediction
                gamedicc['Win%Pred'] = winpred
                gamedicc['Score'] = score
                dicc[gameid] = gamedicc
            driver.close()
            time.sleep(5)
            testpath = json_fullpath + "test"    # THIS IS TO NOT OVERWRITE THE JSON USED LATER ON
            with open(testpath, 'w') as fp:
                json.dump(dicc, fp, indent=4)
            print("This date has been uploaded to json file: ", url[-8:])
        return "Finished"


def pageadderurl(url, counter): #this funcion is for adding/changing the page in the below func, onto a the end of the url eg https://www.oddsportal.com/basketball/usa/nba/results/#/page/
    return url + str(counter)


def getnbafromoddsportal(numberofpages): #for example, for the whole dataset, up to page 22
    count=1
    SEP = os.sep
    projectpath = os.path.dirname(os.getcwd())
    json_fullpath = projectpath + SEP + "data" + SEP + "oddsnba.json"
    with open(json_fullpath) as json_file:
        dicttotal = json.load(json_file)
    while count < numberofpages:
        url = 'https://www.oddsportal.com/basketball/usa/nba/results/#/page/'
        chrome_driver_path = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\90.0.4430.212\\chromedriver.exe'
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(executable_path = chrome_driver_path, options = options)
        url = pageadderurl(url, count)
        if url == 'UP TO DATE':
            count = numberofpages + 1
        else:
            driver.get(url)
            time.sleep(5)
            menu_lateral = driver.find_element_by_class_name('table-main')
            center = menu_lateral.find_element_by_tag_name('tbody')
            hh = center.find_elements_by_tag_name('tr')
            for elem in hh:
                t = elem.get_attribute('xeid')
                if t !=None:
                    dicttotal[t] = elem.text
            print(url)
            time.sleep(2)
            driver.close()
            time.sleep(1)
            testpath = json_fullpath + "test"      # THIS IS TO NOT OVERWRITE THE JSON USED LATER ON
            with open(testpath, 'w') as fp:
                json.dump(dicttotal, fp, indent=4)
            count +=1
            print(f'Page {count} loaded to json ok')
    return "done"
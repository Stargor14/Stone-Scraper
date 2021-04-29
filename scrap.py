import requests
import os
import json
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
browser = webdriver.Chrome(options=chrome_options)

def get_tweets(query='',scrolls=5):
    url = f'https://twitter.com/search?q={query}'
    browser.get(url)
    time.sleep(1)

    body = browser.find_element_by_tag_name('body')
    for i in range(scrolls):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
    tweets = browser.find_elements_by_tag_name("article")
    return tweets

def find_location(account):
    #https://twitter.com/TheAnimeEra
    url = f'https://twitter.com/{account}'
    browser.get(url)
    time.sleep(1)
    bio = browser.find_elements_by_tag_name("span")
    index=0
    for i in bio:
        try:
            if index == 22:
                for j in i.text:
                    if j.isdigit():
                        raise
                print([i.text,index])
            index+=1
        except:
            pass
    return bio

def run(tweets):
    results = []
    saved = []
    for x in range(len(tweets)):
        if x:
            try:
                tweet = {'msg':'','likes':0,'retweets':0,'comments':0,'type':None,'account':'','location':''}
                data = tweets[x].find_elements_by_tag_name('span')
                links = tweets[x].find_elements_by_tag_name('a')
                for i in links:
                    try:
                        if len(i.text) >= 2:
                            for j in range(len(i.text)):
                                if i.text[j] == '@':
                                    tweet['account'] = i.text[j+1:]
                    except Exception as e:
                        pass
                temp = 0
                n=0
                going = False
                msg=''
                for i in data:
                    txt = i.text
                    if txt==temp:
                        continue
                    temp = txt
                    try:
                        if 'K' in txt:
                            txt = float(txt[:-1])*1000
                        txt = float(txt)
                        if going:
                            tweet['msg'] = msg
                        if n==0:
                            tweet['comments'] = int(txt)
                        if n==1:
                            tweet['retweets'] = int(txt)
                        if n==2:
                            tweet['likes'] = int(txt)
                        going = False
                        n+=1
                    except Exception as e:
                        if txt == '·':
                            going = True
                            continue
                        if going:
                            msg+=txt
                results.append(tweet)
                #create table of index meanings
            except Exception as e:
                continue
    return results
    #welp selenium it is
results = []
for i in range(5,35,5):
    tweets = get_tweets(query='Anime',scrolls=i)
    for j in run(tweets):
        results.append(j)

for result in results:
    find_location(result['account'])
    for i in range(len(result['msg'])):
        try:
            if result['msg'][i:i+6] == '      ':
                result['type'] = 'meme'
        except Exception as e:
            #print(e)
            pass
for i in results:
    print(i)
print(len(results))

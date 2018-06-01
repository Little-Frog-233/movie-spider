#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 15:18:50 2018

@author: little-forg
"""

import json
from selenium import webdriver
import re
import time

def get_one_page(url):# get url
    path = 'chromedriver address'
    browser = webdriver.Chrome(path)
    try:
        browser.get(url)
        return browser.page_source
    finally:
        browser.close()

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield{
            'index':item[0],
            'image':item[1],
            'title':item[2].strip(),
            'actor':item[3].strip()[3:] if len(item[3])>3 else '',
            'time':item[4].strip()[5:] if len(item[4])>5 else '',
            'score':item[5].strip()+item[6].strip()
        }

def write_to_file(content):
    path = 'result.txt'
    with open(path,'a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')

def main(offset):
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)

if __name__ == '__main__':
    for i in range(10):
        main(offset=i*10)
        time.sleep(1)
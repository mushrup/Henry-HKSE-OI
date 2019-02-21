from urllib import request
from lxml import etree
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import csv
import random
import time
import logging
import PySimpleGUI as sg
from fake_useragent import UserAgent   
import requests
from lxml.html import fromstring

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"no")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

proxies = get_proxies()
for proxy in range(0,5):
	print (random.choice(list(proxies)))
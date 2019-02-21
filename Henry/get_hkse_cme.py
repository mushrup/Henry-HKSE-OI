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
out_name = 'database.csv'
out_name2 = "database2.csv"

values = ["a"]
layout = [[sg.Text('Date(\'yyyymmdd\',eg:20190118):')],      
          [sg.Input()],	  
          [sg.RButton('Read'), sg.Exit()]]      

window = sg.Window('Persistent GUI Window').Layout(layout)      
while True:      
    event, start_end = window.Read()      
    if event is None or event == 'Exit':      
        pass  
    else:
        values[0] = start_end[0]
        break
window.Close() 

dt = datetime.strptime(values[0], '%Y%m%d')
dt_str = dt.strftime('%Y%m%d')[-6:]
url = "https://www.hkex.com.hk/eng/stat/dmstat/dayrpt/hsif"+dt_str+".htm"
url2 = "https://www.hkex.com.hk/eng/stat/dmstat/dayrpt/hsifa"+dt_str+".htm"
dt_to_print = dt.strftime('%m/%d/%Y')

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

#proxies = get_proxies()

def numbers_to_output(out_name,url):
	with open(out_name,'w', encoding='utf-8') as outfile:
		my_headers=["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
					#"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
					#"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
					#"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14"
					]
		headers = {}
		#headers['User-Agent'] = UserAgent().random	
		headers['User-Agent'] = random.choice(my_headers)
		print(headers)
		
		#proxy = random.choice(list(proxies))
		#proxy_support = request.ProxyHandler({"http": proxy,"https":proxy})
		#opener = request.build_opener(proxy_support)
		#request.install_opener(opener)
		
		req = request.Request(url, headers = headers)
		req = request.urlopen(req).read().decode("utf8")
		sel=etree.HTML(req)

		try:
			web_text = sel.xpath(r"//body/pre/text()")[0]
			print ("Extracting from page: "+url)
			
		except Exception as e:
			logging.error("Error at "+str(datetime.now()))
			web_text = ""
		
		outfile.write(web_text)
numbers_to_output(out_name,url)
numbers_to_output(out_name2,url2)

final_name = "output.csv"
with open(out_name,'r CVXA') as infile, open(final_name,'a',encoding = 'utf-8') as outfile:
	count = 0
	for line in infile:
		count = count + 1
		if count == 39:
			outfile.write('\n'+dt_to_print+'|'+line.split()[16]+'|'+line.split()[17])
		if count == 41:
			outfile.write('|'+line.split()[16]+'|'+line.split()[17])
		if count == 43:
			outfile.write('|'+line.split()[16]+'|'+line.split()[17])
		if count == 45:
			outfile.write('|'+line.split()[16]+'|'+line.split()[17])
		if count == 47:
			outfile.write('|'+line.split()[16]+'|'+line.split()[17])

with open(out_name2,'r') as infile, open(final_name,'a',encoding = 'utf-8') as outfile:
	count = 0
	for line in infile:
		count = count + 1
		if count == 39:
			outfile.write('|'+line.split()[5])
		if count == 41:
			outfile.write('|'+line.split()[5])
		if count == 43:
			outfile.write('|'+line.split()[5])
		if count == 45:
			outfile.write('|'+line.split()[5])
		if count == 47:
			outfile.write('|'+line.split()[5])
			
sg.Popup('Please check file:',final_name)
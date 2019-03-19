# //*[@id="filterCollapse"]/div[1]/div[2]/div/div[1]
#
#
# driver.maximize_window()
import requests
import re
import time
from selenium import webdriver
from lxml import etree
import csv
from pyquery import PyQuery as pq
import time
import random
import pprint
# open browser
# path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
path = "C:\Program Files\Tencent\QQBrowser\chromedriver.exe"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
# chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
b = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
b.get('https://www.lagou.com/')
b.maximize_window()
pprint.pprint(b.get_cookies())
b.quit()

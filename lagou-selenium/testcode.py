# -*- coding: utf-8 -*-
# author:wnight 白夜
import requests
import re
import time
from selenium import webdriver
from lxml import etree
import csv
from pyquery import PyQuery as pq
import time
import random
import json
import requests
import pymongo
# from config import *
from bs4 import BeautifulSoup
import random
import time
from datetime import datetime, date, timedelta


datasum = 0
print('“产品有前景 发展空间大 年终奖 绩效奖金”'.split(' ' or ','or '”'or '“'or '；'or'、'))
print('“弹性工作；团队氛围；15薪”'.split(' ' or ','or '”'or '“'or '；'))
if '20:26发布'.find('发布')  == True:
    print(date.today().strftime("%Y-%m-%d"))
else:
    print('222')

pattern = re.compile('“(.*)”').findall('“产品有前景 发展空间大 年终奖 绩效奖金”')[0].split(' ' or '，'or','or '”'or '“'or '；'or'、')
print(pattern)

# 试一试是不是一致的
#
# 再把if判断翻过了，先判断日期的
#
# 'experienceNeed' : need.get_text().split(' / ')[0],























# soup = BeautifulSoup(b.page_source, 'lxml')
# Administratives = soup.select('div > div.choose-detail > div > div:nth-child(2) > a')
#
# for Administrative in Administratives:
#     data =  Administrative.get_text()
#     if data == '不限':
#         pass
#     else:
#         print(data)

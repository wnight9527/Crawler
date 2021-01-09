import re
import requests
import time
from lxml import etree
import os

url = 'https://zha.erocool.me/detail/1819010o343069.html'
print("开始访问：" + url + "\r\n")
#https://zh.erocool.me/detail/1594211o306030.html
result = requests.get(url,timeout=10,)
print(result.text)
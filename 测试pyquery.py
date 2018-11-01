from pyquery import PyQuery as pq
import json
import requests
from requests.exceptions import RequestException
import re
import time
url = 'http://maoyan.com/board/4?offset=0'
headers = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
}
response = requests.get(url, headers=headers)
# print(response.text)
# doc = pq(url='http://www.baidu.com')
# print(doc('head'))
doc2 = pq(response.text)
# print(doc2('head'))


a = doc2('.star')
print(a)
print(a.text())


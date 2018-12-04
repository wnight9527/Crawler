from pyquery import PyQuery as pq
import json
import requests
from requests.exceptions import RequestException
import re
import time
# url = 'http://maoyan.com/board/4?offset=0'
# headers = {
# 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
# }
# response = requests.get(url, headers=headers)
# # print(response.text)
# # doc = pq(url='http://www.baidu.com')
# # print(doc('head'))
# doc2 = pq(response.text)
# # print(doc2('head'))
#
#
# a = doc2('.star')
# print(a)
# print(a.text())

url = 'https://www.lagou.com/zhaopin/chanpinjingli1/1/?filterOption=3'
headers = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
}
response = requests.get(url, headers=headers)
print(response.text)
print('----------------------------------------')
# doc = pq(url='http://www.baidu.com')
# print(doc('head'))
doc2 = pq(response.text)
# a = doc2('.money')
# print(a.text())
b = doc2('.company_name')
b01 = b('div a')

print(b.text())
print('----------------------------------------')
print(b01)#全部的地址
print('----------------------------------------')
doc3 =pq(b01)
n02 = doc3('a:nth-child(2)')
print(n02)
print('----------------------------------------2')

for itemdizhi in b01.items():
    print(itemdizhi.attr('href'))

print('----------------------------------------')
d = doc2('.li_b_l')
print(d.text())
# 链接地址
html2 = '''
<a class="position_link" href="https://www.lagou.com/jobs/4926084.html" target="_blank" data-index="0" data-lg-tj-id="8E00" data-lg-tj-no="
                                                                                                0101
                                                                                        " data-lg-tj-cid="4926084" data-lg-tj-abt="dm-csearch-useUserAllInterest|1">
                                    <h3 style="max-width: 180px;">产品经理</h3>
                                                                                                                                                                                                                            <span class="add">[<em>徐汇区</em>]</span>
                                                                                                                                                                                                        </a>'''
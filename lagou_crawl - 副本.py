import json
import requests
from requests.exceptions import RequestException
import re
import time
from pyquery import PyQuery as pq

def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):

    # pattern = re.compile('<li.*?data-positionname="(.*?)" data-companyid.*?<span class="money">(.*?)</span>.*?<!--<i></i>-->(.*?)</div>.*?</li>', re.S)
    # items = re.findall(pattern, html)
    doc = pq(html)
    items = doc('.style')
    companyname = doc('.company_name')
    money = doc('.money')
    print(items.text())
    # for item in items:
    #     yield {
    #         'style': style[0],#岗位
    #         'companyname': companyname[0],#薪水
    #         'money': money[0],#经验要求
    #         # 'actor': item[3].strip()[3:],
    #         # 'time': item[4].strip()[5:],
    #         # 'score': item[5] + item[6]
    #     }

def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    base_url = 'https://www.lagou.com/jobs/positionAjax.json'
    params = {
        'px': default,
        'city': '上海',
        'district': '浦东新区',
        'needAddtionalResult': false
        'first':false,
        'pn':'4',
        'kd':'数据分析'
    }
    url = base_url + urlencode(params)





    html = get_one_page(url)
    print(parse_one_page(html))
    # for item in parse_one_page(html):
    #     print(item)
    # #     write_to_file(item)


if __name__ == '__main__':
    for i in range(25):
        main(offset=i)
        time.sleep(2)

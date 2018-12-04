import json
import requests
from requests.exceptions import RequestException
import re
import time

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
    # pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
    #                      + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
    #                      + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    pattern = re.compile('<li.*?data-positionname="(.*?)" data-companyid.*?<span class="money">(.*?)</span>.*?<!--<i></i>-->(.*?)</div>.*?</li>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'gangwei': item[0],#岗位
            'xignshui': item[1],#薪水
            'yaoqiu': item[2].strip(),#经验要求
            # 'actor': item[3].strip()[3:],
            # 'time': item[4].strip()[5:],
            # 'score': item[5] + item[6]
        }


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    # url = 'http://maoyan.com/board/4?offset=' + str(offset)
    url = 'https://www.lagou.com/zhaopin/chanpinjingli1/'+ str(offset)+'/?filterOption=3'

    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(25):
        main(offset=i)
        time.sleep(4)

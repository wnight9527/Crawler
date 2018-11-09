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
    pattern = re.compile('<div class="List-item">.*?element_name="User" target="_blank".*?alt=\"(.*?)\"/>.*?<div class="RichText ztext">(.*?)</div><div class="ContentItem-status">.*?<span class="ContentItem-statusItem">(.*?)</span><span class="ContentItem-statusItem">(.*?)</span><span class="ContentItem-statusItem">(.*?)</span></div></div></div></div><div class="ContentItem-extra">', re.S)
    items = re.findall(pattern, html)


    for item in items:
        yield {
            'name': item[0],
            'Description': item[1],
            'answer': item[2].strip()[:-3],
            'Article': item[2].strip()[:-3],
            'follow': item[3].strip()[:-3]
        }


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = 'https://www.zhihu.com/people/whight001/following?page=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(23):
        main(offset=i)
        time.sleep(1)

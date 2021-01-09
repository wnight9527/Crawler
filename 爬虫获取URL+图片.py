import re
import requests
import time
from lxml import etree
import os
def download(html):
    htmlxpath = etree.HTML(html)
    html_data = htmlxpath.xpath('//*[@id="comicdetail"]/h1/text()')

    news_title = html_data[0]
    char_list = ['*', '|', ':', '?', '/', '<', '>', '"', '\\']
    news_title_result = news_title
    for i in char_list:
        if i in news_title:
            news_title_result = news_title.replace(i, "_")
    filespath = "D:\Project\downloadjpgtest\\" + news_title_result
    isExists = os.path.exists(filespath)
    # 判断结果
    if not isExists:
        os.mkdir(filespath)
        # os.makedirs(path)

        # 通过正则匹配
        re1 = "https://i0.nyacdn.com/galleries/[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|].jpg"

        pic_url = re.findall(re1, html, re.S)
        pic_url = list(dict.fromkeys(pic_url))#去重

        i = 1
        for key in pic_url:
            print("开始下载图片：" + key + "\r\n")
            try:
                pic = requests.get(key, timeout=30)
            except requests.exceptions.ConnectionError:
                print('图片无法下载')
                continue
            except requests.exceptions.ReadTimeout:
                print('图片无法下载')
                continue
            # 保存图片路径
            dir = filespath +"\\" + str(i) + '.jpg'
            fp = open(dir, 'wb')
            fp.write(pic.content)
            fp.close()
            i += 1
            print("下载完成：" + key + "\r\n")
        time.sleep(15)


def main(detail):
    url = 'https://zh.erocool.me' + detail
    print("开始访问：" + url + "\r\n")
    #https://zh.erocool.me/detail/1594211o306030.html
    result = requests.get(url)
    download(result.text)
    # print(result.text)

def pagefind():
    url = 'https://zhb.erocool.me/rank/history/page'
    print("开始访问：" + url + "\r\n")
    # https://zh.erocool.me/detail/1594211o306030.html
    '''
    https://zh.erocool.me/character/utaha-kasumigaoka/popular
    https://zh.erocool.me/artist/michiking/popular
    '''
    result = requests.get(url)
    # print(result.text)
    htmlxpath = etree.HTML(result.text)
    html_data = htmlxpath.xpath('//*[@id="list"]/div[2]/a/@href')
    for i in html_data:
        print(i)
        main(i)
    # print(result.text)


if __name__ == '__main__':
    pagefind()
    # main()

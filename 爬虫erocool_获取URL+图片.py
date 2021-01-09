import re
import requests
import time
from lxml import etree
import os
#增加归档文件夹，在归档里的不再下载
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3823.400 QQBrowser/10.7.4307.400',
     # "cookie":"_ga=GA1.2.404991466.1609568493; _gid=GA1.2.132176058.1610196414; splash_i=false; splashWeb-3880588-42=1; __cfduid=d0120f5b556166c9344aabeec2084ee631610199412",
     }
sleepJudge = 0
errorTimes = 0
correctTimes = 0
URLlist =[
    # 作者
    "https://zha.erocool.me/artist/pochi/popular",
    "https://zh.erocool.me/artist/michiking/popular",
    "https://zha.erocool.me/artist/haitokukan/popular",
    #排行榜
    "https://zhb.erocool.me/rank/history/page/1",
    "https://zhb.erocool.me/rank/history/page/2",
    "https://zhb.erocool.me/rank/history/page/3",
    "https://zhb.erocool.me/rank/history/page/4",
    "https://zhb.erocool.me/rank/month/page/1",
    "https://zhb.erocool.me/rank/month/page/2",
    "https://zhb.erocool.me/rank/month/page/3",
    "https://zhb.erocool.me/rank/month/page/4",
    "https://en.erocool1.com/rank/month/page/1",
    "https://zha.erocool.me/rank/week",
    "https://zha.erocool.me/rank/popular/1",
    #特点
    "https://zh.erocool.me/character/utaha-kasumigaoka/popular",
    "https://zha.erocool.me/character/utaha-kasumigaoka/popular",
    "https://zha.erocool.me/character/megumi-kato/popular",
    "https://zha.erocool.me/tag/blowjob/popular",
    "https://zha.erocool.me/tag/big-breasts/popular",
    "https://zha.erocool.me/tag/femdom/popular",
    "https://zha.erocool.me/tag/full-color/popular",

]

def download(html):
    global sleepJudge
    global errorTimes
    global correctTimes
    news_artist = "NULL"
    htmlxpath = etree.HTML(html)
    html_data = htmlxpath.xpath('//*[@id="comicdetail"]/h1/text()')
    html_artist = htmlxpath.xpath('//*[@id="comicdetail"]/div[2]/div[2]/div[2]/a[1]/text()')
    news_title = html_data[0]
    if html_artist[0]:
        news_artist = html_artist[0]
    char_list = ['*', '|', ':', '?', '/', '<', '>', '"', '\\']
    news_title_result = news_title
    for i in char_list:
        if i in news_title:
            news_title_result = news_title.replace(i, "_")

    basedpath = "D:\Project\Pic_ERo_Download\\"
    filespath =basedpath + "["+news_artist+"]"+ news_title_result
    filespath2 = basedpath +"[_BAD\\"+ "[" + news_artist + "]" + news_title_result
    filespath3 = basedpath +"[_GOOD\\"+ "[" + news_artist + "]" + news_title_result

    isExists = os.path.exists(filespath)
    isExists2 = os.path.exists(filespath2)
    isExists3 = os.path.exists(filespath3)
    # a = os.listdir(path)#文件名列表
    # 判断结果
    if not isExists and not isExists2 and not isExists3:
        os.mkdir(filespath)
        # os.makedirs(path)

        # 通过正则匹配
        re1 = "https://i0.nyacdn.com/galleries/[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|].jpg"

        pic_url = re.findall(re1, html, re.S)
        pic_url = list(dict.fromkeys(pic_url))#去重

        i = 0
        for key in pic_url:
            time.sleep(2.5)
            sleepJudge += 1
            i += 1
            ifSleep()
            print("开始下载图片：" + key + "\r\n")
            try:
                pic = requests.get(key, timeout=30,headers=headers)
            except requests.exceptions.ConnectionError:
                errorTimes +=1
                print('图片无法下载，连接异常:'+ str(errorTimes) + "次")

                continue
            except requests.exceptions.ReadTimeout:
                errorTimes +=1
                print('图片无法下载,连接超时：'+ str(errorTimes) + "次")
                continue
            # 保存图片路径
            dir = filespath +"\\" + str(i) + '.jpg'
            fp = open(dir, 'wb')
            fp.write(pic.content)
            fp.close()
            correctTimes+=1
            print("下载完成：" + str(correctTimes) +"次 "+news_title_result+ key +  "\r\n")


#10次下载睡眠一次
def ifSleep():
    global sleepJudge
    if sleepJudge >= 10:
        print("休息一下" + "\r\n")
        time.sleep(20)
        sleepJudge = 0

#访问漫画具体页面
def main(detail):
    url = 'https://zha.erocool.me' + detail
    print("开始访问：" + url + "\r\n")
    #https://zh.erocool.me/detail/1594211o306030.html
    result = requests.get(url)
    download(result.text)
    # print(result.text)

def pagefind(url):

    print("开始访问主页：" + url + "\r\n")
    try:
        result = requests.get(url, timeout=10,headers=headers)
        # print(result.text)
        htmlxpath = etree.HTML(result.text)
        html_data = htmlxpath.xpath('//*[@id="list"]/div[2]/a/@href')
        print("开始访问子页面》》》" + "\r\n")
        for i in html_data:
            print(i)
            main(i)
        # print(result.text)
    except requests.exceptions.ConnectionError:
        print('主页无法访问，连接异常')
    except requests.exceptions.ReadTimeout:
        print('主页无法访问,连接超时')





if __name__ == '__main__':
    for i in URLlist:
        pagefind(i)
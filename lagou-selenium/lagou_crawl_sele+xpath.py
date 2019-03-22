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
from bs4 import BeautifulSoup
import random
import time
from datetime import datetime, date, timedelta
from Range import *
from config import *

'''
问题：
有些职位因为搜索条件相近，会重复，需要清洗
数据库，怎么分表？
基本把功能实现了，之后第一页的时候爬取二级目录，并且保存 上海这个层级
更新：
把数据处理了下 时间与酬薪
可以把城市获取也改成自动的
学习了全局变量的用法

好像会突然停下来不dong?

'''

#职位数
datasum = 0

# net start MongoDB
# 开启指令
# open browser--两个地址
path=r"C:\Users\white\AppData\Local\Google\Chrome\Application\chromedriver.exe"
# path = "C:\Program Files\Tencent\QQBrowser\chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument()
# chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
b = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)

#执行30页爬取
def main(mongo_table):
    global datasum  # 在使用前初次声明
    #根据职位数计算页数
    Number_positions = int(re.findall(r"\d+", b.find_element_by_class_name('active').text)[0])

    for number in range(0,Number_positions//15+1):
        parse_link(mongo_table)
        print('SUM ', datasum)
        # sleep随机时间
        Interval = random.uniform(3, 4)
        time.sleep(Interval)

        #不是最后一页就继续下一页
        try :
            nextButton = b.find_element_by_class_name('pager_next')
            if nextButton.is_enabled() == True:
                nextButton.click()
                print('进入下一页-----> ')
            else:
                break
        except Exception:
            break

#分析及保存数据库
def parse_link(mongo_table):
    global datasum  # 在使用前初次声明

    soup = BeautifulSoup(b.page_source, 'lxml')
    positions = soup.select('ul > li > div.list_item_top > div.position > div.p_top > a > h3')
    adds = soup.select('ul > li > div.list_item_top > div.position > div.p_top > a > span > em')
    publishs = soup.select('ul > li > div.list_item_top > div.position > div.p_top > span')
    moneys = soup.select('ul > li > div.list_item_top > div.position > div.p_bot > div > span')
    needs = soup.select('ul > li > div.list_item_top > div.position > div.p_bot > div')
    companys = soup.select('ul > li > div.list_item_top > div.company > div.company_name > a')
    EnterpriseCorrelations = soup.select('ul > li > div.list_item_top > div.company > div.industry')
    tags = []
    if soup.find('div', class_='li_b_l'):
        tags = soup.select('ul > li > div.list_item_bot > div.li_b_l')
    fulis = soup.select('ul > li > div.list_item_bot > div.li_b_r')

    for position,add,publish,money,need,company,tag,fuli,EnterpriseCorrelation in \
            zip(positions,adds,publishs,moneys,needs,companys,tags,fulis,EnterpriseCorrelations):

        publishTime = publish_Data_cleaning(publish)
        moneyTemp2 = money_Data_cleaning(money)
        EnterpriseCorrelationTemp = EnterpriseCorrelationData_cleaning(EnterpriseCorrelation.get_text())
        # 考虑到学历可以抵扣一部分经验，其实可以集合考虑
        #fuli tag可能为空的
        try:
            fuliTemp = re.compile('“(.*)”').findall(fuli.get_text())[0]
        except Exception:
            fuliTemp = ''
            continue
        try:
            tagTemp =  tag.get_text().replace('\n','-')
        except Exception:
            tagTemp = ''
            continue
        data = {
            'position' : position.get_text(),
            'add' : city,
            'addAdministrative' : AdministrativeString,
            'publish' : publishTime,
            'moneyLowest' : moneyTemp2[0],
            'moneyHighest': moneyTemp2[1],
            'experienceNeed' : need.get_text().split('\n')[2].split(' / ')[0],
            'degreeNeed': need.get_text().split('\n')[2].split(' / ')[1],
            'company' : company.get_text(),
            'Industry': EnterpriseCorrelationTemp[0],
            'Financing': EnterpriseCorrelationTemp[1],
            'NumberPerson': EnterpriseCorrelationTemp[2],
            'tag' :tagTemp,
            'fuli':fuliTemp
        }
        save_database(data, mongo_table)
        #数量加一
        datasum +=1

#保存数据库
def save_database(data, mongo_table):
    if db[mongo_table].insert_one(data):
        print('GET IT ---> ', data)

#清洗数据
def EnterpriseCorrelationData_cleaning(EnterpriseCorrelation):
    tempInformation = re.match(r'\n                    (.*?) / (.*?) / (.*?)\n                ', EnterpriseCorrelation, re.M | re.I)
    return tempInformation.groups()

def publish_Data_cleaning(publish):
    # 把几天前发布\12:00发布这种描述改成时间
    publishTimeTemp = publish.get_text()
    if publishTimeTemp.find('天前发布') == 1:
        publishTime = (date.today() + timedelta(days=-int(re.findall("\d+", publishTimeTemp)[0]))).strftime("%Y-%m-%d")
    elif publishTimeTemp.find('发布') == 5:
        publishTime = date.today().strftime("%Y-%m-%d")
    else:
        publishTime = publishTimeTemp
    return publishTime

def money_Data_cleaning(money):
    # K、k都有,统一并且分成最小值和最大值,还有xx以上，2k以下的数据
    moneyTemp = money.get_text().lower()
    if moneyTemp.find('以') != -1:
        moneyLowest,moneyHighest = re.findall(r"\d+", moneyTemp)[0]#出错了    moneyLowest,moneyHighest = re.findall(r"\d+", moneyTemp)[0]ValueError: not enough values to unpack (expected 2, got 1)

    else:
        moneyLowest = re.match(r'(.*?)k-(.*?)k', money.get_text().lower(), re.M | re.I).group(1)
        moneyHighest = re.match(r'(.*?)k-(.*?)k', money.get_text().lower(), re.M | re.I).group(2)
    moneyTemp2 = [moneyLowest,moneyHighest]
    return moneyTemp2

if __name__ == '__main__':
    #登录
    b.get('https://www.lagou.com/')
    b.maximize_window()
    input("start---->登录")

    #开始计时
    time_start = time.time()

    for condition in careerList:
        for city in cityRange:

            b.get('https://www.lagou.com/jobs/list_{}?city={}&cl=false&fromSearch=true&labelWords=&suginput='.format(condition,city))
            time.sleep(2)
            #拿区域值
            soupAdministratives = BeautifulSoup(b.page_source, 'lxml')
            Administratives = soupAdministratives.select('div:nth-child(1) > div.choose-detail > div > div:nth-child(2) > a')
            for Administrative in Administratives:
                AdministrativeString = Administrative.get_text()
                print('开始加载区域')
                if AdministrativeString != '不限':

                    # 设置存储位置
                    mongo_table = condition
                    client = pymongo.MongoClient(MONGO_URL, 27017)
                    db = client[MONGO_DB]

                    b.get('https://www.lagou.com/jobs/list_{}?px=default&city={}&district={}#filterBox'.format(condition,city,AdministrativeString))
                    time.sleep(1)
                    main(mongo_table)

                else:
                    print('跳过 不限')
                    # 跳过不限的选项



    print('完成！give me five! 运行时间为:',time.time() - time_start)
    print('获取职位数:{}'.format(datasum))
    b.quit()
#简化爬取的过程，容易出问题
#可以通过重启猫的方式，换ip。用sele登录tplink操作
#sele模拟登录，过验证码
#接口获取的方式
#https://blog.csdn.net/SvJr6gGCzUJ96OyUo/article/details/80544872
#def get_json(url,num):
   # '''''从网页获取JSON,使用POST请求,加上头部信息'''
   # my_headers = {
   #         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
   #          'Host':'www.lagou.com',
   #         'Referer':'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput=',
   #          'X-Anit-Forge-Code':'0',
   #         'X-Anit-Forge-Token': 'None',
   #         'X-Requested-With':'XMLHttpRequest'
   #         }
   #
   # my_data = {
   #         'first': 'true',
   #         'pn':num,
   #         'kd':'数据分析'}
   #
   # res = requests.post(url, headers = my_headers, data = my_data)
   # res.raise_for_status()
   # res.encoding = 'utf-8'
   # # 得到包含职位信息的字典
   # page = res.json()
   # return page

# 获取cookie
    # # 获取cookie并通过json模块将dict转化成str
    # dictCookies = b.get_cookies()
    # print(dictCookies)
    # jsonCookies = json.dumps(dictCookies)
    # # 登录完成后，将cookie保存到本地文件
    # with open('cookies.json', 'w') as f:
    #     f.write(jsonCookies)
    # # 初次建立连接，随后方可修改cookie
    # b.get('https://www.lagou.com/')
    # # 删除第一次建立连接时的cookie
    # b.delete_all_cookies()
    # # 读取登录时存储到本地的cookie
    # with open('cookies.json', 'r', encoding='utf-8') as f:
    #     listCookies = json.loads(f.read())
    # for cookie in listCookies:
    #     b.add_cookie({
    #         'domain': '.lagou.com',  # 此处xxx.com前，需要带点
    #         'name': cookie['name'],
    #         'value': cookie['value'],
    #         'path': '/',
    #         'expires': None
    #     })
    # # 再次访问页面，便可实现免登陆访问
    # b.get('https://www.lagou.com/')


# 储存到csv
# def work(number):
    # html = etree.HTML(b.page_source)
    # print('-----> 开始获取页面数据',)
    #
    # # 字段如下
    #
    # company = html.xpath('//*[@id="s_position_list"]/ul/li/@data-company')
    # positionName = html.xpath('//*[@id="s_position_list"]/ul/li/@data-positionname')
    # Salary = html.xpath('//*[@id="s_position_list"]/ul/li/@data-salary')
    # # Labels = html.xpath('//*[@id="s_position_list"]/ul/li/div[2]/div[1]/span[1]/text()')
    # Welfare = html.xpath('//*[@id="s_position_list"]/ul/li/div[2]/div[2]/text()')
    # EnterpriseInformation = html.xpath('//*[@id="s_position_list"]/ul/li/div[1]/div[2]/div[2]/text()')
    #
    # # 写入文件
    # # newline=空 就不会有空白行
    #
    # with open('crawl318.csv', 'a', encoding='utf-8',newline='') as csvfile:
    #     fieldnames = ['Company',
    #                   'positionName',
    #                   'Salary',
    #                   'AverageSalary',
    #                   'Labels',
    #                   'Welfare',
    #                   'classification',
    #                   'Financing',
    #                   'personsNumber'
    #                   ]
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     # 写入头信息
    #     if number == 0:
    #         writer.writeheader()
    #
    #     TempStatisticalAverage = 0
    #     # 长度取当前页一共多少行
    #     for i in range(len(company)):
    #         #统一k K
    #         Salarymini = Salary[i].lower()
    #         #获取月薪平均值
    #         SalaryTWO = re.match(r'(.*?)k-(.*?)k', Salarymini, re.M | re.I)
    #         averageSalary = round((int(SalaryTWO.group(2)) + int(SalaryTWO.group(1)))/2,1)
    #         #打印当前月薪和平均月薪
    #         TempStatisticalAverage += averageSalary
    #
    #         #处理‘企业服务,数据服务 / B轮 / 150-500人’-------分成三份
    #         tempInformation1 = EnterpriseInformation[i]
    #
    #         tempInformation = re.match(r'\n                    (.*?) / (.*?) / (.*?)\n                ', tempInformation1, re.M | re.I)
    #         classification = tempInformation.group(1)
    #         Financing = tempInformation.group(2)
    #         personsNumber = tempInformation.group(3)
    #         writer.writerow({'Company': company[i],
    #                          'positionName': positionName[i],
    #                          'Salary': Salarymini,
    #                          'AverageSalary': averageSalary,
    #                          # 'Labels':Labels[i],
    #                          'Welfare':Welfare[i],
    #                          'classification':classification,
    #                          'Financing':Financing,
    #                          'personsNumber':personsNumber
    #                          })

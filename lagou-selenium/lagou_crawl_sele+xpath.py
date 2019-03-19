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
from config import *
from bs4 import BeautifulSoup
import random
import time
'''
问题：
有些职位因为搜索条件相近，会重复，需要清洗
数据库，怎么分表？
基本把功能实现了，之后第一页的时候爬取二级目录，并且保存 上海这个层级

把内容拆开了 
把数据处理了下 时间与酬薪
 
'''


# open browser--两个地址
# path=r"C:\Users\white\AppData\Local\Google\Chrome\Application\chromedriver.exe"
path = "C:\Program Files\Tencent\QQBrowser\chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument()
# chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
b = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)

#执行爬取
def main(mongo_table):
    #最多三十个页面
    for number in range(0,31):
        parse_link(mongo_table)
        # sleep随机时间
        Interval = random.uniform(1, 2)
        time.sleep(Interval)

        #不是最后一页就继续下一页
        nextButton = b.find_element_by_class_name('pager_next')
        if nextButton.is_enabled() == True:
            nextButton.click()
            print('-----> 进入下一页')
        else:
            break

#分析及保存数据库
def parse_link(mongo_table):
        # if b.status_code == 404:#只能爬网页找这个结果
        #     pass
        # else:
            soup = BeautifulSoup(b.page_source, 'lxml')
            positions = soup.select('ul > li > div.list_item_top > div.position > div.p_top > a > h3')
            adds = soup.select('ul > li > div.list_item_top > div.position > div.p_top > a > span > em')
            publishs = soup.select('ul > li > div.list_item_top > div.position > div.p_top > span')
            moneys = soup.select('ul > li > div.list_item_top > div.position > div.p_bot > div > span')
            needs = soup.select('ul > li > div.list_item_top > div.position > div.p_bot > div')
            companys = soup.select('ul > li > div.list_item_top > div.company > div.company_name > a')
            tags = []
            if soup.find('div', class_='li_b_l'):
                tags = soup.select('ul > li > div.list_item_bot > div.li_b_l')
            fulis = soup.select('ul > li > div.list_item_bot > div.li_b_r')

            for position,add,publish,money,need,company,tag,fuli in \
					zip(positions,adds,publishs,moneys,needs,companys,tags,fulis):
                data = {
                    'position' : position.get_text(),
                    'add' : city + add.get_text(),
                    'publish' : publish.get_text(),
                    'money' : money.get_text(),
                    'need' : need.get_text().split('\n')[2],
                    'company' : company.get_text(),
                    'tag' : tag.get_text().replace('\n','-'),
                    'fuli' : fuli.get_text()
                }
                save_database(data, mongo_table)

#保存数据库
def save_database(data, mongo_table):
    if db[mongo_table].insert_one(data):
        print('GET IT ---> ', data)

if __name__ == '__main__':
    #登录
    b.get('https://www.lagou.com/')
    input("start---->登录")

    #开始计时
    time_start = time.time()

    for condition in careerList:
        for city in cityRange:

            b.get('https://www.lagou.com/jobs/list_{}?city={}&cl=false&fromSearch=true&labelWords=&suginput='.format(condition,city))
            #拿区域值
            soup = BeautifulSoup(b.page_source, 'lxml')
            Administratives = soup.select('filterCollapse > div:nth-child(1) > div.choose-detail > div > div:nth-child(2) > a')
            for Administrative in Administratives:
                AdministrativeString = Administrative.get_text()
                if AdministrativeString == '不限':
                    #跳过不限的选项
                    pass
                else:
                    #设置存储位置
                    mongo_table = condition
                    client = pymongo.MongoClient(MONGO_URL, MONGO_DB)
                    db = client[mongo_table]

                    b.get('https://www.lagou.com/jobs/list_{}?px=default&city={}&district={}#filterBox'.format(condition, city,AdministrativeString))
                    main(mongo_table)

    print('完成！give me five! 运行时间为',time.time() - time_start)

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

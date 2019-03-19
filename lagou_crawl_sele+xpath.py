# -*- coding: utf-8 -*-
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
# from config import *
from bs4 import BeautifulSoup
import random
import time
'''
问题：
有些职位因为搜索条件相近，会重复，需要清洗
数据库，怎么分表？
基本把功能实现了，之后第一页的时候爬取二级目录，并且保存 上海这个层级
'''
# open browser
path=r"C:\Users\white\AppData\Local\Google\Chrome\Application\chromedriver.exe"


chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument()
# chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
b = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)

def main(mongo_table):
    # #找到最大页数，了解要翻多少页
    # try:
    #     pagelist = b.find_elements_by_class_name('pager_not_current')
    #     pagemax = int(pagelist[-1].text)
    # except IndexError as e:
    #     print(e)

    for number in range(0,31):
        parse_link(mongo_table)
        # sleep 随机时间 再继续
        Interval = random.uniform(1, 2)
        time.sleep(Interval)

        #不是最后一页就继续下一页
        button = b.find_element_by_class_name('pager_next')
        if button.is_enabled() == True:
            button.click()
            print('-----> 进入下一页')
        else:
            break

        print('跳出循环了吗')

def parse_link(mongo_table):
        # if b.status_code == 404:
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
                    'add' : add.get_text(),
                    'publish' : publish.get_text(),
                    'money' : money.get_text(),
                    'need' : need.get_text().split('\n')[2],
                    'company' : company.get_text(),
                    'tag' : tag.get_text().replace('\n','-'),
                    'fuli' : fuli.get_text()
                }
                save_database(data, mongo_table)


def save_database(data, mongo_table):
    if db[mongo_table].insert_one(data):
        print('GET IT ---> ', data)

if __name__ == '__main__':
    careerlist = [
                  # '数据分析',
                  '数据挖掘',
                  '大数据',
                  '推荐算法',
                  '人工智能',
                  'pm',
                  '产品经理',
                  '交互设计',
                  'python',
                  'java',
                  'UI',
                  '运营',
                  '游戏策划',
                  ]
    #职位列表
    b.get('https://www.lagou.com/')
    input("start---->登录")
    #开始计时
    time_start = time.time()

    for condition in careerlist:
        mongo_table = 'lagou'
        # input url 后续改进为可选项或者传入一个字典
        b.get('https://www.lagou.com/jobs/list_' + condition + '?city=上海&cl=false&fromSearch=true&labelWords=&suginput=')
        client = pymongo.MongoClient('localhost', 27017)
        db = client[mongo_table]
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

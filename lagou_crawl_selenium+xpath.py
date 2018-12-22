import requests
import re
import time
from selenium import webdriver
from lxml import etree
import csv
from pyquery import PyQuery as pq
import time
import random
'''
问题：
有重复的内容
?有的时候没有登陆
最后一页没有获取到
pager_is_current是当前页
'''
# open browser
path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
b = webdriver.Chrome(executable_path=path, chrome_options=options)
# input url 后续改进为可选项或者传入一个字典


def work(number):
    html = etree.HTML(b.page_source)
    print('-----开始获取页面数据-----',)

    # turn

    result = html.xpath('//*[@id="s_position_list"]/ul/li/@data-company')
    result2 = html.xpath('//*[@id="s_position_list"]/ul/li/@data-positionname')
    Salary = html.xpath('//*[@id="s_position_list"]/ul/li/@data-salary')

    print(result,'\n',
          result2,'\n',
          Salary)

    # 写入文件
    # newline=空 就不会有空白行
    with open('UI_design.csv', 'a', encoding='utf-8',newline='') as csvfile:
        fieldnames = ['Title',
                      'Company',
                      'Salary',
                      'AverageSalary'
                      ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # 写入头信息
        if number == 0:
            writer.writeheader()
        for i in range(len(result)):
            #获取薪水均值
            Salarymini = Salary[i].lower()
            SalaryTWO = re.match(r'(.*?)k-(.*?)k', Salarymini, re.M | re.I)
            averageSalary = (int(SalaryTWO.group(2)) + int(SalaryTWO.group(1)))/2
            print(averageSalary)
            writer.writerow({'Title': result[i],
                             'Company': result2[i],
                             'Salary': Salarymini,
                             'AverageSalary': averageSalary
                             })

def main():
    b.get('https://www.lagou.com/jobs/list_UI?city=上海&cl=false&fromSearch=true&labelWords=&suginput=')
    #找到最大页数
    pagelist = b.find_elements_by_class_name('pager_not_current')

    pagemax = int(pagelist[-1].text)
    print('total : ',pagemax)
    for number in range(pagemax):
        #打印当前页
        CurrentPageArray = b.find_elements_by_class_name('pager_is_current')
        CurrentPage = CurrentPageArray[0].text
        print('当前页',int(CurrentPage))

        work(number)
        #sleep 随机时间 再继续
        Interval = random.uniform(2, 6)
        print('间隔:', Interval)
        time.sleep(Interval)



        #不是最后一页就继续下一页
        if number < pagemax:
            button = b.find_element_by_class_name('pager_next')
            button.click()
            print('-----进入下一页-----', )

if __name__ == '__main__':
    main()

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
通过hidefocus计算最后一页
<span hidefocus="hidefocus" page="11" class="pager_not_current">
    11
</span>
'''
# open browser
path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
b = webdriver.Chrome(executable_path=path, chrome_options=options)
# input url 后续改进为可选项或者传入一个字典
b.get('https://www.lagou.com/jobs/list_交互设计?city=上海&cl=false&fromSearch=true&labelWords=&suginput=')


def work(number):
    html = etree.HTML(b.page_source)
    print('-----> 开始获取页面数据',)

    # 字段如下

    company = html.xpath('//*[@id="s_position_list"]/ul/li/@data-company')
    positionName = html.xpath('//*[@id="s_position_list"]/ul/li/@data-positionname')
    Salary = html.xpath('//*[@id="s_position_list"]/ul/li/@data-salary')
    # Labels = html.xpath('//*[@id="s_position_list"]/ul/li/div[2]/div[1]/span[1]/text()')
    Welfare = html.xpath('//*[@id="s_position_list"]/ul/li/div[2]/div[2]/text()')
    EnterpriseInformation = html.xpath('//*[@id="s_position_list"]/ul/li/div[1]/div[2]/div[2]/text()')
    print('\n',company,
          '\n',positionName,
          '\n',Salary,
          # '\n', Labels,
          '\n', Welfare,
          '\n', EnterpriseInformation
          )

    # 写入文件
    # newline=空 就不会有空白行
    with open('jh.csv', 'a', encoding='utf-8',newline='') as csvfile:
        fieldnames = ['Company',
                      'positionName',
                      'Salary',
                      'AverageSalary',
                      'Labels',
                      'Welfare',
                      'classification',
                      'Financing',
                      'personsNumber'
                      ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # 写入头信息
        if number == 0:
            writer.writeheader()

        TempStatisticalAverage = 0
        # 长度取当前页一共多少行
        for i in range(len(company)):
            #统一k K
            Salarymini = Salary[i].lower()
            #获取月薪平均值
            SalaryTWO = re.match(r'(.*?)k-(.*?)k', Salarymini, re.M | re.I)
            averageSalary = round((int(SalaryTWO.group(2)) + int(SalaryTWO.group(1)))/2,1)
            #打印当前月薪和平均月薪
            TempStatisticalAverage += averageSalary
            print(averageSalary,'average',TempStatisticalAverage/(i+1))
            #处理‘企业服务,数据服务 / B轮 / 150-500人’-------分成三份
            tempInformation1 = EnterpriseInformation[i]
            print(tempInformation1)
            tempInformation = re.match(r'\n                    (.*?) / (.*?) / (.*?)\n                ', tempInformation1, re.M | re.I)
            classification = tempInformation.group(1)
            Financing = tempInformation.group(2)
            personsNumber = tempInformation.group(3)
            writer.writerow({'Company': company[i],
                             'positionName': positionName[i],
                             'Salary': Salarymini,
                             'AverageSalary': averageSalary,
                             # 'Labels':Labels[i],
                             'Welfare':Welfare[i],
                             'classification':classification,
                             'Financing':Financing,
                             'personsNumber':personsNumber
                             })

def main():

    #找到最大页数，了解要翻多少页
    pagelist = b.find_elements_by_class_name('pager_not_current')
    pagemax = int(pagelist[-1].text)
    print('total : ',pagemax)


    for number in range(pagemax):
        #打印当前页
        CurrentPageArray = b.find_elements_by_class_name('pager_is_current')
        CurrentPage = CurrentPageArray[0].text
        print('当前页',int(CurrentPage))

        # 爬取并写入本地
        work(number)


        #sleep 随机时间 再继续
        Interval = random.uniform(2, 6)
        print('间隔:', Interval,'s')
        time.sleep(Interval)



        #不是最后一页就继续下一页
        if number+1 < pagemax:
            button = b.find_element_by_class_name('pager_next')
            button.click()
            print('-----> 进入下一页', )

if __name__ == '__main__':
    main()

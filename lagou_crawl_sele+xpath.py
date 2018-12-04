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
有的时候没有登陆
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
b.get('https://www.lagou.com/jobs/list_数据分析?px=default&city=上海&district=浦东新区#filterBox.')


def work(number):
    html = etree.HTML(b.page_source)
    print('-----获取页面数据-----')

    # turn

    result = html.xpath('//*[@id="s_position_list"]/ul/li/@data-company')
    result2 = html.xpath('//*[@id="s_position_list"]/ul/li/@data-positionname')
    result3 = html.xpath('//*[@id="s_position_list"]/ul/li/@data-salary')
    print(result,
          result2,
          result3)

    # 写入文件
    # newline=空 就不会有空白行
    with open('data.csv', 'a', encoding='utf-8',newline='') as csvfile:
        fieldnames = ['Post',
                      'Company',
                      'Industry'
                      ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # 写入头信息
        if number == 1:
            writer.writeheader()
        for i in range(len(result)):
            writer.writerow({'Post': result[i],
                             'Company': result2[i],
                             'Industry': result3[i]})

def main():

    #找到最大页数
    pagelist = b.find_elements_by_class_name('pager_not_current')
    pagemax = int(pagelist[-1].text)
    for number in range(1,pagemax):
        work(number)
        Interval = random.uniform(0.5, 6)
        print('interval:', Interval)
        time.sleep(Interval)
    #不是最后一页就继续
        if number < pagemax:
            button = b.find_element_by_class_name('pager_next')
            button.click()


            # fieldnames = ['Post',
            #               'Company',
            #               # 'SalaryD',
            #               # 'SalaryU',
            #               # 'Experience',
            #               'Industry'
            #               # 'Financing',
            #               # 'Number',
            #               # 'sloga'
            #               ]
            # writer.writerow({'Post': result[0],
            #                  'Company': result2[0],
            #                  # 'SalaryD': SalaryD,
            #                  # 'SalaryU': SalaryU,
            #                  # 'Experience': positionAjax['workYear'],
            #                  'Industry': result3[0]
            #                  # 'Financing': positionAjax['financeStage'],
            #                  # 'Number': positionAjax['companySize'],
            #                  # 'sloga': positionAjax['positionAdvantage']
            #                 })

        # a = doc('.list_item_bot div')
        # for item in a.items():
        #     print(item.text())

        # # 拿到最低工资和最高工资
        # patternD = re.compile('(.*?)k-.*?', re.S)
        # SalaryD = re.findall(patternD, positionAjax['salary'].lower())
        # patternU = re.compile('.*?k-(.*?)', re.S)
        # SalaryU = re.findall(patternU, positionAjax['salary'].lower())

if __name__ == '__main__':
    main()

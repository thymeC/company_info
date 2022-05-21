from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import pandas as pd
import time
import re
from random import randint


chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)


def get_data_id(company):
    url = f'https://www.tianyancha.com/search?key={company}'

    driver.get(url)
    try:
        data_id = driver.find_element_by_class_name('search-result-single     ').get_attribute('data-id')
    except:
        pass
    return data_id


def get_info(id):
    driver.get(f'https://www.tianyancha.com/company/{id}')
    try:
        element_info = driver.find_element_by_css_selector("table[class='table -striped-col -breakall']")
    except:
        return ['','','','']
    company_content = element_info.text
    company_content = company_content.replace('\n', ' ')
    result = re.findall(r'企业类型\s(.*?)\s行业\s(.*?)\s.*参保人数\s(.*?)\s.*注册地址\s(.*?)\s', company_content.replace('\n', ' '))
    if not result:
        return ['','','','']
    return result[0]


def get_company_info_by_id(id):
    dict_info = {}
    info = get_info(id)
    dict_info['id'] = id
    dict_info['企业类型'] = info[0]
    dict_info['行业'] = info[1]
    dict_info['参保人数'] = info[2]
    dict_info['注册地址'] = info[3]

    return dict_info


def get_company_info(company):
    dict_info = {}
    dict_info['公司名称'] = company

    try:
        id = get_data_id(company)
    except:
        dict_info['id'] = 'id not found'
        return dict_info
    result = get_company_info_by_id(id)
    dict_info.update(result)

    return dict_info


if __name__ == '__main__':
    info = pd.read_excel('2.xls')
    companies = list(info['公司名称'])
    companies=companies[19:]
    final_info = []
    for company in companies:
        final_info.append(get_company_info(company))
        time.sleep(randint(1,15))

    # my_threadings = []
    # for company in companies:
    #     my_threading = multiThreadingRun(company, get_company_info, company)
    #     my_threading.start()
    #     my_threadings.append(my_threading)
    #
    # for my_threading in my_threadings:
    #     result = my_threading.get_result()
    #     final_info.append(result)

    df = pd.DataFrame(final_info)
    df.to_excel('final_info.xls')
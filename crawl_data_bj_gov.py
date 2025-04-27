import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta
import pandas as pd
import os
from dateutil.relativedelta import relativedelta

def get_data_from_web(url):
    """获取网页内容并解析"""
    response = requests.get(url)
    response.encoding = 'utf-8'  # 根据网页编码调整
    return BeautifulSoup(response.text, 'html.parser')

def extract_table_data(soup, title, date=None):
    """根据标题提取数据"""
    # 查找包含目标标题的元素
    target_element = soup.find('td',string=lambda text:  title in str(text))
    # print("target_element:",target_element)
    if not target_element:
        return None

    data = {}
    data['date']=date
    #获取对应的table
    current_table = target_element.parent.parent
    #提取对应的tr和td
    tr_list = current_table.find_all('tr')
    for i in range(1,len(tr_list)):
        td_list = tr_list[i].find_all('td')
        data[str.strip(td_list[0].text)[:-1]]=str.strip(td_list[1].text)
    
    # print(data)
    return data

def append_dict_to_csv(filename, data_dict):
    """
    将字典追加到CSV文件中，如果字典中的键不存在于CSV文件的列中，则新建列并设默认值为0。

    参数:
        filename (str): CSV文件的路径。
        data_dict (dict): 要追加的数据字典。
    """
    if not os.path.isfile(filename):
        # 如果文件不存在，创建一个新的DataFrame
        df = pd.DataFrame()
    else:
        # 尝试读取现有的CSV文件
        try:
            df = pd.read_csv(filename)
            if df.empty:
                 df = pd.DataFrame()
        except Exception as e:
            # 如果文件不存在，创建一个新的DataFrame
            df = pd.DataFrame()

    # 检查字典中的键是否在DataFrame的列中
    for key in data_dict:
        if key not in df.columns:
            # 如果列不存在，添加新列并设默认值为0
            df[key] = 0

    # 将字典转换为DataFrame
    # new_row = pd.DataFrame([data_dict])

    # 将新行追加到DataFrame
    df2 = pd.DataFrame([data_dict])
    df = pd.concat([df, df2])
    df = df[~df.duplicated(subset='date')]

    # 将更新后的内容写回CSV文件
    df.to_csv(filename, index=False)

# # 示例用法
# filename = 'example.csv'
# data = {'Name': 'John', 'Age': 30, 'City': 'New York'}
# append_dict_to_csv(filename, data)

def get_cur_date(date=None):
    if date:
        new_date=date;
    else:
        new_date = datetime.now().date() - timedelta(days=1)
    return new_date.strftime("%Y/%#m/%#d")
    
def month_format(month=None):
    if month:
        new_month=month;
    else:
        new_month = datetime.now().month() - timedelta(months=1)
    return new_month.strftime("%Y年%#m月")

def get_last_month():
    # 获取当前日期
    current_date = datetime.now()
    # 计算上个月的日期
    last_month_date = current_date - relativedelta(months=1)
    # 格式化日期为"YYYY-MM"格式
    last_month = last_month_date.strftime("%Y年%#m月")
    return last_month

def go_ahead():
    url = "http://bjjs.zjw.beijing.gov.cn/eportal/ui?pageId=307749"
    # url = "D:/liuyh/home-statistics/房地产数据主题服务-20250413.mhtml"
    soup = get_data_from_web(url)
    # print(soup)

    # 提取2025/4/20数据
    date =  get_cur_date()
    # date = "2025/4/13"
    target = date+"存量房网上签约"
    
    print("target:",target)
    data_date = extract_table_data(soup, target, date)
    print("data_date:",data_date)
    if data_date:
        append_dict_to_csv("date.csv", data_date)

    # 提取2025年3月数据
    month = get_last_month()
    # month = "2025年3月"
    target = month+"存量房网上签约"
    print("target:",target)
    data_month = extract_table_data(soup, target, month)
    print("data_month:",data_month)
    if data_month:
        append_dict_to_csv("month.csv", data_month)

go_ahead()
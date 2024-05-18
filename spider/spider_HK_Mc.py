import os

import mysql.connector
import pymysql
import requests
from lxml import etree
import opencc
import random


class ChineseConverter:
    def __init__(self):
        # Create a converter object
        self.converter = opencc.OpenCC('t2s.json')  # Use 't2s.json' for Traditional to Simplified Chinese conversion

    def convert_to_simplified(self, traditional_text):
        # Convert Traditional Chinese to Simplified Chinese
        simplified_text = self.converter.convert(traditional_text)
        return simplified_text

    def convert_text(self, text):
        # Convert the provided text from Traditional to Simplified Chinese
        simplified_text = self.convert_to_simplified(text)
        return simplified_text


convert = ChineseConverter()
headers = {
    'authority': 'mcdonalds.com.hk',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'cookie': '_fbp=fb.2.1703730332669.1418492709; _gcl_au=1.1.1072263701.1703730333; _ga=GA1.1.588479614.1703730333; pll_language=tc; _fw_crm_v=93092126-aca4-484c-c6c8-ca4993d7f8ac; _uetvid=ee4b40e0a54911eeaf0eddbb8d095eee; _ga_ME45GQVQ4S=GS1.1.1704250706.9.1.1704250727.0.0.0; _ga_6ZRVDTPHBF=GS1.1.1704250706.9.1.1704250727.0.0.0',
    'pragma': 'no-cache',
    'referer': 'https://mcdonalds.com.hk/',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}


def save_file_from_url(url, filename):
    """
    保存二进制文件到本机
    :param url: 二进制文件所在url
    :param filename: 保存路径
    :return:
    """
    response = requests.get(url)

    # 获取目录路径
    directory = os.path.dirname(filename)

    # 如果目录不存在，则创建目录
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(filename, 'wb') as file:
        file.write(response.content)
        print(f"{filename} 已成功保存到本地")


def insert_offers_data(img_path, simplified_title, simplified_details):
    cursor = None
    conn = None
    try:
        # 连接数据库
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="azure",
            database="order_system"
        )

        # 创建游标对象
        cursor = conn.cursor()

        # 定义插入数据到表中的SQL查询
        insert_query = """
            INSERT INTO latest_offers (img_path, simplified_title, simplified_details)
            VALUES (%s, %s, %s)
        """

        # 定义要插入的数据
        data = (img_path, simplified_title, simplified_details)

        # 执行查询
        cursor.execute(insert_query, data)

        # 提交更改到数据库
        conn.commit()

        print("数据插入成功。")

    except mysql.connector.Error as err:
        print(f"插入数据时出错: {err}")

    finally:
        # 关闭游标和连接
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


def insert_packages_data(img_path, simplified_title, price, discount):
    cursor = None
    conn = None
    try:
        # 连接数据库
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="azure",
            database="order_system"
        )

        # 创建游标对象
        cursor = conn.cursor()

        # 定义插入数据到表中的SQL查询
        insert_query = """
            INSERT INTO affordable_packages (img_path, simplified_title, price, discount)
            VALUES (%s, %s, %s, %s)
        """

        # 定义要插入的数据
        data = (img_path, simplified_title, price, discount)

        # 执行查询
        cursor.execute(insert_query, data)

        # 提交更改到数据库
        conn.commit()

        print("数据插入成功。")

    except mysql.connector.Error as err:
        print(f"插入数据时出错: {err}")

    finally:
        # 关闭游标和连接
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


def crawl_latest_offers():
    response = requests.get('https://mcdonalds.com.hk/latest-promotions/', headers=headers)
    if response.status_code != 200:
        print(f"请求失败: {response}")

    path = "../res/McDonald_offers"
    tree = etree.HTML(response.text)
    div_list = tree.xpath(".//div[@class='page_item section_item flex_block_item flex_item_2 ']")
    for div in div_list:
        img = div.xpath(".//div[@class='img_container']/img[@class=' mobile_item']/@src")[0]
        title = div.xpath(".//div[@class='text_container']/h3[@class='item_title font_bold']/a/text()")[0]
        simplified_title = convert.convert_text(title).replace(' ', '').replace('\n', '')
        details = div.xpath(".//div[@class='text_container']/div[@class='item_content']/text()")[0]
        simplified_details = convert.convert_text(details)
        file_name = path + "/" + simplified_title + "." + img.split('.')[-1]

        # 保存数据到本地和数据库
        save_file_from_url(img, file_name)
        insert_offers_data(file_name, simplified_title, simplified_details)


def crawl_affordable_packages(url):
    response = requests.get(url=url, headers=headers)
    if response.status_code != 200:
        print(f"请求失败: {response}")
    path = "../res/McDonald_packages"
    tree = etree.HTML(response.text)

    # 开始解析
    div_list = tree.xpath(".//div[@class='menu_category_item flex_item_3']")
    for div in div_list:
        img = div.xpath(".//div[@class='img_container']/img/@src")[0]
        title = div.xpath(".//h5[@class='item_name size_20']/text()")[0].replace(" ", "").replace("\n", "").replace("\t", "")
        simplified_title = convert.convert_text(title)

        file_name = path + "/" + simplified_title + "." + img.split(".")[-1]
        save_file_from_url(img, file_name)

        # 生成80到100之间的随机小数
        random_price = round(random.uniform(80, 100), 2)
        random_discount = round(random.uniform(8, 10), 2)
        insert_packages_data(file_name, simplified_title, random_price, random_discount)


if __name__ == '__main__':
    url_list = ["https://mcdonalds.com.hk/menu/extra-value-meals/"
                "https://mcdonalds.com.hk/menu/extra-value-breakfasts/",
                "https://mcdonalds.com.hk/menu/happy-meals/",
                "https://mcdonalds.com.hk/menu/breakfast-platter-and-twisty-pasta/",
                "https://mcdonalds.com.hk/menu/salads/",
                ]
    for url in url_list:
        crawl_affordable_packages(url)

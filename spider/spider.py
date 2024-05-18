import mysql
import requests
from lxml import etree
import os
import mysql.connector

cookies = {
    'Adshow': '1',
    'ARRAffinity': '405b00e52edc478a3f3060dbac48b5f317a4bcc0eba6362aa633afdb6d0c99f9',
    'ARRAffinitySameSite': '405b00e52edc478a3f3060dbac48b5f317a4bcc0eba6362aa633afdb6d0c99f9',
    '_ga': 'GA1.3.1455650711.1704074430',
    '_gid': 'GA1.3.34712414.1704074430',
    'sajssdk_2015_cross_new_user': '1',
    '_gat': '1',
    '_gat_UA-49420844-1': '1',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2218cc2c0470d46b-09e1b4d81e34f-26031051-1395396-18cc2c0470e1b0d%22%2C%22%24device_id%22%3A%2218cc2c0470d46b-09e1b4d81e34f-26031051-1395396-18cc2c0470e1b0d%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D',
    '_ga_H0FLFLQXE1': 'GS1.3.1704074430.1.1.1704074906.39.0.0',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://www.mcdonalds.com.cn/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
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


def insert_menu_data(menu_name, category_name, cover_path):
    # 连接数据库
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="azure",
        database="order_system"
    )

    # 创建游标对象
    cursor = conn.cursor()

    # 查询category_id
    select_category_id_query = "SELECT category_id FROM dishcategory WHERE category_name = %s"
    cursor.execute(select_category_id_query, (category_name,))
    category_id = cursor.fetchone()

    if category_id:
        # 获取当前最大的menu_id值
        query_max_menu_id = "SELECT MAX(menu_id) FROM menu"
        cursor.execute(query_max_menu_id)
        max_menu_id = cursor.fetchone()[0]

        if max_menu_id is not None:
            menu_id = max_menu_id + 1
        else:
            # 如果没有记录，初始 menu_id 为 1
            menu_id = 1

        # 插入数据到menu表
        insert_menu_query = "INSERT INTO menu (`menu_id`, `menu_name`, `category_id`, `cover_path`) VALUES (%s, %s, %s, %s)"
        menu_values = (menu_id, menu_name, category_id[0], cover_path)

        cursor.execute(insert_menu_query, menu_values)
        conn.commit()
        print("数据插入成功!")
    else:
        print("未找到对应的category_id")

    # 关闭连接
    cursor.close()
    conn.close()


def craw_all_category(url):
    """
    爬取所有的菜单
    :param url:
    :return:
    """
    response = requests.get(url, headers=headers, cookies=cookies)
    tree = etree.HTML(response.text)

    category_name = tree.xpath("/html/body/div[1]/section[1]/div[3]/div/div/div/div[1]/h3/text()")[0]
    div_list = tree.xpath("/html/body/div[1]/section[1]/div[3]/div/div/div/div[2]/div/div")
    file_path = f"../res/McDonald/{category_name}"
    for div in div_list:
        menu_name = div.xpath(".//span[@class='name']/text()")[0]
        pic_src = div.xpath(".//div[@class='pic']/img/@src")[0]
        file_name = f"{file_path}/{menu_name}.{pic_src.split('.')[-1]}"

        save_file_from_url(pic_src, file_name)

        insert_menu_data(menu_name, category_name, file_name)




if __name__ == '__main__':
    categories = ["hamburgers", "beverage", "Snacks", "desserts", "Breakfast-26", "500大卡套餐-2", "Happy-Meal-Items-2"]
    for category in categories:
        url = f"https://www.mcdonalds.com.cn/product/mcdonalds/{category}"
        craw_all_category(url)

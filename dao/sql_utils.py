from datetime import datetime

import mysql.connector

from common.user import User


class DatabaseConnector:
    """
    此类用于连接数据库
    """
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("成功连接到 MySQL 数据库")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            # 如果连接失败，可以选择抛出异常或进行其他处理

    def connect(self):
        """
        建立数据库连接
        :return: None
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("成功建立数据库连接")
        except mysql.connector.Error as err:
            print(f"数据库连接失败: {err}")

    def execute_query(self, query, data=None):
        """
        执行响应的查询语句
        :param query: sql语句模板
        :param data: 需要填充的数据
        :return:
        """
        try:
            self.cursor.execute(query, data)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"查询语句执行成功: {err}")
            return None

    def execute_update(self, query, data=None):
        """
        执行响应的更新语句
        :param query: sql语句模板
        :param data: 需要填充的数据
        :return:
        """
        try:
            self.cursor.execute(query, data)
            self.connection.commit()
            print("更新语句执行成功")
        except mysql.connector.Error as err:
            print(f"更新执行错误: {err}")
            self.connection.rollback()

    def disconnect(self):
        """
        断开数据库连接
        :return: None
        """
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("成功断开数据库连接")


class UserManager:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def register_user(self, username, password, realname, gender, birthday, email, phone_number):
        # 检查用户名是否已存在
        if self.is_username_taken(username):
            print("Username already taken. Please choose another one.")
            return False

        # 将用户信息插入数据库
        insert_query = """
            INSERT INTO User (user_name, user_password, user_realname, user_gender, user_birthday, user_email, phone_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        user_data = (username, password, realname, gender, birthday, email, phone_number)

        try:
            self.db_connector.execute_update(insert_query, user_data)
            print("User registration successful.")
            return True
        except mysql.connector.Error as err:
            print(f"Error registering user: {err}")
            return False

    def modify_user_info(self, username, new_realname, new_gender, new_birthday, new_email, new_phone_number):
        if not self.is_email_registered(new_email):
            print("请输入正确的邮箱!!!")
            return False
        update_query = """
            UPDATE user
            SET user_realname = %s, user_gender = %s, user_birthday = %s, phone_number = %s, user_name = %s
            WHERE user_email = %s
        """
        update_data = (new_realname, new_gender, new_birthday, new_phone_number, username, new_email)

        try:
            self.db_connector.execute_update(update_query, update_data)
            print("User information modification successful.")
            return True
        except mysql.connector.Error as err:
            print(f"Error modifying user information: {err}")
            return False

    def change_password(self, email, new_password):
        if not self.is_email_registered(email):
            print("Email not found. Unable to change password.")
            return False

        # Update the user's password in the database
        update_query = """
            UPDATE user
            SET user_password = %s
            WHERE user_email = %s
        """
        update_data = (new_password, email)

        try:
            self.db_connector.execute_update(update_query, update_data)
            print("Password change successful.")
            return True
        except mysql.connector.Error as err:
            print(f"Error changing password: {err}")
            return False

    def is_email_registered(self, email) -> bool:
        # 检查邮箱是否已经注册
        check_query = """
            SELECT COUNT(*)
            FROM user
            WHERE user_email = %s
        """
        check_data = (email,)

        result = self.db_connector.execute_query(check_query, check_data)

        if result and len(result) > 0:
            return result[0][0] > 0
        else:
            return False

    def login_user(self, email, password):
        # 检查邮箱和密码是否匹配
        query = "SELECT * FROM User WHERE user_email = %s AND user_password = %s"
        result = self.db_connector.execute_query(query, (email, password))

        if result:
            # 如果查询成功，构建 User 对象并返回
            user_info = result[0]  # 假设只有一个匹配的用户
            user = User(email, password)
            user.user_id = user_info[0]
            user.user_name = user_info[1]
            user.user_realname = user_info[3]
            user.user_gender = user_info[4]
            user.user_birthday = user_info[5]
            user.phone_number = user_info[7]
            user.orders = self.get_user_orders_with_details(user_info[0])
            print("Login successful")
            return user
        else:
            print("Invalid email or password.")
            return None

    def show_menu_by_category(self):
        # 查询所有菜品的种类
        query_categories = "SELECT DISTINCT category_name FROM DishCategory"
        categories = self.db_connector.execute_query(query_categories)

        # 查询每个种类的菜单信息
        menu_dict = {}
        for category in categories:
            category_name = category[0]
            query_menu = """
                SELECT *
                FROM Menu m
                JOIN DishCategory dc ON m.category_id = dc.category_id
                WHERE dc.category_name = %s
            """
            menu_data = self.db_connector.execute_query(query_menu, (category_name,))
            menu_dict[category_name] = [dish_info for dish_info in menu_data]

        # 打印菜单字典
        # if menu_dict:
        #     print("菜单字典：")
        #     for category, menu in menu_dict.items():
        #         print(f"{category} 菜单： {menu}")
        # else:
        #     print("菜单字典为空。")

        return menu_dict

    def is_username_taken(self, username):
        # 检查用户名是否已存在
        query = "SELECT user_id FROM User WHERE user_name = %s"
        result = self.db_connector.execute_query(query, (username,))
        return bool(result)

    def show_merchant_info(self, merchant_id):
        # 查询商家信息
        query = "SELECT * FROM Merchant WHERE merchant_id = %s"
        merchant_info = self.db_connector.execute_query(query, (merchant_id,))

        # 打印商家信息
        if merchant_info:
            print("商家信息：")
            print(f"商家ID: {merchant_info[0][0]}")
            print(f"商家名称: {merchant_info[0][1]}")
            print(f"商家地址: {merchant_info[0][2]}")
            print(f"商家联系方式: {merchant_info[0][3]}")
            print(f"所属餐厅ID: {merchant_info[0][4]}")
        else:
            print("未找到该商家。")

    def is_user_exist(self, user_id):
        query = "SELECT * FROM User WHERE user_id = %s"
        result = self.db_connector.execute_query(query, (user_id,))
        return bool(result)

    def is_merchant_exist(self, merchant_id):
        query = "SELECT * FROM Merchant WHERE merchant_id = %s"
        result = self.db_connector.execute_query(query, (merchant_id,))
        return bool(result)

    def is_dish_exist(self, dish_id):
        query = "SELECT * FROM Menu WHERE menu_id = %s"
        result = self.db_connector.execute_query(query, (dish_id,))
        return bool(result)

    def place_order(self, user_id, merchant_id, dish_id):
        # 检查用户是否存在
        if not self.is_user_exist(user_id):
            print("用户不存在。")
            return

        # 检查商家是否存在
        if not self.is_merchant_exist(merchant_id):
            print("商家不存在。")
            return

        # 检查菜品是否存在
        if not self.is_dish_exist(dish_id):
            print("菜品不存在。")
            return

        # 获取当前时间作为下单时间
        order_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 获取当前最大的order_id值
        query_max_order_id = "SELECT MAX(order_id) FROM OrderTable"
        max_order_id = self.db_connector.execute_query(query_max_order_id)[0][0]

        # 插入订单数据，手动为order_id提供唯一值
        query = "INSERT INTO OrderTable (order_id, user_id, merchant_id, dish_id, order_time, order_status) VALUES (%s, %s, %s, %s, %s, %s)"
        order_status = "已下单"
        self.db_connector.execute_query(query, (max_order_id + 1, user_id, merchant_id, dish_id, order_time, order_status))

        print("下单成功。")

    def view_order_status(self, user_id):
        # 查询用户的所有订单信息
        query = "SELECT * FROM OrderTable WHERE user_id = %s"
        orders = self.db_connector.execute_query(query, (user_id,))

        # 打印订单状态信息
        if orders:
            print("订单状态信息：")
            for order in orders:
                print(f"订单ID: {order[0]}")
                print(f"商家ID: {order[2]}")
                print(f"菜品ID: {order[3]}")
                print(f"下单时间: {order[4]}")
                print(f"订单状态: {order[5]}")
                print("--------------------")
        else:
            print("您还没有下过单。")

    def update_order_status(self, order_id, new_status):
        # 检查订单是否存在
        query_check_order = "SELECT * FROM OrderTable WHERE order_id = %s"
        existing_order = self.db_connector.execute_query(query_check_order, (order_id,))
        if not existing_order:
            print("订单不存在。")
            return

        # 更新订单状态
        query_update_status = "UPDATE OrderTable SET order_status = %s WHERE order_id = %s"
        self.db_connector.execute_query(query_update_status, (new_status, order_id))

        print("订单状态更新成功。")

    def view_coupons(self, user_id):
        # 查询用户的所有优惠券信息
        query = "SELECT * FROM Coupon WHERE user_id = %s AND expiration_date >= CURDATE()"
        coupons = self.db_connector.execute_query(query, (user_id,))

        # 打印可用的优惠券信息
        if coupons:
            print("可用的优惠券信息：")
            for coupon in coupons:
                print(f"优惠券ID: {coupon[0]}")
                print(f"商家ID: {coupon[2]}")
                print(f"优惠券类型: {coupon[3]}")
                print(f"折扣金额: {coupon[4]}")
                print(f"过期日期: {coupon[5]}")
                print("--------------------")
        else:
            print("您暂时没有可用的优惠券。")

    def use_coupon(self, user_id, coupon_id):
        # 检查优惠券是否存在且未过期
        query_check_coupon = "SELECT * FROM Coupon WHERE coupon_id = %s AND user_id = %s AND expiration_date >= CURDATE()"
        existing_coupon = self.db_connector.execute_query(query_check_coupon, (coupon_id, user_id))
        if not existing_coupon:
            print("优惠券不存在或已过期。")
            return

        # 获取优惠券信息
        coupon_info = existing_coupon[0]
        merchant_id = coupon_info[2]
        discount_type = coupon_info[3]
        discount_amount = coupon_info[4]

        # 在下单时应用优惠券（此处仅作演示，实际情况可能需要更复杂的逻辑）
        # 这里假设将优惠券信息存储在订单表中
        query_apply_coupon = "UPDATE OrderTable SET discount_type = %s, discount_amount = %s WHERE user_id = %s AND merchant_id = %s AND order_status = '已下单'"
        self.db_connector.execute_query(query_apply_coupon, (discount_type, discount_amount, user_id, merchant_id))

        print("优惠券使用成功。")

    def leave_review(self, user_id, merchant_id, rating, review_content):
        # 检查用户是否存在
        if not self.is_user_exist(user_id):
            print("用户不存在。")
            return

        # 检查商家是否存在
        if not self.is_merchant_exist(merchant_id):
            print("商家不存在。")
            return

        # 获取当前时间作为评价时间
        review_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 获取当前最大的review_id值
        query_max_review_id = "SELECT MAX(review_id) FROM UserReview"
        max_review_id = self.db_connector.execute_query(query_max_review_id)[0][0]

        # 插入用户评价数据，手动为review_id提供唯一值
        query = "INSERT INTO UserReview (review_id, user_id, merchant_id, rating, review_content, review_time) VALUES (%s, %s, %s, %s, %s, %s)"
        self.db_connector.execute_query(query, (max_review_id + 1, user_id, merchant_id, rating, review_content, review_time))

        print("评价成功。")

    def view_delivery_status(self, order_id):
        # 查询订单的配送信息
        query = "SELECT * FROM Delivery WHERE order_id = %s"
        delivery_info = self.db_connector.execute_query(query, (order_id,))

        # 打印配送信息，用于调试
        print("配送信息：", delivery_info)

        # 检查是否有配送信息
        if not delivery_info:
            print("订单配送信息不存在。")
            return

        # 提取唯一的元组
        delivery_info_tuple = delivery_info[0]

        # 打印配送状态信息
        print("配送状态信息：")
        print(f"订单ID: {delivery_info_tuple[0]}")
        print(f"配送地址: {delivery_info_tuple[2]}")
        print(f"配送员ID: {delivery_info_tuple[3]}")
        print(f"配送状态: {delivery_info_tuple[4]}")

    def update_delivery_status(self, order_id, new_status):
        # 检查订单是否存在
        query_check_order = "SELECT * FROM OrderTable WHERE order_id = %s"
        existing_order = self.db_connector.execute_query(query_check_order, (order_id,))
        if not existing_order:
            print("订单不存在。")
            return

        # 检查订单是否已完成（如果已完成，则不允许更新配送状态）
        if existing_order[0][5] == "已完成":
            print("订单已完成，不允许更新配送状态。")
            return

        # 检查配送状态是否合法（可根据实际需求进行进一步验证）
        allowed_statuses = ["已派送", "配送中", "已送达"]
        if new_status not in allowed_statuses:
            print("无效的配送状态。")
            return

        # 获取当前时间作为更新时间
        update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 更新配送状态，去掉与update_time相关的代码
        query_update_status = "UPDATE Delivery SET delivery_status = %s WHERE order_id = %s"
        self.db_connector.execute_query(query_update_status, (new_status, order_id))

        print("配送状态更新成功。")

    def record_merchant_login(self, user_id, merchant_id):
        # 检查用户是否存在
        if not self.is_user_exist(user_id):
            print("用户不存在。")
            return

        # 检查商家是否存在
        if not self.is_merchant_exist(merchant_id):
            print("商家不存在。")
            return

        # 获取当前时间作为登录时间
        login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 获取当前最大的record_id值
        query_max_record_id = "SELECT MAX(record_id) FROM UserMerchantLogin"
        max_record_id = self.db_connector.execute_query(query_max_record_id)[0][0]

        # 插入商家登录信息，手动为record_id提供唯一值
        query = "INSERT INTO UserMerchantLogin (record_id, user_id, merchant_id, login_time) VALUES (%s, %s, %s, %s)"
        self.db_connector.execute_query(query, (max_record_id + 1, user_id, merchant_id, login_time))

        print("商家登录记录成功。")

    def query_order_history(self, user_id=None, merchant_id=None, status=None):
        # 构建查询订单历史记录的SQL语句
        query = "SELECT * FROM OrderTable WHERE 1"

        # 用于存储查询参数的列表
        query_params = []

        # 添加用户ID作为筛选条件
        if user_id is not None:
            query += " AND user_id = %s"
            query_params.append(user_id)

        # 添加商家ID作为筛选条件
        if merchant_id is not None:
            query += " AND merchant_id = %s"
            query_params.append(merchant_id)

        # 添加订单状态作为筛选条件
        if status is not None:
            query += " AND order_status = %s"
            query_params.append(status)

        # 执行查询
        if query_params:
            # 仅在提供了至少一个筛选条件时执行查询
            orders = self.db_connector.execute_query(query, tuple(query_params))
            return orders
        else:
            print("请提供至少一个筛选条件。")
            return []

    def query_merchant_reviews(self, merchant_id):
        # 构建查询商家评价的SQL语句
        query = "SELECT * FROM UserReview WHERE merchant_id = %s"

        # 执行查询
        reviews = self.db_connector.execute_query(query, (merchant_id,))

        # 返回商家收到的所有评价
        return reviews

    def insert_order(self, user_name, restaurant_name, order_status, order_amount):
        try:
            # Connect to the database
            self.db_connector.connect()

            # Get user and restaurant IDs
            user_id_query = "SELECT user_id FROM user WHERE user_name = %s"
            user_id = self.db_connector.execute_query(user_id_query, (user_name,))
            user_id = user_id[0][0] if user_id else None

            restaurant_id_query = "SELECT restaurant_id FROM restaurant WHERE restaurant_name = %s"
            restaurant_id = self.db_connector.execute_query(restaurant_id_query, (restaurant_name,))
            restaurant_id = restaurant_id[0][0] if restaurant_id else None

            if user_id is not None and restaurant_id is not None:
                # Insert order information
                order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                insert_order_query = "INSERT INTO orders (user_id, restaurant_id, order_time, order_status, order_amount) VALUES (%s, %s, %s, %s, %s)"
                order_data = (user_id, restaurant_id, order_time, order_status, order_amount)
                self.db_connector.execute_update(insert_order_query, order_data)
                print("Order inserted successfully")
            else:
                print("User or restaurant not found")

        except Exception as e:
            print(f"Error: {e}")

    def get_user_orders_with_details(self, user_id):
        try:
            get_orders_query = """
                SELECT o.order_id, u.user_name, r.restaurant_name, o.order_time, o.order_status, o.order_amount
                FROM orders o
                JOIN user u ON o.user_id = u.user_id
                JOIN restaurant r ON o.restaurant_id = r.restaurant_id
                WHERE o.user_id = %s
            """
            orders = self.db_connector.execute_query(get_orders_query, (user_id,))
            return orders
        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Disconnect from the database
            self.db_connector.disconnect()

    def load_restaurants(self):
        # 执行SQL查询
        query = "SELECT * FROM restaurant"

        with self.db_connector.connection.cursor() as cursor:
            cursor.execute(query)
            # 获取查询结果
            restaurants = cursor.fetchall()

        result = {}
        for restaurant in restaurants:
            result[restaurant[1]] = restaurant
        return result

    def get_all_offers(self) -> dict:
        select_query = """
            SELECT id, img_path, simplified_title, simplified_details, price, discount
            FROM latest_offers
        """

        try:
            cursor = self.db_connector.connection.cursor(dictionary=True)
            cursor.execute(select_query)

            offers_dict = {}
            for row in cursor.fetchall():
                simplified_title = row['simplified_title']
                offers_dict[simplified_title] = row

            return offers_dict

        except mysql.connector.Error as err:
            print(f"Error fetching offers: {err}")
            return None

    def get_all_packages(self) -> dict:
        select_query = """
            SELECT id, img_path, simplified_title, price, discount
            FROM affordable_packages
        """

        try:
            cursor = self.db_connector.connection.cursor(dictionary=True)
            cursor.execute(select_query)

            offers_dict = {}
            for row in cursor.fetchall():
                simplified_title = row['simplified_title']
                offers_dict[simplified_title] = row

            return offers_dict

        except mysql.connector.Error as err:
            print(f"Error fetching offers: {err}")
            return None


# 示例用法
# 替换以下参数为你的数据库信息
if __name__ == '__main__':
    host = "localhost"
    user = "root"
    password = "azure"
    database = "order_system"

    # 创建数据库连接对象
    db_connector = DatabaseConnector(host, user, password, database)

    # 创建用户管理对象
    user_manager = UserManager(db_connector)

    # user_manager.modify_user_info("existing_username", "azure", "1", "1990-01-01", "azure@example.com", "1234567890")
    packages_dict = user_manager.get_all_packages()
    print(packages_dict)
    db_connector.disconnect()

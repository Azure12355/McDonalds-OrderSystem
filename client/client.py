from common.user import User
from dao.sql_utils import UserManager, DatabaseConnector


class Client:

    def __init__(self):
        self.dbConnector = DatabaseConnector("localhost", "root", "azure", "mcdonald_ordersystem")
        self.userManager = UserManager(self.dbConnector)

    def getAllDishes(self) -> dict:
        """
        获取所有的菜单
        :return: {category: dishes}
        """
        return self.userManager.show_menu_by_category()

    def getAllRestaurant(self) -> dict:
        """
        获取所有的餐厅
        :return: {name: address}
        """
        return self.userManager.load_restaurants()

    def uploadOrder(self, userName, restaurantName, order_status, order_amount):
        """
        上传订单
        :param userName: 用户名
        :param restaurantName: 餐厅名
        :param order_status: 订单状态
        :param order_amount: 订单金额
        :return:
        """
        self.userManager.insert_order(userName, restaurantName, order_status, order_amount)

    def login(self, emil, pwd):
        """
        用户登录
        :param emil: 邮箱
        :param pwd: 密码
        :return: 用户对象
        """
        return self.userManager.login_user(emil, pwd)

    def register(self, username, password, realname, gender, birthday, email, phone_number):
        return self.userManager.register_user(username, password, realname, gender, birthday, email, phone_number)

    def getOrders(self, user: User):
        """
        获取指定用户的订单信息
        :param user: 用户
        :return: {用户名: [订单信息1, 订单信息2]}
        """
        user.orders = self.userManager.get_user_orders_with_details(user.user_id)

    def changePassword(self, email, new_password) -> bool:
        """
        修改密码
        :param email: 邮箱
        :param new_password: 新密码
        :return: 是否成功修改
        """
        return self.userManager.change_password(email, new_password)

    def updatePersonalInfo(self, email, user_name, new_realname, new_gender, new_birthday, new_phone_number) -> bool:
        """
        更新用户个人信息
        :param email: 邮箱
        :param user_name: 用户名
        :param new_realname: 真实姓名
        :param new_gender: 性别
        :param new_birthday: 生日
        :param new_phone_number: 电话
        :return: 是否成功修改
        """
        return self.userManager.modify_user_info(
            username=user_name,
            new_realname=new_realname,
            new_gender=new_gender,
            new_birthday=new_birthday,
            new_email=email,
            new_phone_number=new_phone_number
        )

    def getAllOffers(self) -> dict:
        """
        读取所有的优惠菜品
        :return: 返回 {优惠彩屏:{字段:详情},}
        """
        return self.userManager.get_all_offers()

    def getAllPackages(self) -> dict:
        """
        读取所有的套餐
        :return: 返回 {套餐名:{套餐字段:详情},}
        """
        return self.userManager.get_all_packages()


if __name__ == '__main__':
    client = Client()
    dish_map = client.getAllDishes()
    print(dish_map)

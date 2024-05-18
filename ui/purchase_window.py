from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QDialog, QLabel, QLineEdit, QScrollArea, QButtonGroup, \
    QMessageBox, QHBoxLayout, QComboBox, QSizePolicy, QToolButton

from client.client import Client
from common.user import User
from utils.utils import Utils


class PurchaseWindow(QDialog):
    def __init__(self, dishesMap: dict, user: User):
        super().__init__()
        self.setFixedSize(500, 700)
        # 设置整体垂直布局
        main_layout = QVBoxLayout()

        self.setWindowTitle("支付")
        icon = QIcon("../res/images/images (8).png")
        self.setWindowIcon(icon)

        # 餐厅信息
        self.restaurant_info = RestaurantInfo()
        # 将餐厅信息部分添加到垂直布局中
        main_layout.addWidget(self.restaurant_info)

        # 购物订单信息
        self.shopping_order_info = OrderInfo(dishesMap)
        main_layout.addWidget(self.shopping_order_info)

        # 用户信息
        self.user = user

        # 商品总价格
        total_price_label = QLabel('总计:')
        total_price_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        total_price_label.setObjectName("total_price_label")
        price_amount_label = QLabel("{:.2f}".format(self.shopping_order_info.total_price))
        price_amount_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        price_amount_label.setObjectName("price_amount")

        # 支付订单信息
        self.payment_info = {"user_name": self.user.user_name,
                             "restaurant_name": self.restaurant_info.restaurant_combo.currentText(),
                             "order_status": "已完成",
                             "order_amount": "{:.2f}".format(self.shopping_order_info.total_price)}

        # 支付按钮
        payment_button = QPushButton('支付', self)
        payment_button.setObjectName("payment_btn")
        payment_button.clicked.connect(self.show_payment_window)
        payment_button.setFixedHeight(50)

        payment_widget = QWidget()
        payment_widget.setObjectName("payment_widget")
        payment_widget.setFixedSize(460, 50)

        layout1 = QHBoxLayout(payment_widget)
        layout1.addWidget(total_price_label, 1)
        layout1.addWidget(price_amount_label, 5)
        layout1.addWidget(payment_button, 3)
        layout1.setContentsMargins(0, 0, 0, 0)
        layout1.setSpacing(0)

        # 将商品总价格和支付按钮添加到主布局中
        main_layout.addWidget(payment_widget)

        # 主widget
        main_widget = QWidget()
        main_widget.setObjectName("purchase_widget")
        main_widget.setStyleSheet(Utils().read_qss_file("../res/qss/purchase_window.qss"))
        main_widget.setLayout(main_layout)

        # 主布局
        layout = QVBoxLayout(self)
        layout.addWidget(main_widget)

    def show_payment_window(self):
        # 创建支付窗口
        payment_window = PaymentWindow(self)
        payment_window.setWindowTitle('支付窗口')

        # 显示支付窗口
        payment_window.exec_()


class RestaurantInfo(QWidget):
    def __init__(self):
        super().__init__()

        # 创建界面
        self.arrive_time = None
        self.arrive_label = None
        self.address_label = None
        self.restaurant_combo = None
        self.restaurant_info = Client().getAllRestaurant()
        self.init_ui()

    def init_ui(self):
        # 下拉选择框
        self.restaurant_combo = QComboBox()
        self.restaurant_combo.currentIndexChanged.connect(self.update_address)

        # 餐厅地址
        self.address_label = QLabel()
        self.address_label.setObjectName("address_label")
        self.address_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout1 = QHBoxLayout()
        layout1.addWidget(self.restaurant_combo, 2)
        layout1.addWidget(self.address_label, 8)

        # 预计送达时间
        self.arrive_label = QLabel()
        self.arrive_label.setObjectName("arrive_label")
        self.arrive_label.setText("预计送达时间: ")

        # 送达时间
        self.arrive_time = QLabel()
        self.arrive_time.setObjectName("arrive_time")
        self.arrive_time.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout2 = QHBoxLayout()
        layout2.addWidget(self.arrive_label, 2)
        layout2.addWidget(self.arrive_time, 8)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)

        # 主widget
        main_widget = QWidget()
        main_widget.setObjectName("restaurant_info_widget")
        main_widget.setStyleSheet(Utils().read_qss_file("../res/qss/purchase_window.qss"))
        main_widget.setLayout(layout)

        # 主layout
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(main_widget)

        for restaurant in self.restaurant_info.values():
            self.restaurant_combo.addItem(restaurant[1])

    def update_address(self):
        # 获取当前选择的餐厅名
        selected_restaurant = self.restaurant_combo.currentText()

        # 更新地址标签
        if selected_restaurant in self.restaurant_info:
            self.address_label.setText(f'{self.restaurant_info[selected_restaurant][2]}')
            self.arrive_time.setText(Utils().add_minutes_to_current_time(30))
        else:
            self.address_label.clear()

    def get_selected_restaurant(self):
        self.restaurant_combo: QComboBox
        return self.restaurant_combo.currentText()


class PaymentWindow(QDialog):
    def __init__(self, parent: PurchaseWindow):
        super().__init__()

        self.setWindowTitle("支付")
        icon = QIcon("../res/images/images (8).png")
        self.setWindowIcon(icon)

        # 设置整体垂直布局
        main_layout = QVBoxLayout(self)

        # 创建按钮组，确保三个支付按钮互斥
        self.button_group = QButtonGroup(self)

        self.parent = parent

        # 添加支付方式按钮
        button_layout = QHBoxLayout()
        payment1 = QToolButton()
        payment1.setText("微信支付")
        icon = QIcon("../res/icons/微信支付.png")
        payment1.setObjectName("payment_method_btn")
        payment1.setIcon(icon)
        payment1.setIconSize(QSize(80, 80))
        payment1.setCheckable(True)
        payment1.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        payment2 = QToolButton()
        payment2.setText("支付宝")
        icon = QIcon("../res/icons/支付宝支付.png")
        payment2.setObjectName("payment_method_btn")
        payment2.setIcon(icon)
        payment2.setIconSize(QSize(80, 80))
        payment2.setCheckable(True)
        payment2.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        payment3 = QToolButton()
        payment3.setText("银联支付")
        icon = QIcon("../res/icons/银联.png")
        payment3.setObjectName("payment_method_btn")
        payment3.setIcon(icon)
        payment3.setIconSize(QSize(80, 80))
        payment3.setCheckable(True)
        payment3.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.button_group.addButton(payment1)
        self.button_group.addButton(payment2)
        self.button_group.addButton(payment3)
        button_layout.addWidget(payment1)
        button_layout.addWidget(payment2)
        button_layout.addWidget(payment3)

        main_layout.addLayout(button_layout)

        # 添加确认支付按钮
        confirm_payment_button = QPushButton('确认支付', self)
        confirm_payment_button.setObjectName("confirm_payment_button")
        confirm_payment_button.clicked.connect(self.confirm_payment)

        # 将确认支付按钮添加到主布局中
        main_layout.addWidget(confirm_payment_button)

        self.setStyleSheet(Utils().read_qss_file("../res/qss/purchase_window.qss"))

    def confirm_payment(self):
        # 获取选中的支付方式
        selected_button = self.button_group.checkedButton()
        if selected_button:
            confirmation = QMessageBox.question(self, '确认支付', f'支付方式为: {selected_button.text()}',
                                                QMessageBox.Yes | QMessageBox.No)

            if confirmation == QMessageBox.Yes:
                user_name = self.parent.payment_info.get('user_name')
                restaurant_name = self.parent.payment_info.get('restaurant_name')
                order_status = self.parent.payment_info.get('order_status')
                order_amount = self.parent.payment_info.get('order_amount')
                Client().uploadOrder(user_name, restaurant_name, order_status, order_amount)
                Client().getOrders(self.parent.user)

                QMessageBox.information(self, '支付成功', '支付成功！订单已完成!!!')
                self.accept()  # 关闭支付窗口
                self.parent.hide()
            else:
                QMessageBox.warning(self, '支付取消', '支付已取消')
        else:
            QMessageBox.information(self, '提示', "请选择支付方式")
            print("请选择支付方式")

    def uploadOrder(self, user_name, restaurant_name, order_status, order_amount):
        Client().uploadOrder(user_name, restaurant_name, order_status, order_amount)


class OrderBox(QWidget):
    def __init__(self, dish: dict):
        super().__init__()

        # 设置尺寸策略
        self.setFixedHeight(60)
        self.setFixedWidth(385)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        # 菜品名
        self.title = QLabel()
        self.title.setText(str(dish.get("title")))

        # 价格
        self.price = QLabel()
        self.price.setText("单价: " + dish.get("price"))

        # 数量
        self.quantity = QLabel()
        self.quantity.setText("数量: {}".format(dish.get("dishQuantity")))

        # 水平布局装载所有组件
        layout = QHBoxLayout()
        layout.addWidget(self.title, 5)
        layout.addWidget(self.price, 3)
        layout.addWidget(self.quantity, 1)

        # 主widget
        main_widget = QWidget()
        main_widget.setObjectName("dish_box_widget")
        main_widget.setStyleSheet(Utils().read_qss_file("../res/qss/purchase_window.qss"))
        main_widget.setLayout(layout)

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(main_widget)


class OrderInfo(QWidget):
    def __init__(self, dishMap: dict):
        super().__init__()

        # 设置主窗口大小
        # self.setFixedHeight(500)
        # 设置尺寸策略为 Fixed
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # 创建菜品详情的垂直布局
        layout = QVBoxLayout()
        menu_details_layout = QVBoxLayout()
        self.total_price = 0
        for dish in dishMap.values():
            self.total_price += round(float(dish.get('price')[1:]) * float(dish.get('dishQuantity')), 2)

            order_box = OrderBox(dish)
            menu_details_layout.addWidget(order_box)

        # 创建滚动区域，并将菜品详情布局放入其中
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area_widget = QWidget()
        scroll_area_widget.setLayout(menu_details_layout)
        scroll_area.setWidget(scroll_area_widget)
        layout.addWidget(scroll_area)

        # 主widget
        main_widget = QWidget()
        main_widget.setObjectName("order_info_widget")
        main_widget.setStyleSheet(Utils().read_qss_file("../res/qss/purchase_window.qss"))
        main_widget.setLayout(layout)

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(main_widget)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建按钮
        self.purchase_button = QPushButton('购买', self)

        # 将按钮连接到槽函数（即按钮点击时调用的函数）
        self.purchase_button.clicked.connect(self.show_purchase_window)

        # 设置主窗口布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.purchase_button)

    def show_purchase_window(self):
        # 创建子窗口，这里要使用 PurchaseWindow 类的实例
        dishesMap = {"汉堡":
                         {"title": "汉堡",
                          "price": "99.9",
                          "dishQuantity": "10"}}
        purchase_window = PurchaseWindow(dishesMap)
        purchase_window.setWindowTitle('购买窗口')

        # 显示 PurchaseWindow 实例
        purchase_window.exec_()


if __name__ == '__main__':
    app = QApplication([])

    # 创建主窗口
    main_window = MainWindow()
    main_window.show()

    app.exec_()

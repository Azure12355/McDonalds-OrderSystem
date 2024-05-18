from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea, QHBoxLayout, QSizePolicy

from common.user import User
from utils.utils import Utils


class OrderBoxWidget(QWidget):
    def __init__(self, order_id, user_name, restaurant_name, order_time, order_status, order_amount):
        super().__init__()

        # 设置 Widget 大小为
        self.setFixedHeight(100)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        # 创建水平布局
        layout = QHBoxLayout()

        # 添加订单信息标签（从左到右）
        order_id_label = QLabel(f'订单ID: {order_id}', self)
        user_name_label = QLabel(f'用户名称: {user_name}', self)
        restaurant_name_label = QLabel(f'餐厅名称: {restaurant_name}', self)
        order_time_label = QLabel(f'订单时间: {order_time}', self)
        order_status_label = QLabel(f'订单状态: {order_status}', self)
        order_amount_label = QLabel(f'订单金额: {order_amount}', self)

        # 将标签添加到水平布局中
        layout.addWidget(order_id_label)
        layout.addWidget(user_name_label)
        layout.addWidget(restaurant_name_label)
        layout.addWidget(order_time_label)
        layout.addWidget(order_status_label)
        layout.addWidget(order_amount_label)

        # 主widget
        main_widget = QWidget()
        main_widget.setObjectName("order_management_main_widget")
        main_widget.setStyleSheet(Utils().read_qss_file("../res/qss/order_management.qss"))
        main_widget.setLayout(layout)

        # 主布局
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(main_widget)

class OrderMessageWidget(QWidget):
    def __init__(self, user: User):
        super().__init__()

        # 设置 Widget 大小为 500*100
        # self.setFixedSize(500, 600)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # 创建垂直布局
        main_layout = QVBoxLayout()

        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # 创建垂直布局用于存放订单盒子
        orders_layout = QVBoxLayout()

        # 添加多个 OrderBoxWidget（示例数据）
        self.user = user
        if len(self.user.orders) == 0:
            label = QLabel("你还没有任何消费记录, 一起来愉快点餐吧")
            orders_layout.addWidget(label)
        else:
            for order in self.user.orders:
                order_box_widget = OrderBoxWidget(
                    order_id=order[0],
                    user_name=order[1],
                    restaurant_name=order[2],
                    order_time=order[3],
                    order_status=order[4],
                    order_amount=order[5]
                )
                orders_layout.addWidget(order_box_widget)
        # 将垂直布局添加到滚动区域中
        scroll_widget = QWidget(self)
        scroll_widget.setObjectName("scroll_widget")
        scroll_widget.setStyleSheet(Utils().read_qss_file("../res/qss/order_management.qss"))
        scroll_widget.setLayout(orders_layout)
        scroll_area.setWidget(scroll_widget)

        # 将滚动区域添加到主布局中
        main_layout.addWidget(scroll_area)

        # 主widget
        main_widget = QWidget()
        main_widget.setObjectName("order_management_main_widget")
        main_widget.setStyleSheet(Utils().read_qss_file("../res/qss/order_management.qss"))
        main_widget.setLayout(main_layout)

        # 主布局
        layout = QVBoxLayout(self)
        layout.addWidget(main_widget)


if __name__ == '__main__':
    app = QApplication([])

    # 创建主窗口
    main_window = QWidget()
    main_window.setWindowTitle('订单消息示例')

    # 创建订单消息 Widget
    order_message_widget = OrderMessageWidget()

    # 设置主窗口布局
    main_layout = QVBoxLayout(main_window)
    main_layout.addWidget(order_message_widget)

    main_window.show()

    app.exec_()

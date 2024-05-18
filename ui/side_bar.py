from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication, QSizePolicy, QListWidget, QListWidgetItem


class SideBar(QWidget):
    def __init__(self):
        super().__init__()

        # 设置主窗口大小
        self.setFixedSize(220, 740)
        # 设置尺寸策略为Fixed
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # 设置objectName, 用于标识对象
        self.setObjectName("side_bar")

        # 创建布局管理器
        layout = QVBoxLayout(self)

        # 添加QListWidget
        self.list_widget = QListWidget(self)
        items = ["首页", "最新优惠", "精选套餐", "菜单点餐", "购物车管理", "订单管理", "我的", "设置"]
        for item in items:
            item = QListWidgetItem(item)
            self.list_widget.addItem(item)
        self.list_widget.currentItemChanged.connected()

        # 将组件添加到布局管理器中
        layout.addWidget(self.list_widget)


if __name__ == '__main__':
    app = QApplication([])
    side_bar = SideBar()
    side_bar.show()
    app.exec()

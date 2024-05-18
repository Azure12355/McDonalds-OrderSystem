from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import QListWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, QGroupBox, QScrollArea, QListWidget, QPushButton, \
    QLineEdit, QSizePolicy, QMessageBox
from client.client import Client
from ui.bottom_popup_window import DishDetailsBox, PackageDetails
from utils.utils import Utils


class MenuOrder(QWidget):
    def __init__(self, items):
        super().__init__()

        # 设置主窗口大小
        # self.setFixedSize(870, 640)
        # 设置尺寸策略为 Fixed
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.layout = QVBoxLayout()
        self.setObjectName("menu_order")
        self.setStyleSheet(Utils().read_qss_file("../res/qss/menu_order.qss"))

        # 搜索框
        self.searchEdit = QLineEdit()
        self.searchEdit.setObjectName("menu_order_search_edit")
        # self.searchEdit.setFixedSize(400, 50)

        # 搜索按钮
        self.searchBtn = QPushButton("搜索")
        self.searchBtn.setObjectName("menu_order_search_btn")
        # self.searchBtn.setFixedSize(150, 50)

        # 水平布局装载搜索框和按钮
        self.searchLayout = QHBoxLayout()
        self.searchLayout.addWidget(self.searchEdit)
        self.searchLayout.addWidget(self.searchBtn)
        # 菜品分类列表
        self.dishCategoryList = QListWidget()
        self.dishCategoryList.setObjectName("category_list")
        self.dishCategoryList.setStyleSheet(Utils().read_qss_file("../res/qss/menu_order.qss"))
        self.dishCategoryList.setFixedWidth(180)

        # 使用list装载所有的菜品分类
        self.dishCategoryMap = []
        # 使用Map装载所有GroupBox
        self.dishCategoryGroupBoxMap = {}

        # 右半区菜品窗口
        self.dishWindowLayout = QVBoxLayout()
        self.createDishCategoryItem(items=items)
        for key, value in self.dishCategoryGroupBoxMap.items():
            self.dishWindowLayout.addWidget(value)

        # 将右半区菜品窗口放置到滚动布局中
        self.scrollContent = QWidget()
        self.scrollContent.setLayout(self.dishWindowLayout)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.scrollContent)
        self.scrollArea.setWidgetResizable(True)

        # 水平布局装载list和dish_window
        self.bottom_widget = QWidget()
        self.bottom_widget.setObjectName("bottom_widget")
        self.bottom_widget.setStyleSheet(Utils().read_qss_file("../res/qss/menu_order.qss"))
        self.hLayout = QHBoxLayout(self.bottom_widget)
        self.hLayout.addWidget(self.dishCategoryList, 3)
        self.hLayout.addWidget(self.scrollArea, 7)

        # 主要布局
        self.layout.addLayout(self.searchLayout)
        self.layout.addWidget(self.bottom_widget)
        self.setLayout(self.layout)

        # 注册点击事件
        self.init_event()

    def init_event(self):
        # 绑定list的item点击事件
        self.dishCategoryList.itemClicked.connect(self.scrollToGroupBox)
        self.searchBtn.clicked.connect(self.searchDishes)

    def createDishCategoryGroupBox(self, title):
        """
        根据list中对应的item的title构建对应的groupBox
        :param title: item的title
        :return: None
        """
        group_box = QGroupBox()
        group_box.setFixedWidth(600)
        group_box.setTitle(title)
        group_box_layout = QVBoxLayout()
        group_box.setLayout(group_box_layout)
        self.dishCategoryGroupBoxMap[title] = group_box

    def createDishCategoryItem(self, items: list):
        """
        创建List中的item项
        :param items: 需要添加的items列表
        :return: None
        """
        global icon_path
        for item in items:
            listItem = QListWidgetItem(item)
            listItem.setFont(QFont("幼圆", 13, QFont.Weight.ExtraBold))  # 设置字体
            if item == "汉堡":
                icon_path = "../res/animations/animate (20).png"
            elif item == "披萨":
                icon_path = "../res/animations/animate (8).png"
            elif item == "小食":
                icon_path = "../res/animations/animate (42).png"
            elif item == "甜品":
                icon_path = "../res/animations/animate (22).png"
            elif item == "早餐":
                icon_path = "../res/animations/fried-egg.png"
            elif item == "饮品":
                icon_path = "../res/animations/animate (28).png"
            elif item == "500大卡套餐":
                icon_path = "../res/animations/animate (10).png"
            elif item == "开心乐园餐":
                icon_path = "../res/animations/animate (2).png"
            elif item == "热菜":
                icon_path = "../res/animations/hot-pot.png"
            elif item == "凉菜":
                icon_path = "../res/animations/pancake.png"
            else:
                icon_path = ""
            icon = QIcon(icon_path)
            listItem.setIcon(icon)  # 设置图标
            self.dishCategoryList.addItem(listItem)
            self.createDishCategoryGroupBox(item)
        self.dishCategoryList.setIconSize(QSize(50, 50))

    def addDishToGroupBox(self, group_box_title, item: [QWidget, QVBoxLayout, QHBoxLayout]):
        """
        往对应的groupBox中添加元素
        :param group_box_title: 需要添加元素的groupBox
        :param item: 需要添加的元素
        :return: None
        """
        group_box: QGroupBox = self.dishCategoryGroupBoxMap.get(group_box_title)
        if group_box is not None:
            group_box_layout = group_box.layout()
            if isinstance(item, QWidget):
                group_box_layout.addWidget(item)
            elif isinstance(item, (QHBoxLayout, QVBoxLayout)):
                group_box_layout.addChildLayout(item)
            else:
                print("添加的元素类型有误！！！")

    def scrollToGroupBox(self, item: QListWidgetItem):
        """
        点击对应的item项，滚动到指定的groupBox
        :param item: 被点击的项
        :return: None
        """
        # 获取点击的item在list中的索引
        title = item.text()
        # 获取对应的groupBox
        group_box = self.dishCategoryGroupBoxMap[title]
        # 获取垂直滚动条
        v_scroll_bar = self.scrollArea.verticalScrollBar()
        # 计算滚动到指定的groupbox的顶部的位置
        scroll_position = group_box.pos().y() - self.scrollArea.contentsMargins().top()
        # 设置垂直滚动条的值
        v_scroll_bar.setValue(scroll_position)

    def searchDishes(self):
        # 获取搜索关键字
        keyword = self.searchEdit.text().lower()

        # 遍历每个GroupBox中的菜品标签，根据关键字进行匹配
        for group_title, group_box in self.dishCategoryGroupBoxMap.items():
            group_box_layout = group_box.layout()
            for i in range(group_box_layout.count()):
                widget: PackageDetails
                widget = group_box_layout.itemAt(i).widget()
                if isinstance(widget, PackageDetails):
                    # 获取菜品标签的文本
                    dish_name = widget.title.text()
                    # 判断关键字是否存在于菜品标签中
                    if keyword in dish_name:
                        # 使用 ensureWidgetVisible 函数确保 widget 完全可见
                        self.scrollArea.ensureWidgetVisible(widget)
                        return

        # 如果没有匹配项，弹出提示窗口
        QMessageBox.information(self, "Search Result", "No matching dishes found.")
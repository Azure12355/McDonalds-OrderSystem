# -*- coding: utf-8 -*-
import warnings

from PySide6.QtCore import QSize, Qt, QPropertyAnimation, QEasingCurve, QPoint, QPointF, Slot, Signal
from PySide6.QtGui import QIcon, QPixmap, QFont, Qt, QMouseEvent
from PySide6.QtWidgets import QSizePolicy, QListWidget, QListWidgetItem, QTabWidget, QHBoxLayout, \
    QLabel, QScrollArea, QSpacerItem, QGroupBox, QFrame, QButtonGroup, QCheckBox, QWidget, QApplication, QVBoxLayout, QPushButton, \
    QGridLayout, QLineEdit

from utils.utils import Utils

# 忽略特定类型的 DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)


class CDrawer(QWidget):
    LEFT, TOP, RIGHT, BOTTOM = range(4)

    def __init__(self, *args, stretch=1 / 3, direction=0, widget=None, **kwargs):
        super(CDrawer, self).__init__(*args, **kwargs)
        self.setWindowFlags(self.windowFlags(
        ) | Qt.FramelessWindowHint | Qt.Popup | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 进入动画
        self.animIn = QPropertyAnimation(
            self, duration=500, easingCurve=QEasingCurve.OutCubic)
        self.animIn.setPropertyName(b'pos')
        # 离开动画
        self.animOut = QPropertyAnimation(
            self, duration=500, finished=self.onAnimOutEnd,
            easingCurve=QEasingCurve.OutCubic)
        self.animOut.setPropertyName(b'pos')
        self.animOut.setDuration(500)
        self.setStretch(stretch)  # 占比
        self.direction = direction  # 方向
        # 半透明背景
        self.alphaWidget = QWidget(
            self, objectName='CDrawer_alphaWidget',
            styleSheet='#CDrawer_alphaWidget{background:rgba(55,55,55,100);}')
        self.alphaWidget.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setWidget(widget)  # 子控件

    def resizeEvent(self, event):
        self.alphaWidget.resize(self.size())
        super(CDrawer, self).resizeEvent(event)

    def mousePressEvent(self, event):
        pos = event.pos()
        if pos.x() >= 0 and pos.y() >= 0 and self.childAt(pos) == None and self.widget:
            if not self.widget.geometry().contains(pos):
                self.animationOut()
                return
        super(CDrawer, self).mousePressEvent(event)

    def show(self):
        super(CDrawer, self).show()
        parent = self.parent().window() if self.parent() else self.window()
        if not parent or not self.widget:
            return
        # 设置Drawer大小和主窗口一致
        self.setGeometry(parent.geometry())
        geometry = self.geometry()
        self.animationIn(geometry)

    def animationIn(self, geometry):
        """进入动画
        :param geometry:
        """
        if self.direction == self.LEFT:
            # 左侧抽屉
            self.widget.setGeometry(
                0, 0, int(geometry.width() * self.stretch), geometry.height())
            self.widget.hide()
            self.animIn.setStartValue(QPoint(-self.widget.width(), 0))
            self.animIn.setEndValue(QPoint(0, 0))
            self.animIn.start()
            self.widget.show()
        elif self.direction == self.TOP:
            # 上方抽屉
            self.widget.setGeometry(
                0, 0, geometry.width(), int(geometry.height() * self.stretch))
            self.widget.hide()
            self.animIn.setStartValue(QPoint(0, -self.widget.height()))
            self.animIn.setEndValue(QPoint(0, 0))
            self.animIn.start()
            self.widget.show()
        elif self.direction == self.RIGHT:
            # 右侧抽屉
            width = int(geometry.width() * self.stretch)
            self.widget.setGeometry(
                geometry.width() - width, 0, width, geometry.height())
            self.widget.hide()
            self.animIn.setStartValue(QPoint(self.width(), 0))
            self.animIn.setEndValue(
                QPoint(self.width() - self.widget.width(), 0))
            self.animIn.start()
            self.widget.show()
        elif self.direction == self.BOTTOM:
            # 下方抽屉
            height = int(geometry.height() * self.stretch)
            self.widget.setGeometry(
                0, geometry.height() - height, geometry.width(), height)
            self.widget.hide()
            self.animIn.setStartValue(QPoint(0, self.height()))
            self.animIn.setEndValue(
                QPoint(0, self.height() - self.widget.height()))
            self.animIn.start()
            self.widget.show()

    def animationOut(self):
        """离开动画
        """
        self.animIn.stop()  # 停止进入动画
        geometry = self.widget.geometry()
        if self.direction == self.LEFT:
            # 左侧抽屉
            self.animOut.setStartValue(geometry.topLeft())
            self.animOut.setEndValue(QPoint(-self.widget.width(), 0))
            self.animOut.start()
        elif self.direction == self.TOP:
            # 上方抽屉
            self.animOut.setStartValue(QPoint(0, geometry.y()))
            self.animOut.setEndValue(QPoint(0, -self.widget.height()))
            self.animOut.start()
        elif self.direction == self.RIGHT:
            # 右侧抽屉
            self.animOut.setStartValue(QPoint(geometry.x(), 0))
            self.animOut.setEndValue(QPoint(self.width(), 0))
            self.animOut.start()
        elif self.direction == self.BOTTOM:
            # 下方抽屉
            self.animOut.setStartValue(QPoint(0, geometry.y()))
            self.animOut.setEndValue(QPoint(0, self.height()))
            self.animOut.start()

    def onAnimOutEnd(self):
        """离开动画结束
        """
        # 模拟点击外侧关闭
        QApplication.sendEvent(self, QMouseEvent(
            QMouseEvent.MouseButtonPress, QPointF(-1, -1), Qt.LeftButton, Qt.NoButton, Qt.NoModifier))

    def setWidget(self, widget):
        """设置子控件
        :param widget:
        """
        self.widget = widget
        if widget:
            widget.setParent(self)
            self.animIn.setTargetObject(widget)
            self.animOut.setTargetObject(widget)

    def setEasingCurve(self, easingCurve):
        """设置动画曲线
        :param easingCurve:
        """
        self.animIn.setEasingCurve(easingCurve)

    def getStretch(self):
        """获取占比
        """
        return self.stretch

    def setStretch(self, stretch):
        """设置占比
        :param stretch:
        """
        self.stretch = max(0.1, min(stretch, 0.9))

    def getDirection(self):
        """获取方向
        """
        return self.direction

    def setDirection(self, direction):
        """设置方向
        :param direction:
        """
        direction = int(direction)
        if direction < 0 or direction > 3:
            direction = self.LEFT
        self.direction = direction


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置主窗口大小
        self.setFixedSize(900, 740)
        # 设置尺寸策略为Fixed
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # 设置objectName
        self.setObjectName("main_window")
        # 设置样式
        self.setStyleSheet(Utils.read_qss_file("../res/qss/main_window.qss"))

        # 顶栏
        self.top_bar = TopBar()
        # 功能窗口
        self.function_widget = FunctionWidget()

        self.init_widget()

    def init_widget(self):
        # 创建垂直布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.top_bar)
        layout.addWidget(self.function_widget)
        for i in range(50):
            offer_details = LatestOfferDetails()
            offer_details.set_cover("../res/images/images (10).jpg")
            offer_details.set_title("$33 脆辣雞腿飽及飲品配一款小食(參考價$42.5起)")
            offer_details.set_desc(
                "-可選:中薯條 / 粒粒粟米杯(中) / 蘋果批\n-可轉配或加錢升級其他飲品。升級請參考飲品價目表\n-優惠於早上11時至午夜12時適用")
            self.function_widget.latest_offer.set_offer_details(offer_details)


class TopBar(QWidget):
    def __init__(self):
        super().__init__()

        # 设置主窗口大小
        self.setFixedSize(850, 50)
        # 设置尺寸策略为Fixed
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.setObjectName("top_bar")
        self.layout = QHBoxLayout(self)

        self.title = QLabel("校园点餐系统欢迎您, 祝您用餐愉快~~~")

        self.setting_btn = QPushButton()
        self.setting_btn.setFixedSize(30, 30)
        self.setting_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setting_btn.setIcon(QIcon("../res/icons/cloud.png"))
        self.setting_btn.setIconSize(QSize(30, 30))

        self.close_btn = QPushButton()
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.close_btn.setIcon(QIcon("../res/icons/icon_ (18).png"))
        self.close_btn.setIconSize(QSize(30, 30))

        self.minimum_btn = QPushButton()
        self.minimum_btn.setFixedSize(30, 30)
        self.minimum_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.minimum_btn.setIcon(QIcon("../res/icons/缩小.png"))
        self.minimum_btn.setIconSize(QSize(30, 30))

        self.maximum_btn = QPushButton()
        self.maximum_btn.setFixedSize(30, 30)
        self.maximum_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.maximum_btn.setIcon(QIcon("../res/icons/icon_ (23).png"))
        self.maximum_btn.setIconSize(QSize(30, 30))

        self.init_widget()

    def init_widget(self):
        # 创建布局管理器
        self.layout.addWidget(self.title, 8)
        self.layout.addWidget(self.setting_btn, 1)
        self.layout.addWidget(self.minimum_btn, 1)
        self.layout.addWidget(self.maximum_btn, 1)
        self.layout.addWidget(self.close_btn, 1)

    def set_title(self, title):
        self.title.setText(title)


class FunctionWidget(QTabWidget):
    def __init__(self):
        super().__init__()

        # 设置主窗口大小
        self.setFixedSize(876, 800)
        # 设置尺寸策略为Fixed
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # 创建布局管理器
        self.layout = QVBoxLayout(self)

        item1 = QListWidgetItem()
        item1.setText("item1")
        item2 = QListWidgetItem()
        item2.setText("item2")
        item3 = QListWidgetItem()
        item3.setText("item3")

        # 创建TabWidget
        self.function_stacked_widget = QTabWidget(self)
        self.latest_offer = LatestOffer()
        self.affordable_package = AffordablePackage()
        self.menu_order = MenuOrder([item1, item2, item3])
        self.order_management = QWidget()

        self.function_stacked_widget.addTab(self.latest_offer, "最新优惠")
        self.function_stacked_widget.addTab(self.affordable_package, "实惠套餐")
        self.function_stacked_widget.addTab(self.menu_order, "菜单点餐")
        self.function_stacked_widget.addTab(self.order_management, "订单管理")

        for i in range(1, 4):
            for j in range(50):
                packageDetails = PackageDetails(self.menu_order)
                packageDetails.set_cover("../res/images/images (33).png")
                packageDetails.set_title("香辣鸡腿堡")
                packageDetails.set_discount("8.8")
                packageDetails.set_current("39.9")
                packageDetails.set_origin("58.8")

                self.menu_order.add_dish_to_group_box(f"item{i}", packageDetails)
        # 将组件添加到布局管理器中
        self.layout.addWidget(self.function_stacked_widget)


class LatestOffer(QWidget):
    def __init__(self):
        super().__init__()

        # 设置主窗口大小
        self.setFixedSize(870, 640)
        # 设置尺寸策略为 Fixed
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout = QVBoxLayout(self)

        # 主图片
        self.main_cover = QLabel()
        self.main_cover.setFixedSize(800, 350)
        self.main_cover.setPixmap(QPixmap("../res/images/images (35).png"))
        self.main_cover.setScaledContents(True)

        # 创建网格布局放置图片
        self.grid_layout = QGridLayout(self)

        self.main_layout = QVBoxLayout(self)

        self.scroll_area = QScrollArea(self)

        # 网格中已经存放的组件数量
        self.size = 0

        # 设置每行显示的图片数量
        self.cover_per_row = 2

        self.init_widget()

    def init_widget(self):
        # 创建垂直布局管理器
        self.main_layout.addWidget(self.main_cover)
        # 将网格布局添加到主布局中
        self.main_layout.addLayout(self.grid_layout)
        # 创建滚动区域装载整个布局

        # 创建 QWidget 作为滚动区域的可滚动内容
        scroll_content = QWidget()
        scroll_content.setLayout(self.main_layout)

        # 设置滚动区域的可滚动内容
        self.scroll_area.setWidget(scroll_content)

        # 设置滚动区域的滚动条属性
        self.scroll_area.setWidgetResizable(True)

        self.layout.addWidget(self.scroll_area)

    def size(self):
        """
        返回个数
        :return: 返回个数
        """
        return self.size

    def set_column_capacity(self, capacity):
        """
        设置网格布局中每行显示的个数
        :param capacity: 每行个数
        :return: none
        """
        self.cover_per_row = capacity

    def set_offer_details(self, offer_details):
        """
        在网格中设置对应的套餐详情
        :param offer_details: 套餐详情对象
        :return: none
        """
        row = self.size // self.cover_per_row
        col = self.size % self.cover_per_row
        self.grid_layout.addWidget(offer_details, row, col)
        self.size += 1


class LatestOfferDetails(QWidget):
    def __init__(self):
        super().__init__()

        # 设置主窗口大小
        self.setFixedSize(400, 600)
        # 设置尺寸策略为 Fixed
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # 封面
        self.cover = QLabel()
        self.cover.setFixedSize(400, 300)
        self.cover.setScaledContents(True)

        # 字体
        self.title_font = QFont()
        self.title_font.setPointSize(16)
        self.title_font.setBold(True)

        # 标题
        self.title = QLabel()
        self.title.setFixedWidth(400)
        self.title.setFont(self.title_font)
        self.title.setWordWrap(True)
        self.title.setAlignment(Qt.AlignCenter)

        # 字体
        self.desc_font = QFont()
        self.desc_font.setPointSize(12)
        self.desc_font.setBold(False)

        # 描述
        self.desc = QLabel()
        self.desc.setFixedWidth(400)
        self.desc.setFont(self.desc_font)
        self.desc.setWordWrap(True)
        self.desc.setAlignment(Qt.AlignCenter)

        # 购买按钮
        self.buy = QPushButton()
        self.buy.setText("购买")

        self.init_widget()

    def init_widget(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.cover)
        layout.addWidget(self.title)
        layout.addWidget(self.desc)
        layout.addWidget(self.buy)

    def set_cover(self, cover_file_name):
        """
        设置优惠详情的封面
        :param cover_file_name:
        :return:
        """
        self.cover.setPixmap(QPixmap(cover_file_name))

    def set_title(self, title):
        """
        设置标题
        :param title:
        :return:
        """
        self.title.setText(title)

    def set_desc(self, desc):
        """
        设置描述
        :param desc:
        :return:
        """
        self.desc.setText(desc)


class AffordablePackage(QWidget):
    def __init__(self):
        super().__init__()

        # 设置主窗口大小
        self.setFixedSize(870, 640)
        # 设置尺寸策略为 Fixed
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout = QVBoxLayout(self)
        # 装载整体的布局
        self.main_layout = QVBoxLayout()

        for i in range(20):
            packageDetails = PackageDetails(self)
            packageDetails.set_cover("../res/images/images (33).png")
            packageDetails.set_title("香辣鸡腿堡")
            packageDetails.set_discount("8.8")
            packageDetails.set_current("39.9")
            packageDetails.set_origin("58.8")

            self.main_layout.addWidget(packageDetails)

        # 创建 QWidget 作为滚动区域的可滚动内容
        scroll_content = QWidget()
        scroll_content.setLayout(self.main_layout)

        # 设置滚动区域的可滚动内容
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(scroll_content)

        # 设置滚动区域的滚动条属性
        self.scroll_area.setWidgetResizable(True)

        self.layout.addWidget(self.scroll_area)


class PackageDetails(QWidget):
    def __init__(self, parent_widget: QWidget):
        super().__init__()
        self.parent_widget = parent_widget
        # 设置主窗口大小
        self.setFixedHeight(200)
        # 设置尺寸策略为 Fixed
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        # 封面
        self.cover = QLabel()
        self.cover.setObjectName("package_details_cover")
        self.cover.setFixedSize(200, 200)
        self.cover.setScaledContents(True)

        # 套餐名
        self.title = QLabel()
        self.title.setObjectName("package_details_title")
        self.title.setFixedHeight(50)
        # 套餐标题的字体样式
        self.title_font = QFont()
        self.title_font.setPointSize(14)
        self.title_font.setBold(True)
        self.title.setFont(self.title_font)

        # 折扣
        self.discount = QLabel()
        self.discount.setObjectName("package_details_discount")
        self.discount.setFixedSize(20, 10)

        # 现价
        self.current = QLabel()
        self.current.setObjectName("package_details_current")
        self.current.setFixedSize(30, 10)

        # 原价
        self.origin = QLabel()
        self.origin.setObjectName("package_details_origin")
        self.origin.setFixedSize(30, 10)

        # 购买按钮
        self.buy = QPushButton("选规格")
        self.buy.setObjectName("package_details_buy")
        self.buy.setFixedSize(50, 30)

        # 价格线的弹簧
        self.price_spacer = QSpacerItem(10, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # 状态价格这行的容器
        self.price_layout = QHBoxLayout()
        self.price_layout.addWidget(self.current, )
        self.price_layout.addWidget(self.origin, )
        self.price_layout.addSpacerItem(self.price_spacer)
        self.price_layout.addWidget(self.buy, )

        # 垂直布局装载 title, discount, price
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.discount)
        self.layout.addLayout(self.price_layout)

        # 整体布局
        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(self.cover)
        self.main_layout.addLayout(self.layout)
        self.main_layout.setAlignment(Qt.AlignLeft)

        self.buy.clicked.connect(self.show_bottom_popup)

    def set_cover(self, cover_file_name):
        """
        设置优惠详情的封面
        :param cover_file_name:
        :return:
        """
        self.cover.setPixmap(QPixmap(cover_file_name))

    def set_title(self, title):
        """
        设置标题
        :param title:
        :return:
        """
        self.title.setText(title)

    def set_discount(self, discount):
        """
        设置折扣
        :param discount:
        :return:
        """
        self.discount.setText(discount)

    def set_current(self, current):
        """
        设置现价
        :param current:
        :return:
        """
        self.current.setText(current)

    def set_origin(self, origin):
        """
        设置现价
        :param origin:
        :return:
        """
        self.origin.setText(origin)

    def show_bottom_popup(self):
        if not hasattr(self, 'topDrawer'):
            # 判断是否已经拥有该属性，如果没有就创建
            self.bottomDrawer = CDrawer(self, stretch=3 / 4, direction=CDrawer.BOTTOM)
            self.bottomDrawer.setWidget(BottomPopupWidget(self.bottomDrawer))
        self.bottomDrawer.show()


class MenuOrder(QWidget):
    def __init__(self, items):
        super().__init__()

        # 设置主窗口大小
        self.setFixedSize(870, 640)
        # 设置尺寸策略为 Fixed
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout = QVBoxLayout()

        # 搜索框
        self.search_edit = QLineEdit()
        self.search_edit.setObjectName("menu_order_search_edit")
        self.search_edit.setFixedSize(400, 50)

        # 搜索按钮
        self.search_btn = QPushButton("搜索")
        self.search_btn.setObjectName("menu_order_search_btn")
        self.search_btn.setFixedSize(150, 50)

        # 水平布局装载搜索框和按钮
        self.search_layout = QHBoxLayout()
        self.search_layout.addWidget(self.search_edit)
        self.search_layout.addWidget(self.search_btn)
        # 菜品分类列表
        self.dish_categories = QListWidget()
        self.dish_categories.setFixedWidth(200)

        # 使用list装载所有的菜品分类
        self.all_dish_categories = []
        # 使用Map装载所有GroupBox
        self.group_box_map = {}

        # 右半区菜品窗口
        self.dish_window_layout = QVBoxLayout()
        self.create_dish_category_item(items=items)
        for key, value in self.group_box_map.items():
            self.dish_window_layout.addWidget(value)

        # 将右半区菜品窗口放置到滚动布局中
        self.scroll_content = QWidget()
        self.scroll_content.setLayout(self.dish_window_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setWidgetResizable(True)

        # 水平布局装载list和dish_window
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.dish_categories)
        self.hlayout.addWidget(self.scroll_area)

        # 主要布局
        self.layout.addLayout(self.search_layout)
        self.layout.addLayout(self.hlayout)
        self.setLayout(self.layout)

        # 注册点击事件
        self.init_event()

    def init_event(self):
        # 绑定list的item点击事件
        self.dish_categories.itemClicked.connect(self.scroll_to_group_box)

    def create_dish_group_box(self, title):
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
        self.group_box_map[title] = group_box

    def create_dish_category_item(self, items: list):
        """
        创建List中的item项
        :param items: 需要添加的items列表
        :return: None
        """
        for item in items:
            self.dish_categories.addItem(item)
            self.create_dish_group_box(item.text())

    def add_dish_to_group_box(self, group_box_title, item: [QWidget, QVBoxLayout, QHBoxLayout]):
        """
        往对应的groupBox中添加元素
        :param group_box_title: 需要添加元素的groupBox
        :param item: 需要添加的元素
        :return: None
        """
        group_box: QGroupBox = self.group_box_map.get(group_box_title)
        if group_box is not None:
            group_box_layout = group_box.layout()
            if isinstance(item, QWidget):
                group_box_layout.addWidget(item)
            elif isinstance(item, (QHBoxLayout, QVBoxLayout)):
                group_box_layout.addChildLayout(item)
            else:
                print("添加的元素类型有误！！！")

    def scroll_to_group_box(self, item: QListWidgetItem):
        """
        点击对应的item项，滚动到指定的groupBox
        :param item: 被点击的项
        :return: None
        """
        # 获取点击的item在list中的索引
        title = item.text()
        # 获取对应的groupBox
        group_box = self.group_box_map[title]
        # 获取垂直滚动条
        v_scroll_bar = self.scroll_area.verticalScrollBar()
        # 计算滚动到指定的groupbox的顶部的位置
        scroll_position = group_box.pos().y() - self.scroll_area.contentsMargins().top()
        # 设置垂直滚动条的值
        v_scroll_bar.setValue(scroll_position)


class DishDetailsBox(QWidget):
    """
    装载菜品的盒子
    """
    checkBoxSignal = Signal(QWidget, bool)

    def __init__(self, dishId: str, cover: QPixmap, title: str, price: str):
        super().__init__()

        # 设置主窗口大小
        self.setFixedSize(100, 200)
        # 设置尺寸策略为 Fixed
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # 复选框
        self.checkBox = QCheckBox()
        # 自定义checkBox信号
        self.checkBox.stateChanged.connect(self.checkBoxStateChanged)

        # 菜品id
        self.dishId = dishId

        # 封面
        self.cover = QLabel()
        self.cover.setPixmap(cover)
        self.cover.setFixedSize(100, 100)

        # 标题
        self.title = QLabel(title)
        self.title.setFixedSize(100, 50)

        # 价格
        self.price = QLabel(price)
        self.price.setFixedSize(100, 50)

        layout = QVBoxLayout(self)
        layout.addWidget(self.checkBox)
        layout.addWidget(self.cover)
        layout.addWidget(self.title)
        layout.addWidget(self.price)

    @Slot(int)
    def checkBoxStateChanged(self, state):
        if state == 2:
            # 发出自定义信号
            self.checkBoxSignal.emit(self, True)
        else:
            # 发出自定义信号
            self.checkBoxSignal.emit(self, False)


class DishDetailsGroupBox(QWidget):
    """
    装载DishBox的GroupBox
    """

    def __init__(self, title):
        super().__init__()

        # 设置主窗口大小
        self.setFixedWidth(400)
        # 设置尺寸策略为 Fixed
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)

        # 创建groupBox用于装载dishBox
        self.groupBox = QGroupBox()
        self.groupBox.setTitle(title)

        # 创建按钮组实现多个radioBtn间的互斥
        button_group = QButtonGroup()

        # 网格中已经存放的dishBox数量
        self.size = 0
        # 设置每行显示的dishBox
        self.cover_per_row = 3

        # 网格布局装载所有的dishBox
        self.gridLayout = QGridLayout()

        # dishBox的map, 统一管理map
        self.dishBoxMap = {}
        self.groupBox.setLayout(self.gridLayout)

        # 主布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.groupBox)

    def deleteDishBox(self, dishBoxTitle):
        """
        从布局中删除对应的dishBox
        :param dishBoxTitle: 需要删除的dishBox的标题
        :return: None
        """
        self.gridLayout.removeWidget(self.dishBoxMap.pop(dishBoxTitle))

    def addDishBox(self, dishBox: DishDetailsBox):
        """
        往布局中添加指定的dishBox
        :param dishBox: 需要添加的dishBox
        :return: None
        """
        row = self.size // self.cover_per_row
        col = self.size % self.cover_per_row
        self.gridLayout.addWidget(dishBox, row, col)
        self.dishBoxMap[dishBox.title.text()] = dishBox
        self.size += 1

    def getAllDishBox(self) -> dict:
        """
        返回所有的dishBox
        :return: dict
        """
        return self.dishBoxMap


class DishDetailsWidget(QWidget):
    """
    菜品详情页
    """

    def __init__(self):
        super().__init__()

        # 设置主窗口大小
        self.setFixedSize(400, 500)
        # 设置尺寸策略为 Fixed
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # 封面
        self.cover = QLabel()
        self.cover.setFixedSize(400, 300)

        # 标题
        self.title = QLabel()
        self.title.setFixedSize(200, 50)

        # 描述
        self.desc = QLabel()
        self.desc.setFixedSize(200, 200)

        # 加入购物车按钮
        self.addToCartBtn = QPushButton("加入购物车")

        # 管理groupBox的map
        self.groupBoxMap = {}

        # 垂直布局配合滚轮布局
        self.contentLayout = QVBoxLayout()
        self.contentLayout.addWidget(self.cover)
        self.contentLayout.addWidget(self.title)
        self.contentLayout.addWidget(self.desc)

        self.scrollContent = QWidget()
        self.scrollContent.setLayout(self.contentLayout)
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.scrollContent)
        self.scrollArea.setWidgetResizable(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.scrollArea)
        layout.addWidget(self.addToCartBtn)

    def addDishGroupBox(self, groupBox: DishDetailsGroupBox):
        """
        往content中添加对应的groupBox
        :param groupBox: 需要添加的groupBox
        :return: None
        """
        self.contentLayout.addWidget(groupBox)
        groupBoxTitle = groupBox.groupBox.title()
        self.groupBoxMap[groupBoxTitle] = groupBox

    def createDishGroupBox(self, groupBoxTitle: str):
        """
        根据对应的title创建groupBox
        :param groupBoxTitle: title
        :return: None
        """
        groupBox = DishDetailsGroupBox(groupBoxTitle)
        self.contentLayout.addWidget(groupBox)
        self.groupBoxMap[groupBoxTitle] = groupBox

    def deleteGroupBox(self, groupBoxTitle):
        """
        根据指定的groupBox的title从content中删除对应的groupBox
        :param groupBoxTitle: 需要删除的groupBox的title
        :return: None
        """
        groupBox = self.groupBoxMap.get(groupBoxTitle)
        if groupBox is not None:
            self.contentLayout.removeWidget(groupBox)

    def getAllGroupBox(self) -> dict:
        """
        以字典的形式返回所有的groupBox
        :return: dict
        """
        return self.groupBoxMap

    def addDishBoxToGroupBox(self, groupBoxTitle: str, dishBox: DishDetailsBox):
        groupBox: DishDetailsGroupBox = self.groupBoxMap.get(groupBoxTitle)
        if groupBox is not None:
            groupBox.addDishBox(dishBox)


class BottomPopupWidget(QWidget):
    def __init__(self, packageDetails: PackageDetails, *args, **kwargs):
        super(BottomPopupWidget, self).__init__(*args, **kwargs)

        # 使用样式表设置背景颜色
        self.setObjectName("bottom_popup_widget")
        # 主要布局
        layout = QVBoxLayout(self)

        self.frame = QFrame()
        self.frame.setStyleSheet('QFrame {background-color: white;}')
        # frame的布局
        frameLayout = QHBoxLayout(self.frame)

        self.packageDetails = packageDetails

        # 菜品详情
        self.dishDetailsWidget = DishDetailsWidget()

        # 存放所有已经选中的菜品
        self.dishBoxSelectedMap = {}

        # 购物车
        self.shoppingCartWidget = ShoppingCart()

        # 往frame布局中添加dishDetailsWidget和shoppingCartWidget
        frameLayout.addWidget(self.dishDetailsWidget)
        frameLayout.addWidget(self.shoppingCartWidget)

        # 主布局
        layout.addWidget(self.frame)
        # 注册事件
        self.processDishBoxSignal()

    def processDishBoxSignal(self):
        groupBox: DishDetailsGroupBox
        dishBox: DishDetailsBox
        for groupBoxTitle, groupBox in self.dishDetailsWidget.getAllGroupBox().items():
            for dishBoxTitle, dishBox in groupBox.getAllDishBox().items():
                dishBox.checkBoxSignal.connect(self.addDishBoxSelectedToMap)

    @Slot(str, DishDetailsBox, bool)
    def addDishBoxSelectedToMap(self, dishBox: DishDetailsBox, isSelected: bool):
        if isSelected:
            self.dishBoxSelectedMap[dishBox.dishId] = dishBox

            # 构造购物车的商品项
            item = ShoppingCertItem(dishBox.dishId, self.shoppingCartWidget)
            item.setCover("")
            item.setTitle(dishBox.title.text())
            item.setPrice(dishBox.price.text())
            self.shoppingCartWidget.addShoppingCartItem(item)
        elif not isSelected:
            # 删除map中对应的dishBox
            self.dishBoxSelectedMap.pop(dishBox.dishId)
            item = self.shoppingCartWidget.shoppingCartItemMap.get(dishBox.dishId)
            if item is not None:
                self.shoppingCartWidget.deleteShoppingCartItem(dishBox.dishId)

        print(self.dishBoxSelectedMap.keys())

    def processShoppingCartItemSignal(self):
        item: ShoppingCertItem
        for item in self.shoppingCartWidget.getAllItems().values():
            item.shoppingCartItemSignal.connect()

    def toggleCheckBoxState(self, dishBoxId):
        checkBox: QCheckBox = self.dishBoxSelectedMap.get(dishBoxId)
        checkBox.setChecked(False)



class ShoppingCertItem(QWidget):
    """
    购物车中的菜单项
    """
    shoppingCartItemSignal = Signal(str)

    def __init__(self, dishId: str, shoppingCart):
        super().__init__()

        # 设置主窗口大小
        # self.setFixedSize(300, 200)
        # 设置尺寸策略为 Fixed
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # 依附的购物车
        self.shoppingCart = shoppingCart

        # 封面
        self.cover = QLabel()
        self.cover.setFixedSize(100, 100)

        # 菜品数量
        self.dishQuantity = 1

        # 菜品id
        self.dishId = dishId

        # 种类
        self.categoryId = None
        self.categoryName = None

        # 菜品名
        self.title = QLabel()
        self.title.setFixedSize(100, 100)

        # 价格
        self.price = QLabel()
        self.price.setFixedSize(100, 50)

        # 减少数量按钮
        self.reduceQuantityBtn = QPushButton()
        self.reduceQuantityBtn.setFixedSize(50, 50)

        # 显示数量的标签
        self.dishQuantityLabel = QLabel()
        self.dishQuantityLabel.setFixedSize(50, 50)

        # 增加数量的按钮
        self.increaseQuantityBtn = QPushButton()
        self.increaseQuantityBtn.setFixedSize(50, 50)

        # 删除按钮
        self.deleteBtn = QPushButton("删除")
        self.deleteBtn.setFixedSize(100, 50)

        # 水平布局装载 价格和按钮
        priceLayout = QHBoxLayout()
        priceLayout.addWidget(self.price)
        priceLayout.addWidget(self.reduceQuantityBtn)
        priceLayout.addWidget(self.dishQuantityLabel)
        priceLayout.addWidget(self.increaseQuantityBtn)
        priceLayout.addWidget(self.deleteBtn)

        # 垂直布局装载 price_layout 和 title
        titleLayout = QVBoxLayout()
        titleLayout.addWidget(self.title)
        titleLayout.addLayout(priceLayout)

        # 主要布局
        layout = QHBoxLayout(self)
        layout.addWidget(self.cover)
        layout.addLayout(titleLayout)

        self.refreshQuantityLabel()
        # 事件处理
        self.processDeleteEvent()

    def setCover(self, coverPath: str):
        self.cover.setPixmap(QPixmap(coverPath))

    def setTitle(self, title: str):
        self.title.setText(title)

    def setPrice(self, price: str):
        self.price.setText(price)

    def processDeleteEvent(self):
        """
        事件处理
        :return: None
        """
        self.deleteBtn.clicked.connect(self.deleteItemFromShoppingCart)
        self.reduceQuantityBtn.clicked.connect(self.reduceQuantity)
        self.increaseQuantityBtn.clicked.connect(self.increaseQuantity)

    def deleteItemFromShoppingCart(self):
        self.shoppingCart.deleteShoppingCartItem(self.dishId)
        self.shoppingCartItemSignal.emit(self.dishId)

    def refreshQuantityLabel(self):
        """
        刷新数量视图显示的内容
        :return: None
        """
        self.dishQuantityLabel.setText(str(self.dishQuantity))

    def reduceQuantity(self):
        """
        减少商品数量
        :return: None
        """
        if self.dishQuantity > 1:
            self.dishQuantity -= 1
        else:
            self.deleteItemFromShoppingCart()
        self.refreshQuantityLabel()
        self.shoppingCart.setCheckoutPrice()

    def increaseQuantity(self):
        """
        增加商品数量
        :return: None
        """
        self.dishQuantity += 1
        self.refreshQuantityLabel()
        self.shoppingCart.setCheckoutPrice()

    def emptyQuantity(self):
        """
        清空商品数量
        :return: None
        """
        self.dishQuantity = 0
        self.refreshQuantityLabel()


class ShoppingCart(QWidget):
    def __init__(self):
        super().__init__()

        # 设置主窗口大小
        # self.setFixedSize(300, 500)
        # 设置尺寸策略为 Fixed
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # 标题
        self.title = QLabel("购物车")
        self.title.setFixedSize(300, 100)

        # 清空购物车按钮
        self.emptyBtn = QPushButton("清空购物车")
        self.emptyBtn.setFixedSize(100, 50)

        # 水平布局装载标题栏
        titleLayout = QHBoxLayout()
        titleLayout.addWidget(self.title)
        titleLayout.addWidget(self.emptyBtn)

        # 购物车项的Map
        self.shoppingCartItemMap = {}

        # 购物车项的布局
        self.itemLayout = QVBoxLayout()

        # 滚轮布局装载所有的购物车项
        self.scrollContent = QWidget()
        self.scrollContent.setLayout(self.itemLayout)
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.scrollContent)
        self.scrollArea.setWidgetResizable(True)

        self.itemScrollLayout = QVBoxLayout()
        self.itemScrollLayout.addWidget(self.scrollArea)

        # 结算金额
        self.totalPrice = 0
        self.checkoutPrice = QLabel("0.0")
        self.checkoutPrice.setFixedSize(300, 100)

        # 结算按钮
        self.checkoutBtn = QPushButton("结算")
        self.checkoutBtn.setFixedSize(100, 50)

        # 布局装载结算栏
        checkoutLayout = QHBoxLayout()
        checkoutLayout.addWidget(self.checkoutPrice)
        checkoutLayout.addWidget(self.checkoutBtn)

        # 购物车主布局
        layout = QVBoxLayout(self)
        layout.addLayout(titleLayout)
        layout.addLayout(self.itemScrollLayout)
        layout.addLayout(checkoutLayout)

        # 事件处理
        self.processEvent()

    def setCheckoutPrice(self):
        """
        计算购物车中商品的总价格
        :return: None
        """
        item: ShoppingCertItem
        self.totalPrice = 0
        for itemTitle, item in self.getAllItems().items():
            self.totalPrice += round(float(item.price.text()) * item.dishQuantity, 2)
        self.checkoutPrice.setText(str(self.totalPrice))

    def addShoppingCartItem(self, item: ShoppingCertItem):
        """
        往购物车中添加商品项
        :param item: 需要添加的商品项
        :return: None
        """
        self.itemLayout.addWidget(item)
        filtered_keys = [key for key in self.shoppingCartItemMap.keys() if key.startswith(item.dishId)]
        if len(filtered_keys) == 0:
            self.shoppingCartItemMap[item.dishId] = item
        else:
            self.shoppingCartItemMap[f"{item.dishId}_{len(filtered_keys)}"] = item
        print(self.shoppingCartItemMap.keys())
        self.setCheckoutPrice()

    def deleteShoppingCartItem(self, itemId: str):
        """
        删除购物车中的商品项
        :param itemId: 商品id
        :return: None
        """
        item = self.shoppingCartItemMap.pop(itemId)
        if item is not None:
            # 从布局中移除子组件
            self.itemLayout.removeWidget(item)
            # 断开与父组件的连接，以确保子组件能够被正确删除
            item.setParent(None)
            # 使用 deleteLater() 从内存中删除子组件
            item.deleteLater()

        # 更新购物车总价
        self.setCheckoutPrice()

    def getAllItems(self) -> dict:
        """
        返回购物车中所有的商品
        :return: dict
        """
        return self.shoppingCartItemMap

    def emptyShoppingCart(self):
        """
        删除购物车中所有的商品
        :return: None
        """
        for itemTitle in self.shoppingCartItemMap.keys():
            item = self.shoppingCartItemMap.get(itemTitle)
            if item is not None:
                # 从布局中移除子组件
                self.itemLayout.removeWidget(item)
                # 断开与父组件的连接，以确保子组件能够被正确删除
                item.setParent(None)
                # 使用 deleteLater() 从内存中删除子组件
                item.deleteLater()

        # 更新购物车总价
        self.setCheckoutPrice()
        # 清空购物车Map
        self.shoppingCartItemMap.clear()

    def processEvent(self):
        self.emptyBtn.clicked.connect(self.emptyShoppingCart)


if __name__ == '__main__':
    app = QApplication([])
    side_bar = MainWindow()
    side_bar.show()
    app.exec()

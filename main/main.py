from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, QIcon, QFont, QCursor, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QSizePolicy, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, \
    QLabel, QPushButton

from client.client import Client
from ui.affordablePackage_window import AffordablePackage
from ui.bottom_popup_window import PackageDetails, ShoppingCart
from ui.change_personal_info_window import InfoChange
from ui.home_window import HomePage ,read_binary_files_in_directory
from ui.latestOffer_window import LatestOffer, LatestOfferDetails
from ui.menuOrder_window import MenuOrder
from ui.orderManagement_window import OrderMessageWidget
from utils.utils import Utils


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置主窗口大小
        self.m_Position = None
        self.m_flag = None
        self.setFixedSize(1200, 750)
        # 设置尺寸策略为Fixed
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setObjectName("main_window")
        self.setStyleSheet(Utils.read_qss_file("../res/qss/main_window.qss"))

        # 隐藏最外层窗口边框
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # 设置标题
        self.setWindowTitle("McDonald's")
        # 设置图标
        icon = QIcon("../res/images//images (12).png")
        self.setWindowIcon(icon)

        # 修改个人信息窗口
        self.infoChangeWidget = InfoChange(self)

        self.client = Client()
        # 用户
        self.user = None
        # 优惠
        self.offers_dict = self.client.getAllOffers()
        # 套餐
        self.packages_dict = self.client.getAllPackages()
        # 菜单
        self.menu = self.client.getAllDishes()
        # 将购物车应用于全局
        self.shoppingCartItemMap = {}

        # 添加QListWidget
        self.listWidget = QListWidget(self)
        self.listWidget.setObjectName("side_bar")
        self.listWidget.setStyleSheet(Utils.read_qss_file("../res/qss/side_bar.qss"))
        items_data = [("首页", "../res/icons/首页.png"),
                      ("最新优惠", "../res/icons/优惠券_文字.png"),
                      ("精选套餐", "../res/icons/精选优品.png"),
                      ("菜单点餐", "../res/icons/菜单.png"),
                      ("购物车管理", "../res/icons/购物车.png"),
                      ("订单管理", "../res/icons/查看订单.png"),
                      ("修改个人信息", "../res/icons/个人_fill.png")]
        for item_text, icon_path in items_data:
            item = QListWidgetItem(item_text)
            item.setFont(QFont("微软雅黑", 13, QFont.Weight.Normal))  # 设置字体
            icon = QIcon(icon_path)
            item.setIcon(icon)  # 设置图标
            self.listWidget.addItem(item)
        self.listWidget.setIconSize(QSize(25, 25))

        self.listWidget.currentItemChanged.connect(self.showSelectedPage)

        self.showPage = QVBoxLayout()

        # 设置图标button
        iconBtn = QPushButton("McDonald's")
        icon = QIcon("../res/images//images (12).png")
        iconBtn.setIcon(icon)
        iconBtn.setIconSize(QSize(35, 35))
        iconBtn.setObjectName("icon_btn")

        # 顶栏
        topBar = QWidget()
        topBar.setObjectName("top_bar")
        topBar.setStyleSheet(Utils.read_qss_file("../res/qss/top_bar.qss"))
        top_label = QLabel()
        top_label.setText("Welcome to McDonald's, let's have a good time ordering together 😊")
        top_label.setObjectName("top_bar")
        self.close_btn = QPushButton()
        self.close_btn.setFixedSize(QSize(30, 30))
        self.close_btn.setIcon(QIcon("../res/icons/关闭.png"))
        self.close_btn.setIconSize(QSize(25, 25))

        self.maximum_btn = QPushButton()
        self.maximum_btn.setFixedSize(QSize(30, 30))
        self.maximum_btn.setIcon(QIcon("../res/icons/最大化.png"))
        self.maximum_btn.setIconSize(QSize(20, 20))

        self.minimum_btn = QPushButton()
        self.minimum_btn.setFixedSize(QSize(30, 30))
        self.minimum_btn.setIcon(QIcon("../res/icons/缩小.png"))
        self.minimum_btn.setIconSize(QSize(30, 30))

        topLayout = QHBoxLayout(topBar)
        topLayout.addWidget(top_label, 10)
        topLayout.addWidget(self.minimum_btn, 2)
        topLayout.addWidget(self.maximum_btn, 2)
        topLayout.addWidget(self.close_btn, 2)

        self.close_btn.clicked.connect(self.close)
        self.maximum_btn.clicked.connect(self.toggleMaximized)
        self.minimum_btn.clicked.connect(self.showMinimized)

        # 左半区布局装载侧边栏
        self.side_bar = QWidget()
        self.side_bar.setObjectName("side_bar")
        self.side_bar.setStyleSheet(Utils.read_qss_file("../res/qss/side_bar.qss"))
        sideLayout = QVBoxLayout(self.side_bar)
        sideLayout.addWidget(iconBtn)
        sideLayout.addWidget(self.listWidget)

        # 右半区布局
        self.right_bar = QWidget()
        self.right_bar.setObjectName("right_bar")
        self.right_bar.setStyleSheet(Utils.read_qss_file("../res/qss/right_bar.qss"))
        rightLayout = QVBoxLayout(self.right_bar)
        rightLayout.addWidget(topBar)
        rightLayout.addLayout(self.showPage)

        # 主布局
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.side_bar, 2)
        main_layout.addWidget(self.right_bar, 8)

        # 将布局管理器设置给主窗口
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        central_widget.setObjectName("main_widget")
        central_widget.setStyleSheet(Utils().read_qss_file("../res/qss/main_window.qss"))
        self.setCentralWidget(central_widget)
        self.listWidget.setCurrentRow(0)
        self.showSelectedPage()

    def showSelectedPage(self):
        # 移除QVBoxLayout中的所有组件
        while self.showPage.count():
            item = self.showPage.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 获取当前选中的项
        selectedItem = self.listWidget.currentItem()
        if selectedItem is not None:
            # 获取名称
            itemText = selectedItem.text()
            if itemText == "首页":
                homePage = HomePage()

                file_paths = read_binary_files_in_directory("../res/McDonald/homepage")
                homePage.load_covers(file_paths)

                self.showPage.addWidget(homePage)
            elif itemText == "最新优惠":
                latestOffer = LatestOffer()
                for value in self.offers_dict.values():
                    latestOfferDetails = LatestOfferDetails(
                        cover=QPixmap(value.get("img_path")),
                        title=value.get("simplified_title"),
                        desc=value.get("simplified_details"),
                        offers_dict=self.offers_dict,
                        shoppingCartItemMap=self.shoppingCartItemMap,
                        user=self.user
                    )
                    latestOffer.addLatestOffer(latestOfferDetails)
                self.showPage.addWidget(latestOffer)
            elif itemText == "精选套餐":
                self.showPage.addWidget(AffordablePackage(self.shoppingCartItemMap, self.user, self.packages_dict))
            elif itemText == "菜单点餐":
                categoryList = []
                for category, dishesList in self.menu.items():
                    if len(dishesList) != 0:
                        categoryList.append(category)

                menuOrderWidget = MenuOrder(categoryList)
                for category, dishesList in self.menu.items():
                    if len(dishesList) != 0:
                        for dish in dishesList:
                            if dish[4] is not None:
                                dishBox = PackageDetails(self, str(dish[0]), str(dish[4]), str(dish[1]), str(dish[5]), str(dish[3]),
                                                         str(dish[6]), dish[7], self.shoppingCartItemMap, self.user)
                                menuOrderWidget.addDishToGroupBox(category, dishBox)

                self.showPage.addWidget(menuOrderWidget)
            elif itemText == "购物车管理":
                self.showPage.addWidget(ShoppingCart(self.shoppingCartItemMap, self.user))
            elif itemText == "订单管理":
                self.showPage.addWidget(OrderMessageWidget(self.user))
            elif itemText == "修改个人信息":
                self.infoChangeWidget.show()

    def toggleMaximized(self):
        """
        切换窗口 最大/最小
        :return: none
        """
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.MouseButton.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))


if __name__ == "__main__":
    app = QApplication([])

    main_widget = MyMainWindow()
    main_widget.show()

    app.exec()

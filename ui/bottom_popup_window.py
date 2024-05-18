from PySide6.QtCore import Signal, Slot, QSize
from PySide6.QtGui import QPixmap, QFont, Qt, QIcon
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QFrame, QVBoxLayout, QWidget, QScrollArea, QPushButton, QLabel, QSizePolicy, \
    QGridLayout, QButtonGroup, QGroupBox, QSpacerItem, QTextBrowser

from common.user import User
from ui.main_window import CDrawer
from ui.purchase_window import PurchaseWindow
from utils.utils import Utils


class ShoppingCertItem(QWidget):
    """
    购物车中的菜单项
    """
    shoppingCartItemSignal = Signal(str)

    def __init__(self, dishId: str, shoppingCart):
        super().__init__()

        # 设置主窗口大小
        self.setFixedHeight(150)
        # 设置尺寸策略为 Fixed

        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        # 依附的购物车
        self.shoppingCart = shoppingCart

        # 封面
        self.coverPath = None
        self.cover = QLabel()
        self.cover.setObjectName("shopping_cart_item_cover")
        self.cover.setFixedSize(100, 100)
        self.cover.setScaledContents(True)

        # 菜品数量
        self.dishQuantity = 1

        # 菜品id
        self.dishId = dishId

        # 种类
        self.categoryId = None
        self.categoryName = None

        # 菜品名
        self.title = QLabel()
        self.title.setObjectName("shopping_cart_item_title")
        self.title.setFixedSize(500, 30)

        # 价格
        self.price = QLabel()
        self.price.setObjectName("shopping_cart_item_price")
        self.price.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.price.setFixedHeight(50)

        # 减少数量按钮
        self.reduceQuantityBtn = QPushButton()
        self.reduceQuantityBtn.setObjectName("reduce_btn")
        self.reduceQuantityBtn.setIcon(QIcon("../res/icons/减少.png"))
        self.reduceQuantityBtn.setIconSize(QSize(10, 10))
        self.reduceQuantityBtn.setFixedSize(20, 20)

        # 显示数量的标签
        self.dishQuantityLabel = QLabel()
        self.dishQuantityLabel.setObjectName("dish_quantity")
        self.dishQuantityLabel.setFixedSize(30, 20)

        # 增加数量的按钮
        self.increaseQuantityBtn = QPushButton()
        self.increaseQuantityBtn.setObjectName("increase_btn")
        self.increaseQuantityBtn.setIcon(QIcon("../res/icons/加.png"))
        self.increaseQuantityBtn.setIconSize(QSize(10, 10))
        self.increaseQuantityBtn.setFixedSize(20, 20)

        # 删除按钮
        self.deleteBtn = QPushButton("删除")
        self.deleteBtn.setObjectName("delete_btn")
        self.deleteBtn.setFixedSize(100, 30)

        # 水平布局装载 价格和按钮
        priceLayout = QHBoxLayout()
        priceLayout.addWidget(self.price)
        priceLayout.setAlignment(self.price, Qt.AlignmentFlag.AlignLeft)
        priceLayout.addWidget(self.reduceQuantityBtn)
        priceLayout.addWidget(self.dishQuantityLabel)
        priceLayout.addWidget(self.increaseQuantityBtn)
        priceLayout.addWidget(self.deleteBtn)

        # 垂直布局装载 price_layout 和 title
        titleLayout = QVBoxLayout()
        titleLayout.addWidget(self.title)
        titleLayout.addLayout(priceLayout)

        # 主要布局
        main_widget = QWidget()
        main_widget.setObjectName("shopping_cart_item")
        main_widget.setStyleSheet(Utils().read_qss_file("../res/qss/shopping_cart.qss"))
        layout = QHBoxLayout(main_widget)
        layout.addWidget(self.cover)
        layout.addLayout(titleLayout)

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(main_widget)

        self.refreshQuantityLabel()
        # 事件处理
        self.processDeleteEvent()

    def setCover(self, coverPath: str):
        self.coverPath = coverPath
        self.cover.setPixmap(QPixmap(coverPath))

    def setTitle(self, title: str):
        self.title.setText(title)

    def setPrice(self, price: str):
        self.price.setText(price)

    def setCategoryId(self, categoryId: str):
        self.categoryId = categoryId

    def setCategoryName(self, categoryName: str):
        self.categoryName = categoryName

    def setDishQuantity(self, quantity: int):
        self.dishQuantity = quantity
        self.dishQuantityLabel.setText(str(self.dishQuantity))

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
            self.shoppingCart.shoppingCartItemMap[str(self.dishId)]["dishQuantity"] = self.dishQuantity
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
        self.shoppingCart.shoppingCartItemMap[str(self.dishId)]["dishQuantity"] = self.dishQuantity
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
    def __init__(self, shoppingCartItemMap: dict, user: User):
        super().__init__()

        # 设置主窗口大小
        # self.setFixedSize(300, 500)
        # 设置尺寸策略为 Fixed
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.user = user

        self.shoppingCartItemMap = shoppingCartItemMap
        self.shoppingCartItemBoxMap = {}

        # 图标
        self.title = QPushButton("购物车")
        self.title.setObjectName("title")
        self.title.setIcon(QIcon("../res/animations/trolley.png"))
        self.title.setIconSize(QSize(60, 60))
        self.title.setFixedSize(150, 60)

        # 标题
        self.info = QLabel("欢迎来到购物车, 一起愉快购物吧😊~~~~~")
        self.info.setObjectName("info")
        info_font = QFont("微软雅黑", 14, QFont.Weight.Normal)
        self.info.setFont(info_font)

        # 清空购物车按钮
        self.emptyBtn = QPushButton("清空购物车")
        self.emptyBtn.setObjectName("empty_btn")
        self.emptyBtn.setFixedSize(100, 50)

        # 水平布局装载标题栏
        titleLayout = QHBoxLayout()
        titleLayout.addWidget(self.title, 1)
        titleLayout.setAlignment(self.title, Qt.AlignmentFlag.AlignLeft)
        titleLayout.addWidget(self.info, 10)
        titleLayout.addWidget(self.emptyBtn, 1)

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
        self.checkoutPrice.setObjectName("checkout_price")
        self.checkoutPrice.setFixedSize(300, 50)

        # 结算按钮
        self.checkoutBtn = QPushButton("结算\nCheckout Cart")
        self.checkoutBtn.setObjectName("checkout_btn")
        self.checkoutBtn.setFixedSize(150, 50)

        # 布局装载结算栏
        checkoutWidget = QWidget()
        checkoutWidget.setObjectName("checkout_widget")
        checkoutLayout = QHBoxLayout(checkoutWidget)
        checkoutLayout.addWidget(self.checkoutPrice)
        checkoutLayout.setAlignment(self.checkoutPrice, Qt.AlignmentFlag.AlignLeft)
        checkoutLayout.addWidget(self.checkoutBtn)
        checkoutLayout.setAlignment(self.checkoutBtn, Qt.AlignmentFlag.AlignRight)

        # 购物车主布局
        main_widget = QWidget()
        main_widget.setObjectName("shopping_cart")
        main_widget.setStyleSheet(Utils().read_qss_file("../res/qss/shopping_cart.qss"))
        layout = QVBoxLayout(main_widget)
        layout.addLayout(titleLayout)
        layout.addLayout(self.itemScrollLayout)
        layout.addWidget(checkoutWidget)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(main_widget)

        item: dict
        for item in shoppingCartItemMap.values():
            cartItem = ShoppingCertItem(item.get("dishId"), self)
            cartItem.setCover(item.get("coverPath"))
            cartItem.setTitle(item.get("title"))
            cartItem.setPrice(item.get("price"))
            cartItem.setCategoryId(item.get("categoryId"))
            cartItem.setCategoryName(item.get("categoryName"))
            cartItem.setDishQuantity(item.get("dishQuantity"))
            self.addShoppingCartItem(cartItem, True)

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
            self.totalPrice += round(float(item.price.text()[1:]) * item.dishQuantity, 2)
        self.checkoutPrice.setText(
            "总价格: ${:.2f}".format(self.totalPrice)
        )

    def addShoppingCartItem(self, item: ShoppingCertItem, isInit: bool):
        """
        往购物车中添加商品项
        :param item: 需要添加的商品项
        :param isInit: 是否是初始化
        :return: None
        """
        self.itemLayout.addWidget(item)
        if self.shoppingCartItemBoxMap.get(item.dishId) is None:
            self.shoppingCartItemBoxMap[item.dishId] = item

        if not isInit:
            # 将购物车项加入到Map中
            newItem = {"dishId": item.dishId,
                       "coverPath": item.coverPath,
                       "title": item.title.text(),
                       "price": item.price.text(),
                       "categoryId": item.categoryId,
                       "categoryName": item.categoryName,
                       "dishQuantity": item.dishQuantity}
            self.shoppingCartItemMap[item.dishId] = newItem
        self.setCheckoutPrice()

    def deleteShoppingCartItem(self, itemId: str):
        """
        删除购物车中的商品项
        :param itemId: 商品id
        :return: None
        """
        item = self.shoppingCartItemBoxMap.pop(itemId)
        if item is not None:
            # 从布局中移除子组件
            self.itemLayout.removeWidget(item)
            # 断开与父组件的连接，以确保子组件能够被正确删除
            item.setParent(None)
            # 使用 deleteLater() 从内存中删除子组件
            item.deleteLater()
        self.shoppingCartItemMap.pop(itemId)
        # 更新购物车总价
        self.setCheckoutPrice()

    def getAllItems(self) -> dict:
        """
        返回购物车中所有的商品
        :return: dict
        """
        return self.shoppingCartItemBoxMap

    def emptyShoppingCart(self):
        """
        删除购物车中所有的商品
        :return: None
        """
        for itemTitle in self.shoppingCartItemBoxMap.keys():
            item = self.shoppingCartItemBoxMap.get(itemTitle)
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
        self.shoppingCartItemBoxMap.clear()
        self.shoppingCartItemMap.clear()

    def checkout(self):
        # 创建子窗口，这里要使用 PurchaseWindow 类的实例
        purchase_window = PurchaseWindow(self.shoppingCartItemMap, self.user)
        purchase_window.setWindowTitle('购买窗口')

        # 显示 PurchaseWindow 实例
        purchase_window.exec()

    def processEvent(self):
        self.emptyBtn.clicked.connect(self.emptyShoppingCart)
        self.checkoutBtn.clicked.connect(self.checkout)


class PackageDetails(QWidget):
    def __init__(self, parent_widget: QWidget, dishId: str, coverPath: str, title: str, discount: str, current: str, categoryId: str,
                 categoryName: str, shoppingCartItemMap: dict, user: User):
        super().__init__()
        self.parent_widget = parent_widget
        # 设置主窗口大小
        self.setFixedHeight(200)
        # 设置尺寸策略为 Fixed
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        self.shoppingCartItemMap = shoppingCartItemMap
        self.user = user
        # 封面
        self.cover = QLabel()
        self.coverPath = coverPath
        self.cover.setPixmap(QPixmap(coverPath))
        self.cover.setObjectName("package_details_cover")
        self.cover.setFixedSize(200, 200)
        self.cover.setScaledContents(True)

        # 餐名
        self.title = QLabel()
        self.title.setText(title)
        self.title.setObjectName("package_details_title")
        self.title.setFixedHeight(50)
        # 套餐标题的字体样式
        self.title_font = QFont()
        self.title_font.setPointSize(14)
        self.title_font.setBold(True)
        self.title.setFont(self.title_font)

        # 菜品id
        self.dishId = dishId

        # 折扣
        self.discount = QPushButton()
        self.discount.setText(discount + "折")
        self.discount.setObjectName("package_details_discount")
        self.discount.setFixedSize(50, 20)

        # 现价
        self.current = QLabel()
        self.current.setText("$" + current)
        self.current.setObjectName("package_details_current")
        self.current.setFixedHeight(100)

        # 原价
        self.origin = QLabel()
        formatted_text = "${:.2f}".format(float(current) / (float(discount) / 10))
        self.origin.setText(formatted_text)
        self.origin.setObjectName("package_details_origin")
        self.origin.setFixedHeight(100)

        # 类别
        self.categoryId = categoryId
        self.categoryName = categoryName

        # 购买按钮
        self.buy = QPushButton("选规格")
        self.buy.setObjectName("package_details_buy")
        # self.buy.setFixedSize(50, 30)

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
        widget = QWidget()
        widget.setObjectName("package_details")
        widget.setStyleSheet(Utils().read_qss_file("../res/qss/package_details.qss"))
        self.main_layout = QHBoxLayout(widget)
        self.main_layout.addWidget(self.cover)
        self.main_layout.addLayout(self.layout)
        self.main_layout.setAlignment(Qt.AlignLeft)

        layout = QHBoxLayout(self)
        layout.addWidget(widget)
        self.buy.clicked.connect(self.showBottomPopup)

    def setCover(self, cover_file_name):
        """
        设置优惠详情的封面
        :param cover_file_name:
        :return:
        """
        self.cover.setPixmap(QPixmap(cover_file_name))

    def setTitle(self, title):
        """
        设置标题
        :param title:
        :return:
        """
        self.title.setText(title)

    def setDiscount(self, discount):
        """
        设置折扣
        :param discount:
        :return:
        """
        self.discount.setText(discount)

    def setCurrent(self, current):
        """
        设置现价
        :param current:
        :return:
        """
        self.current.setText(current)

    def setOrigin(self, origin):
        """
        设置现价
        :param origin:
        :return:
        """
        self.origin.setText(origin)

    def showBottomPopup(self):
        if not hasattr(self, 'topDrawer'):
            # 判断是否已经拥有该属性，如果没有就创建
            self.bottomDrawer = CDrawer(self, stretch=3 / 4, direction=CDrawer.BOTTOM)
            self.bottomDrawer.setWidget(BottomPopupWidget(self, self.shoppingCartItemMap, self.user))
        self.bottomDrawer.show()


class DishDetailsBox(QWidget):
    """
    装载菜品的盒子
    """
    checkBoxSignal = Signal(QWidget, bool)

    def __init__(self, dishId: str, coverPath: str, title: str, price: str, categoryId: str, categoryName: str, user: User):
        super().__init__()

        # 设置主窗口大小
        self.setFixedSize(150, 200)
        # 设置尺寸策略为 Fixed
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.user = user

        # 复选框
        self.checkBox = QCheckBox()
        # 自定义checkBox信号
        self.checkBox.stateChanged.connect(self.checkBoxStateChanged)

        # 菜品id
        self.dishId = dishId

        # 菜品种类
        self.categoryId = categoryId
        self.categoryName = categoryName

        # 封面
        self.cover = QLabel()
        self.cover.setObjectName("dish_details_box_cover")
        self.coverPath = coverPath
        self.cover.setPixmap(QPixmap(coverPath))
        self.cover.setScaledContents(True)
        self.cover.setFixedSize(100, 100)
        # 标题
        self.title = QLabel(title)
        self.title.setObjectName("dish_details_box_title")
        # self.title.setFixedSize(100, 50)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.title.setWordWrap(True)

        # 价格
        self.price = QLabel(price)
        self.price.setObjectName("dish_details_box_price")
        # self.price.setFixedSize(100, 50)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.price.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.title.setWordWrap(True)

        # 主widget
        self.main_widget = QWidget()
        self.main_widget.setObjectName("dish_details_box_main_widget")
        self.main_widget.setStyleSheet(Utils().read_qss_file("../res/qss/dish_details_box.qss"))
        layout = QVBoxLayout(self.main_widget)
        layout.addWidget(self.checkBox)
        layout.addWidget(self.cover)
        layout.addWidget(self.title)
        layout.addWidget(self.price)

        layout.setAlignment(self.checkBox, Qt.AlignmentFlag.AlignRight)
        layout.setAlignment(self.cover, Qt.AlignmentFlag.AlignHCenter)
        layout.setAlignment(self.title, Qt.AlignmentFlag.AlignHCenter)
        layout.setAlignment(self.price, Qt.AlignmentFlag.AlignHCenter)

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.main_widget)

    @Slot(int)
    def checkBoxStateChanged(self, state):
        if state == 2:
            # 发出自定义信号
            self.checkBoxSignal.emit(self, True)
            self.main_widget.setStyleSheet(Utils().read_qss_file("../res/qss/dish_details_box_checked.qss"))
        else:
            # 发出自定义信号
            self.checkBoxSignal.emit(self, False)
            self.main_widget.setStyleSheet(Utils().read_qss_file("../res/qss/dish_details_box.qss")
            )


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
        self.groupBox.setFixedWidth(350)
        self.groupBox.setObjectName("dish_details_groupBox")
        self.groupBox.setStyleSheet(Utils().read_qss_file("../res/qss/bottom_popup.qss"))
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
        # self.setFixedSize(400, 500)
        # 设置尺寸策略为 Fixed
        # self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # 封面
        self.cover = QLabel()
        self.cover.setFixedSize(350, 350)
        self.cover.setObjectName("dish_details_cover")
        self.cover.setScaledContents(True)

        # 标题
        self.title = QLabel()
        self.title.setObjectName("dish_details_title")
        self.title.setFixedSize(250, 50)

        # 管理groupBox的map
        self.groupBoxMap = {}

        # 垂直布局配合滚轮布局
        self.contentLayout = QVBoxLayout()
        self.contentLayout.addWidget(self.cover)
        self.contentLayout.addWidget(self.title)

        self.scrollContent = QWidget()
        self.scrollContent.setFixedWidth(378)
        self.scrollContent.setObjectName("dish_details_scroll_widget")
        self.scrollContent.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.scrollContent.setLayout(self.contentLayout)
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.scrollContent)
        self.scrollArea.setWidgetResizable(True)

        main_widget = QWidget()
        main_widget.setObjectName("dish_details_main_widget")
        main_widget.setStyleSheet(Utils().read_qss_file("../res/qss/bottom_popup.qss"))
        layout = QVBoxLayout(main_widget)
        layout.addWidget(self.scrollArea)

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(main_widget)

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
        groupBox.setFixedWidth(250)
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

    def setCover(self, coverPath):
        pixmap = QPixmap(coverPath)
        self.cover.setPixmap(pixmap)

    def setTitle(self, title):
        self.title.setText(title)


class BottomPopupWidget(QWidget):
    def __init__(self, packageDetails: PackageDetails, shoppingCartItemMap: dict, user: User, *args, **kwargs):
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
        self.user = user
        # 菜品详情
        self.dishDetailsWidget = DishDetailsWidget()

        # 存放所有已经选中的菜品
        self.dishBoxSelectedMap = {}

        # 购物车
        self.shoppingCartWidget = ShoppingCart(shoppingCartItemMap, self.user)

        # 往frame布局中添加dishDetailsWidget和shoppingCartWidget
        frameLayout.addWidget(self.dishDetailsWidget, 4)
        frameLayout.addWidget(self.shoppingCartWidget, 7)

        # 主布局
        layout.addWidget(self.frame)

        # 载入菜品
        self.loadPackageDetails()

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
            item.setCover(dishBox.coverPath)
            item.setTitle(dishBox.title.text())
            item.setPrice(dishBox.price.text())
            self.shoppingCartWidget.addShoppingCartItem(item, False)
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

    def loadPackageDetails(self):
        """
        载入菜品详细信息
        :return:
        """
        dishGroupBox = DishDetailsGroupBox(self.packageDetails.categoryName)
        dishBox = DishDetailsBox(self.packageDetails.dishId,
                                 self.packageDetails.coverPath,
                                 self.packageDetails.title.text(),
                                 self.packageDetails.current.text(),
                                 self.packageDetails.categoryId,
                                 self.packageDetails.categoryName,
                                 self.user)
        dishGroupBox.addDishBox(dishBox)
        self.dishDetailsWidget.addDishGroupBox(dishGroupBox)
        dishGroupBox.dishBoxMap[self.packageDetails.title.text()] = dishBox
        self.dishDetailsWidget.groupBoxMap[self.packageDetails.categoryName] = dishGroupBox

        # 设置详情
        self.dishDetailsWidget.setCover(self.packageDetails.coverPath)
        self.dishDetailsWidget.setTitle(self.packageDetails.title.text())
        self.processDishBoxSignal()

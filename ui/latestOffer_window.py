from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QSizePolicy, QWidget, QScrollArea, QGridLayout

from common.common import CDrawer
from common.user import User
from ui.bottom_popup_window import BottomPopupWidget, PackageDetails, ShoppingCertItem
from utils.utils import Utils


class LatestOfferDetails(QWidget):
    def __init__(self, cover: QPixmap, title: str, desc: str, offers_dict: dict, shoppingCartItemMap: dict, user: User):
        super().__init__()

        # 设置主窗口大小
        # self.setFixedSize(400, 600)
        # 设置尺寸策略为 Fixed
        # self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setObjectName("box_widget")
        self.setStyleSheet(Utils().read_qss_file("../res/qss/latest_offers.qss"))

        self.offers_dict = offers_dict
        self.shoppingCartItemMap = shoppingCartItemMap
        self.uer = user

        # 封面
        self.cover = QLabel()
        self.cover.setPixmap(cover)
        self.cover.setFixedSize(400, 300)
        self.cover.setScaledContents(True)

        # 字体
        self.title_font = QFont()
        self.title_font.setPointSize(16)
        self.title_font.setBold(True)

        # 标题
        self.title = QLabel()
        self.title.setText(title)
        self.title.setFixedWidth(400)
        self.title.setFont(self.title_font)
        self.title.setObjectName("latest_offer_title")
        self.title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.title.setWordWrap(True)

        # 字体
        self.desc_font = QFont()
        self.desc_font.setPointSize(12)
        self.desc_font.setBold(False)

        # 描述
        self.desc = QLabel()
        self.desc.setText(desc)
        self.desc.setFixedWidth(400)
        self.desc.setFont(self.desc_font)
        self.desc.setWordWrap(True)
        self.desc.setObjectName("latest_offer_desc")
        self.desc.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # 购买按钮
        self.buy = QPushButton()
        self.buy.setObjectName("latest_offer_buy")
        self.buy.setText("购买")

        self.initWidget()
        self.buy.clicked.connect(self.buy_clicked)

    def initWidget(self):
        main_widget = QWidget()
        main_widget.setObjectName("latest_offer_box")
        layout = QVBoxLayout(main_widget)
        layout.addWidget(self.cover)
        layout.addWidget(self.title)
        layout.addWidget(self.desc)
        layout.addWidget(self.buy)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(main_widget)

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

    def setDesc(self, desc):
        """
        设置描述
        :param desc:
        :return:
        """
        self.desc.setText(desc)

    def buy_clicked(self):
        if not hasattr(self, 'topDrawer'):
            # 判断是否已经拥有该属性，如果没有就创建
            self.bottomDrawer = CDrawer(self, stretch=3 / 4, direction=CDrawer.BOTTOM)
            title = self.title.text()
            packageDetails = PackageDetails(
                parent_widget=self,
                dishId="offer-"+title,
                coverPath=self.offers_dict.get(title).get("img_path"),
                title=title,
                discount=str(self.offers_dict.get(title).get("discount")),
                current=str(self.offers_dict.get(title).get("price")),
                categoryId="offers-"+title,
                categoryName="offers",
                shoppingCartItemMap=self.shoppingCartItemMap,
                user=self.uer
            )
            self.bottomDrawer.setWidget(BottomPopupWidget(packageDetails, self.shoppingCartItemMap, self.uer))
        self.bottomDrawer.show()



class LatestOffer(QWidget):
    def __init__(self):
        super().__init__()

        # 设置主窗口大小
        # self.setFixedSize(870, 750)
        # 设置尺寸策略为 Fixed
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.layout = QVBoxLayout(self)
        self.setStyleSheet(Utils().read_qss_file("../res/qss/latest_offers.qss"))

        # 主图片
        self.main_cover = QLabel()
        self.main_cover.setFixedSize(900, 400)
        self.main_cover.setPixmap(QPixmap("../res/images/images (35).png"))
        self.main_cover.setScaledContents(True)

        # 创建网格布局放置图片
        self.grid_layout = QGridLayout()
        self.grid_layout.setObjectName("grid_layout")

        self.main_layout = QVBoxLayout()

        self.scroll_area = QScrollArea()

        # 网格中已经存放的组件数量
        self.size = 0

        # 设置每行显示的图片数量
        self.cover_per_row = 2

        # 设置map管理所有的latestOffer
        self.latestOfferDetailsMap = {}

        self.initWidget()

    def initWidget(self):
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

    def setColumnCapacity(self, capacity):
        """
        设置网格布局中每行显示的个数
        :param capacity: 每行个数
        :return: none
        """
        self.cover_per_row = capacity

    def addLatestOffer(self, offerDetails: LatestOfferDetails):
        """
        在网格中设置对应的套餐详情
        :param offerDetails: 套餐详情对象
        :return: none
        """
        row = self.size // self.cover_per_row
        col = self.size % self.cover_per_row
        self.grid_layout.addWidget(offerDetails, row, col)
        self.latestOfferDetailsMap[offerDetails.title.text()] = offerDetails
        self.size += 1

    def deleteLatestOffer(self, offerDetailsTitle: str):
        offerDetails = self.latestOfferDetailsMap.pop(offerDetailsTitle)
        if offerDetails is not None:
            self.grid_layout.removeWidget(offerDetails)
            self.size -= 1

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QSizePolicy, QSpacerItem, QPushButton, QLabel, QWidget, QScrollArea

from common.user import User
from ui.bottom_popup_window import BottomPopupWidget, PackageDetails
from utils.utils import Utils


class AffordablePackage(QWidget):
    def __init__(self, shoppingCartItemMap: dict, user: User, packages_dict: dict):
        super().__init__()

        # 设置主窗口大小
        # self.setFixedSize(870, 640)
        # 设置尺寸策略为 Fixed
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.layout = QVBoxLayout(self)
        # 装载整体的布局
        self.main_layout = QVBoxLayout()
        self.setObjectName("package_window")
        self.setStyleSheet(Utils().read_qss_file("../res/qss/affordable_packages.qss"))

        self.shoppingCartItemMap = shoppingCartItemMap
        self.user = user
        for package in packages_dict.values():
            packageDetails = PackageDetails(
                parent_widget=self,
                dishId="package-"+str(package.get("id")),
                coverPath=package.get("img_path"),
                title=package.get("simplified_title"),
                discount=str(package.get("discount")),
                current=str(package.get("price")),
                categoryId="package-"+str(package.get("id")),
                categoryName="package",
                shoppingCartItemMap=shoppingCartItemMap,
                user=user
            )
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

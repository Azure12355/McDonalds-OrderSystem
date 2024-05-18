from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QSizePolicy, QWidget, QGroupBox, QVBoxLayout, QLabel, QGridLayout, QApplication, QScrollArea
import os
from utils.utils import Utils


def read_binary_files_in_directory(directory_path):
    # 获取目录中所有文件的列表
    file_list = os.listdir(directory_path)
    file_paths = []

    # 遍历文件列表
    for filename in file_list:
        # 构建文件的完整路径
        file_path = os.path.join(directory_path, filename)

        # 检查文件是否为普通文件且可读
        if os.path.isfile(file_path):
            file_paths.append(file_path)

    return file_paths


class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        # 设置主窗口大小
        # self.setFixedWidth(800)
        # 设置尺寸策略为 Fixed
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setObjectName("home_page")
        self.setStyleSheet(Utils.read_qss_file("../res/qss/home_window.qss"))

        # 封面管理map
        self.cover_map = {}
        self.cover_size = 0

        # 封面装载的容器
        self.cover_group_box = QGroupBox()
        self.cover_group_box.setTitle("首页精选")

        # group_box的布局为垂直布局
        self.group_box_layout = QVBoxLayout(self.cover_group_box)

        # 网格布局装载cover
        self.cover_grid_layout = QGridLayout()

        # 滚动布局装载网格布局
        scroll_content = QWidget()
        scroll_content.setLayout(self.cover_grid_layout)
        scroll_area = QScrollArea()
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)

        self.group_box_layout.addWidget(scroll_area)

        # 主布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.cover_group_box)

    def load_covers(self, cover_paths):
        for cover_path in cover_paths:
            # 获取图片
            pixmap = QPixmap(cover_path)

            # 创建 QLabel
            cover = QLabel()
            cover.setPixmap(pixmap)
            cover.setScaledContents(True)

            # 计算图片尺寸和占用位置
            if pixmap.width() / pixmap.height() == 4 / 3:
                # 4:3 图片
                cover.setFixedSize(400, 300)
                cover_span = 2

            else:
                # 2:3 图片
                cover.setFixedSize(200, 300)
                cover_span = 1

            # 添加图片到布局
            self.add_cover(cover, cover_span)

    def add_cover(self, cover, cover_span):
        # 计算当前行和列
        row = self.cover_size // 4
        col = self.cover_size % 4

        # 检查是否需要新的一行
        if col + cover_span > 4:
            col = 0
            row += 1

        # 添加图片到布局
        self.cover_grid_layout.addWidget(cover, row, col, 1, cover_span)

        # 更新图片总数
        self.cover_size += cover_span


if __name__ == "__main__":
    app = QApplication([])
    file_paths = read_binary_files_in_directory("../res/McDonald/homepage")

    home_page = HomePage()
    home_page.load_covers(file_paths)
    home_page.show()

    app.exec()

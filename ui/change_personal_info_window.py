import re

from PySide6.QtWidgets import QMessageBox, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QLabel, QWidget

from client.client import Client


class InfoChange(QWidget):
    def __init__(self, main_window: QWidget):
        super().__init__()
        self.main_window = main_window  # 引用登录窗口以便后续显示或隐藏

        self.setWindowTitle("个人信息修改")
        self.setFixedSize(400, 500)  # 与登录窗口尺寸保持一致

        # 创建表单组件
        layout1 = QHBoxLayout()
        self.username_label = QLabel("用户名:")
        self.username_label.setFixedWidth(60)
        self.username_input = QLineEdit()
        layout1.addWidget(self.username_label)
        layout1.addWidget(self.username_input)

        layout2 = QHBoxLayout()
        self.password_label = QLabel("密码:")
        self.password_label.setFixedWidth(60)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout2.addWidget(self.password_label)
        layout2.addWidget(self.password_input)

        layout3 = QHBoxLayout()
        self.realname_label = QLabel("真实姓名:")
        self.realname_label.setFixedWidth(60)
        self.realname_input = QLineEdit()
        layout3.addWidget(self.realname_label)
        layout3.addWidget(self.realname_input)

        layout4 = QHBoxLayout()
        self.gender_label = QLabel("性别:")
        self.gender_label.setFixedWidth(60)
        self.gender_input = QLineEdit()
        layout4.addWidget(self.gender_label)
        layout4.addWidget(self.gender_input)

        layout5 = QHBoxLayout()
        self.birthday_label = QLabel("生日:")
        self.birthday_label.setFixedWidth(60)
        self.birthday_input = QLineEdit()
        layout5.addWidget(self.birthday_label)
        layout5.addWidget(self.birthday_input)

        layout7 = QHBoxLayout()
        self.phone_label = QLabel("电话号码:")
        self.phone_label.setFixedWidth(60)
        self.phone_input = QLineEdit()
        layout7.addWidget(self.phone_label)
        layout7.addWidget(self.phone_input)

        # 创建按钮
        self.change_button = QPushButton("修改")
        self.change_button.clicked.connect(self.change_clicked)

        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.cancel_clicked)

        # 设置布局
        layout = QVBoxLayout()
        self.setLayout(layout)

        form_layout = QVBoxLayout()
        form_layout.addLayout(layout2)
        form_layout.addLayout(layout3)
        form_layout.addLayout(layout4)
        form_layout.addLayout(layout5)
        form_layout.addLayout(layout1)
        form_layout.addLayout(layout7)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.change_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

    def cancel_clicked(self):
        self.close()

    def validate_inputs(self):
        username = self.username_input.text()
        password = self.password_input.text()
        realname = self.realname_input.text()
        gender = self.gender_input.text()
        birthday = self.birthday_input.text()
        phone_number = self.phone_input.text()

        if not password or not username or not realname or not gender or not birthday or not phone_number:
            QMessageBox.warning(self, "无效输入", "字段不能为空~~~")
            return False

        # 检查电话号码格式
        if phone_number and not re.match(r"\d{10}", phone_number):
            QMessageBox.warning(self, "无效输入", "请输入有效的电话号码（10位数字）")
            return False

        return True

    def change_clicked(self):
        if not self.validate_inputs():
            return

        username = self.username_input.text()
        password = self.password_input.text()
        realname = self.realname_input.text()
        gender = self.gender_input.text()
        birthday = self.birthday_input.text()
        phone_number = self.phone_input.text()

        # 假设有一个userManager对象来处理注册逻辑
        success = Client().updatePersonalInfo(email=self.main_window.user.user_email,
                                              user_name=username,
                                              new_realname=realname,
                                              new_gender=gender,
                                              new_birthday=birthday,
                                              new_phone_number=phone_number)

        if success:
            QMessageBox.information(self, "修改成功", "修改个人成功！")
        else:
            QMessageBox.warning(self, "注册失败", "修改失败，请检查您的信息并重试。")

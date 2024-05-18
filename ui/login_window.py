import re

from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QApplication, QMessageBox
from client.client import Client
from main.main import MyMainWindow
from utils.utils import Utils


class Forget(QWidget):
    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window  # 引用登录窗口以便后续显示或隐藏

        self.setWindowTitle("忘记密码")
        self.setFixedSize(400, 500)  # 与登录窗口尺寸保持一致

        layout6 = QHBoxLayout()
        self.email_label = QLabel("要找回的邮箱:")
        self.email_label.setFixedWidth(80)
        self.email_input = QLineEdit()
        layout6.addWidget(self.email_label)
        layout6.addWidget(self.email_input)

        layout2 = QHBoxLayout()
        self.password_label = QLabel("重置密码:")
        self.password_label.setFixedWidth(80)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout2.addWidget(self.password_label)
        layout2.addWidget(self.password_input)

        layout3 = QHBoxLayout()
        self.repeat_password_label = QLabel("再次输入密码:")
        self.repeat_password_label.setFixedWidth(80)
        self.repeat_password_input = QLineEdit()
        self.repeat_password_input.setEchoMode(QLineEdit.Password)
        layout3.addWidget(self.repeat_password_label)
        layout3.addWidget(self.repeat_password_input)

        # 创建按钮
        self.retrieve_account = QPushButton("找回账号")
        self.retrieve_account.clicked.connect(self.register_clicked)

        self.return_login_button = QPushButton("返回登录界面")
        self.return_login_button.clicked.connect(self.show_login_window)

        # 设置布局
        layout = QVBoxLayout()
        self.setLayout(layout)

        form_layout = QVBoxLayout()
        form_layout.addLayout(layout6)
        form_layout.addLayout(layout2)
        form_layout.addLayout(layout3)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.retrieve_account)
        button_layout.addWidget(self.return_login_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

    def show_login_window(self):
        self.login_window.show()
        self.close()

    def validate_inputs(self):
        email = self.email_input.text()
        password = self.password_input.text()
        re_password = self.repeat_password_input.text()

        if not email or not password or not re_password:
            QMessageBox.warning(self, "无效输入", "字段不能为空!!!")

        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            QMessageBox.warning(self, "无效输入", "请输入有效的邮箱地址")
            return False

        if password != re_password:
            QMessageBox.warning(self, "无效输入", "两次输入的密码不一致, 请重新输入!!!")
            return False

        return True

    def register_clicked(self):
        if not self.validate_inputs():
            return

        email = self.email_input.text()
        password = self.password_input.text()

        # 假设有一个userManager对象来处理注册逻辑
        success = Client().changePassword(email, password)

        if success:
            QMessageBox.information(self, "修改失败", "修改密码成功!!!请返回登录")
        else:
            QMessageBox.warning(self, "修改失败", "修改失败, 请检查邮箱输入是否正确")


class Register(QWidget):
    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window  # 引用登录窗口以便后续显示或隐藏

        self.setWindowTitle("用户注册")
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

        layout6 = QHBoxLayout()
        self.email_label = QLabel("邮箱:")
        self.email_label.setFixedWidth(60)
        self.email_input = QLineEdit()
        layout6.addWidget(self.email_label)
        layout6.addWidget(self.email_input)

        layout7 = QHBoxLayout()
        self.phone_label = QLabel("电话号码:")
        self.phone_label.setFixedWidth(60)
        self.phone_input = QLineEdit()
        layout7.addWidget(self.phone_label)
        layout7.addWidget(self.phone_input)

        # 创建按钮
        self.register_button = QPushButton("注册")
        self.register_button.clicked.connect(self.register_clicked)

        self.return_login_button = QPushButton("返回登录界面")
        self.return_login_button.clicked.connect(self.show_login_window)

        # 设置布局
        layout = QVBoxLayout()
        self.setLayout(layout)

        form_layout = QVBoxLayout()
        form_layout.addLayout(layout6)
        form_layout.addLayout(layout2)
        form_layout.addLayout(layout3)
        form_layout.addLayout(layout4)
        form_layout.addLayout(layout5)
        form_layout.addLayout(layout1)
        form_layout.addLayout(layout7)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.register_button)
        button_layout.addWidget(self.return_login_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

    def show_login_window(self):
        self.login_window.show()
        self.close()

    def validate_inputs(self):
        username = self.username_input.text()
        password = self.password_input.text()
        realname = self.realname_input.text()
        gender = self.gender_input.text()
        birthday = self.birthday_input.text()
        email = self.email_input.text()
        phone_number = self.phone_input.text()

        if not password or not username or not realname or not gender or not birthday or not email or not phone_number:
            QMessageBox.warning(self, "无效输入", "字段不能为空~~~")
            return False
        # 检查邮箱格式
        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            QMessageBox.warning(self, "无效输入", "请输入有效的邮箱地址")
            return False

        # 检查电话号码格式
        if phone_number and not re.match(r"\d{10}", phone_number):
            QMessageBox.warning(self, "无效输入", "请输入有效的电话号码（10位数字）")
            return False

        return True

    def register_clicked(self):
        if not self.validate_inputs():
            return

        username = self.username_input.text()
        password = self.password_input.text()
        realname = self.realname_input.text()
        gender = self.gender_input.text()
        birthday = self.birthday_input.text()
        email = self.email_input.text()
        phone_number = self.phone_input.text()

        # 假设有一个userManager对象来处理注册逻辑
        success = Client().register(username, password, realname, gender, birthday, email, phone_number)

        if success:
            QMessageBox.information(self, "注册成功", "注册成功！")
        else:
            QMessageBox.warning(self, "注册失败", "注册失败，请检查您的信息并重试。")


class Login(QWidget):
    def __init__(self, mainWindow: MyMainWindow):
        super().__init__()

        # 设置主窗口大小
        self.setFixedSize(400, 500)
        # 设置尺寸策略为Fixed
        # self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setObjectName("login_window")
        self.setStyleSheet(Utils().read_qss_file("../res/qss/login_window.qss"))

        self.setWindowTitle("Login")
        # 设置图标
        icon = QIcon("../res/images//images (12).png")
        self.setWindowIcon(icon)

        self.register_window = None
        self.forget_window = None

        # 标题
        self.title = QLabel("登录后开始点餐")
        self.title.setFixedSize(400, 50)
        self.title.setObjectName("title")

        # 账号输入框
        self.accountLabel = QLabel("邮箱:")
        self.accountInput = QLineEdit()
        self.accountLabel.setObjectName("account_label")
        self.accountInput.setObjectName("account_input")
        self.accountInput.setText("azure@example.com")

        # 密码输入框
        self.passwordLabel = QLabel("密码:")
        self.passwordInput = QLineEdit()
        self.passwordInput.setObjectName("password_input")
        self.passwordLabel.setObjectName("password_label")
        self.passwordInput.setEchoMode(QLineEdit.Password)  # 设置EchoMode为Password以隐藏输入的文本
        self.passwordInput.setText("azure")

        # 登录按钮
        self.loginButton = QPushButton("登录")
        self.loginButton.clicked.connect(self.loginClicked)
        self.loginButton.setObjectName("login_btn")

        # 忘记密码按钮
        self.forgotPasswordButton = QPushButton("忘记密码")
        self.forgotPasswordButton.clicked.connect(self.showForgotPasswordDemo)
        self.forgotPasswordButton.setObjectName("forget_btn")

        # 注册账号按钮
        self.registerButton = QPushButton("注册账号")
        self.registerButton.clicked.connect(self.showRegisterDemo)
        self.registerButton.setObjectName("register_btn")

        # 主界面
        self.mainWindow = mainWindow

        # 设置布局
        layout = QVBoxLayout(self)
        layout.setObjectName("main_layout")

        # Account layout
        accountLayout = QHBoxLayout()
        accountLayout.addWidget(self.accountLabel)
        accountLayout.addWidget(self.accountInput)

        # Password layout
        passwordLayout = QHBoxLayout()
        passwordLayout.addWidget(self.passwordLabel)
        passwordLayout.addWidget(self.passwordInput)

        # Buttons layout
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self.forgotPasswordButton)
        buttonsLayout.addWidget(self.registerButton)

        layout.addWidget(self.title,)
        layout.addLayout(accountLayout)
        layout.addLayout(passwordLayout)
        layout.addWidget(self.loginButton)
        layout.addLayout(buttonsLayout)

        self.app = app  # 保存应用程序实例

    def loginClicked(self):
        # 在这里添加登录逻辑
        enteredAccount = self.accountInput.text()
        enteredPassword = self.passwordInput.text()

        if not enteredAccount or not enteredPassword:
            QMessageBox.warning(self, "登录错误", "请输入账号和密码")
            return

        user = Client().login(enteredAccount, enteredPassword)
        if user is None:
            QMessageBox.warning(self, "登录失败", "用户名或密码错误")
            return

        # 关闭登录窗口
        self.close()

        # 打开主窗口
        self.mainWindow.user = user
        self.mainWindow.show()

    def showForgotPasswordDemo(self):
        self.forget_window.show()
        self.hide()

    def showRegisterDemo(self):
        self.register_window.show()
        self.hide()


# 示例用法
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication([])

    main_window = MyMainWindow()
    login_window = Login(main_window)
    register_window = Register(login_window)
    forget_window = Forget(login_window)

    login_window.register_window = register_window
    login_window.forget_window = forget_window
    login_window.show()

    sys.exit(app.exec())

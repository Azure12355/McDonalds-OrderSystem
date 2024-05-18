class User:
    def __init__(self, emil, password):
        self.user_id = None
        self.user_email = emil
        self.user_password = password
        self.user_name = None
        self.user_realname = None
        self.user_gender = 1
        self.user_birthday = None
        self.phone_number = None
        self.orders = []


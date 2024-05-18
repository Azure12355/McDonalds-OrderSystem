import datetime


class Utils:

    @staticmethod
    def read_qss_file(qss_file_name):
        """
        此方法用于读取qss源文件中的文本内容并且返回
        :param qss_file_name: 文件路径
        :return: 文本文件
        """
        with open(qss_file_name, encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def get_sys_time():
        # 获取当前日期和时间
        current_datetime = datetime.datetime.now()

        # 格式化为字符串，保留到秒
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        return formatted_datetime

    @staticmethod
    def add_minutes_to_current_time(minutes):
        # 获取当前日期和时间
        current_datetime = datetime.datetime.now()

        # 定义一个时间间隔为指定分钟数的 timedelta 对象
        time_interval = datetime.timedelta(minutes=minutes)

        # 在当前时间上加上时间间隔
        new_datetime = current_datetime + time_interval

        formatted_datetime = new_datetime.strftime("%Y-%m-%d %H:%M:%S")

        return formatted_datetime


if __name__ == '__main__':
    print(Utils().add_minutes_to_current_time(30))

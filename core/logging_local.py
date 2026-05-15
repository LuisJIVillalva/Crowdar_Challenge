from datetime import datetime

class log():
    color_end = '\033[0m'
    @staticmethod
    def info(message):
        color_ini = '\033[32m'
        date = datetime.now().strftime("%H:%M:%S")
        print(f"{color_ini}{date} - INFO - {message}", log.color_end)

    @staticmethod
    def test(message):
        color_ini = '\033[37m'
        date = datetime.now().strftime("%H:%M:%S")
        print(f"{color_ini}{date} - TEST - {message}", log.color_end)

    @staticmethod
    def config(message):
        color_ini = '\033[32m'
        date = datetime.now().strftime("%H:%M:%S")
        print(f"{color_ini}{date} - CONFIG - {message}", log.color_end)

    @staticmethod
    def warning(message):
        color_ini = '\033[93m'
        date = datetime.now().strftime("%H:%M:%S")
        print(f"{color_ini}{date} - WARNING - {message}", log.color_end)

    @staticmethod
    def error(message):
        color_ini = '\033[31m'
        date = datetime.now().strftime("%H:%M:%S")
        print(f"{color_ini}{date} - ERROR - {message}", log.color_end)
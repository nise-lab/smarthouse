"""
IOパーツは
light や servo のインターフェース
"""

import os.path

class IoPart:
    def __init__(self, gpio, device_id):
        self.gpio = gpio
        self.device_id = device_id
        self.status_file_name = "gpio/%d" % device_id

    def get_status(self):
        # 状態を取得
        result = "unknown"

        if os.path.isfile(self.status_file_name):
            # 状態ファイルがあればファイルから読む
            status_file = open(self.status_file_name, "r")
            result = status_file.read()
            status_file.close()
        else:
            # 無い場合はデバイスから読み取る
            result = self.get_status_from_gpio()

        return result

    def set_status(self, status):
        self.__validate_status(status)
        raise Exception("set_status が定義されていません")

    def get_status_from_gpio(self):
        # GPIOから状態を読み取る，できないものは"unknown"返す
        return("unknown")

    def write_status(self, status):
        # ステータスの書き込み
        status_file = open(self.status_file_name, "w")
        status_file.write(status)
        status_file.flush()
        status_file.close()

if __name__ == "__main__":
    pass

"""
IOパーツ サーボモータ
"""
# Servo Control with the Raspberry Pi - YouTube
# http://www.youtube.com/watch?v=ddlDgUymbxc
# freq: 50Hz
# 0   : duty 2.5
# 90  : duty 7.5
# 180 : duty 12.5

import time
import re

from io_part import IoPart

class Servo(IoPart):
    def __init__(self, gpio, device_id):
        IoPart.__init__(self, gpio, device_id)

    def set_status(self, status):
        # "unknown" : 一度も動作させていない（現在の angle 不明）
        # "busy" : 動作中
        # angle_value : 停止中 現在のangle
        self.status_validation(status)

        angle = int(status)
        result = self.set_angle(angle)
        return(result)

    def set_angle(self, angle):
        # サーボモータの制御
        self.status_validation(angle)

        current_status = self.get_status()
        if current_status == "busy":
            return("busy reject")

        if current_status != "unknown":
            current_angle = int(current_status)
            if current_angle == angle:
                return("still this angle")

        self.write_status("busy")
        self.__setup()

        servo = self.gpio.PWM(self.device_id, 50)
        servo.start(2.5 + 10.0 * angle / 180.0)
        time.sleep(0.5)
        servo.stop()
        self.write_status(str(angle))
        return("accept")

    def status_validation(self, status):
        # 定義されているステータスなのか
        # 指定値内のステータスなのか確認する
        regexp = re.compile("(?P<angle>\A[0-9]{1,3}\Z)")
        matched = regexp.search(str(status))

        try:
            matched.groups()
        except AttributeError:
            raise Exception("status: " + str(status) + " が不正です")

        angle = matched.group("angle")
        if int(angle) < 0 or 180 < int(angle):
            raise Exception("angle が不正です")

    def get_status_from_gpio(self):
        # GPIOから状態を読み取る
        status = "unknown"
        return(status)

    def __setup(self):
        self.gpio.setmode(self.gpio.BCM)
        self.gpio.setup(self.device_id, self.gpio.OUT)

if __name__ == "__main__":
    from servo import Servo; import RPi.GPIO as g; g.setwarnings(False); s = Servo(g, 23)

    s.set_angle(0)
    print(s.get_status())
    s.set_angle(180)
    print(s.get_status())
    s.set_angle(90)
    print(s.get_status())

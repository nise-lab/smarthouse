"""
IOパーツ LED
点滅する LED
"""

import time

from light import Light

class Blinker(Light):
    def __init__(self, gpio, device_id):
        Light.__init__(self, gpio, device_id)

    def set_status(self, status):
        # "blinking" : 点滅中
        # "free" : 消灯中
        self.status_validation(status)

        result = "謎"
        if status == "blinking":
            result = self.blink()
        return(result)

    def blink(self, times=10, span=0.2):
        # 点滅させる
        if self.get_status == "blinking":
            return("still blinking")

        self.write_status("blinking")
        self.setup()

        for i in range(times):
            self.gpio.output(self.device_id, self.gpio.HIGH)
            time.sleep(span)
            self.gpio.output(self.device_id, self.gpio.LOW)
            time.sleep(span)

        self.write_status("free")
        return("accept")

    def status_validation(self, status):
        # 定義されているステータスなのか
        # 指定値内のステータスなのか確認する
        if status != "blinking":
            raise Exception("status が不正です")

    def get_status_from_gpio(self):
        # GPIOから状態を読み取る
        status = "unknown"
        return(status)

if __name__ == "__main__":
    import RPi.GPIO as g
    g.setwarnings(False)
    b = Blinker(g, 18)
    b.blink()

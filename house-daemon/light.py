"""
IOパーツ LED
"""

from io_part import IoPart

class Light(IoPart):
    def __init__(self, gpio, device_id):
        IoPart.__init__(self, gpio, device_id)

    def set_status(self, status):
        # "on" : 点灯中
        # "off" : 消灯中
        self.status_validation(status)

        result = "謎"
        if status == "on":
            result = self.turn_on()
        if status == "off":
            result = self.turn_off()
        return(result)

    def turn_on(self):
        # 点灯
        current_status = self.get_status()
        if current_status == "on":
            return("still on")

        self.setup()
        self.gpio.output(self.device_id, self.gpio.HIGH)
        self.write_status("on")
        return("accept")

    def turn_off(self):
        # 消灯
        current_status = self.get_status()
        if current_status == "off":
            return("still off")

        self.setup()
        self.gpio.output(self.device_id, self.gpio.LOW)
        self.write_status("off")
        return("accept")

    def status_validation(self, status):
        # 定義されているステータスなのか
        # 指定値内のステータスなのか確認する
        if status != "on" and status != "off":
            raise Exception("status が不正です")

    def get_status_from_gpio(self):
        # GPIOから状態を読み取る
        status = "unknown"

        self.setup()
        gpio_level = self.gpio.input(self.device_id)
        if gpio_level == self.gpio.HIGH:
            status = "on"
        elif gpio_level == self.gpio.LOW:
            status = "off"

        self.write_status(status)
        return(status)

    def setup(self):
        self.gpio.setmode(self.gpio.BCM)
        self.gpio.setup(self.device_id, self.gpio.OUT)

if __name__ == "__main__":
    import RPi.GPIO as g
    import time
    g.setwarnings(False)

    l = Light(g, 18)
    l.turn_on()
    time.sleep(0.5)
    l.turn_off()

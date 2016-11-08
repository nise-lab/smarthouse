"""
ハードウェアの操作を受け付ける
"""
import RPi.GPIO
import json
import codecs

from light import Light
from blinker import Blinker
from servo import Servo

class Hardware:
    def __init__(self, io_parts_seed_file):
        self.gpio = RPi.GPIO
        self.gpio.setwarnings(False)

        io_parts_seeds = json.load(
            codecs.open(io_parts_seed_file, "r", "utf-8")
        )

        self.io_parts = {}
        for name, part in io_parts_seeds.items():
            type = part["type"]
            id = part["id"]

            if(type == "light"):
                self.io_parts[name] = Light(self.gpio, id)
            elif(type == "blink"):
                self.io_parts[name] = Blinker(self.gpio, id)
            elif(type == "servo"):
                self.io_parts[name] = Servo(self.gpio, id)
            else:
                raise Exception("type が不正なIOパーツが含まれています")

    def get_status(self, part_name):
        self.part_validation(part_name)
        part = self.io_parts[part_name]
        condition = part.get_status()

        return(condition)

    def set(self, part_name, status_name):
        self.part_validation(part_name)
        part = self.io_parts[part_name]
        status_name = str(status_name)
        result = part.set_status(status_name)

        message =  "[HARDWARE] SET " + part_name
        message += " STATUS " + status_name
        message += " > " + result
        print(message)

        return(result)

    def part_validation(self, part_name):
        try:
            self.io_parts[part_name]
        except KeyError:
            message =  "part:" + part_name + "は定義されていません"
            raise Exception(message)

if __name__ == "__main__":
    # HOUSE_SECTIONS_SEED_FILE = "io_parts.json" # 本番環境
    HOUSE_SECTIONS_SEED_FILE = "io_parts_test.json" # テスト環境
    hardware = Hardware(HOUSE_SECTIONS_SEED_FILE)
    import time
    hardware.set("room_led1", "on")
    time.sleep(0.5)
    hardware.set("room_led1", "off")
    time.sleep(0.5)
    hardware.set("room_led2", "blinking")
    time.sleep(0.5)
    hardware.set("window_servo", 0)
    time.sleep(0.5)
    hardware.set("window_servo", 180)
    time.sleep(0.5)
    hardware.set("window_servo", 90)

    print(hardware.get_status("room_led1"))
    print(hardware.get_status("room_led2"))
    print(hardware.get_status("window_servo"))

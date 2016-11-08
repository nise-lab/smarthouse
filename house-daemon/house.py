"""
家具の操作を受け付ける
"""
import json
import codecs
from collections import OrderedDict

from hardware import Hardware
from house_section import HouseSection

class House:
    def __init__(self, house_sections_seed_file, io_parts_seed_file):
        self.hardware = Hardware(io_parts_seed_file)

        house_sections_seeds = json.load(
            codecs.open(house_sections_seed_file, "r", "utf-8")
        )

        self.house_sections = {}
        for section_name, section in house_sections_seeds.items():
            priority = section["priority"]
            message_name = section["message_name"]
            self.house_sections[section_name] = HouseSection(
                self.hardware,
                section_name,
                message_name,
                priority
            )
            for name, condition in section["conditions"].items():
                message_name = condition["message_name"]
                priority = condition["priority"]
                io_part_statuses = condition["io_part_statuses"]
                self.house_sections[section_name].add_condition(
                    name,
                    message_name,
                    priority,
                    io_part_statuses
                )

        self.update_section_current_conditions()

    def get_section_contents(self, sorted_mode=False):
        # {
        #   "room": {
        #     "message_name": "部屋の照明",
        #     "priority": 0
        #     "current_condition": "bright",
        #     "conditions": {
        #       "brighter": { message_name: "明るめ", ... },
        #       ...
        #     }
        #   },
        #   ...
        # }

        section_contents = {}
        for section_name in self.house_sections:
            section_content = self.get_section_content(
                section_name,
                sorted_mode
            )
            section_contents[section_name] = section_content

        if sorted_mode:
            # message_name に基づいてソート
            # 参考 https://goo.gl/gXyZ8h
            section_contents = OrderedDict(sorted(
                section_contents.items(),
                key=lambda x:x[1]["priority"])
            )

        return(section_contents)

    def get_section_content(self, section_name, sorted_mode=False):
        # {
        #   "message_name": "部屋の照明",
        #   "priority": "0"
        #   "current_condition": "bright",
        #   "conditions": {
        #     "brighter": {
        #       "message_name": "明るめ",
        #       "priority": "0",
        #       "io_part_statuses": {
        #         "room_led1": "on", "room_led2": "on"
        #       }
        #     },
        #     ...
        #   }
        # }

        self.update_section_current_condition(section_name)
        section_content = {}
        self.section_validation(section_name)
        section = self.house_sections[section_name]
        section_content["message_name"] = section.message_name
        section_content["priority"] = section.priority
        section_content["current_condition"] = section.current_condition

        conditons = section.conditions
        if sorted_mode:
            # message_name に基づいてソート
            conditons = OrderedDict(sorted(
                conditons.items(),
                key=lambda x:x[1]["priority"])
            )
        section_content["conditions"] = conditons

        current_io_part_status = section.current_io_part_status
        section_content["current_io_part_status"] = current_io_part_status

        return(section_content)

    def get_section_conditions(self):
        # { "room": "bright", "bed": "on", ... }
        section_conditions = {}
        for name, section in self.house_sections.items():
            conditon = self.get_section_condition()
            section_conditions[name] = conditon
        return(section.current_condition)

    def get_section_condition(self, section_name):
        self.section_validation(section_name)
        section = self.house_sections[section_name]
        return(section.current_condition)

    def set(self, section_name, condition_name):
        # section の conditon を書き換える

        self.section_validation(section_name)
        section = self.house_sections[section_name]
        result = section.set_condition(condition_name)

        message =  "[HOUSE] SET " + section_name
        message += " CONDITION " + condition_name
        message += " > " + result
        print(message)

        return(result)

    def update_section_current_conditions(self):
        for name in self.house_sections:
            self.update_section_current_condition(name)

    def update_section_current_condition(self, section_name):
        self.section_validation(section_name)
        section = self.house_sections[section_name]
        result = section.update_current_condition()
        return(result)

    def section_validation(self, section_name):
        try:
            self.house_sections[section_name]
        except KeyError:
            message =  "section:" + section_name + "は定義されていません"
            raise Exception(message)

if __name__ == "__main__":
    # 本番環境
    # HOUSE_SECTIONS_SEED_FILE = "house_sections.json"
    # IO_PARTS_SEED_FILE = "io_parts.json"

    # テスト環境
    HOUSE_SECTIONS_SEED_FILE = "house_sections_test.json"
    IO_PARTS_SEED_FILE = "io_parts_test.json"

    h = House(HOUSE_SECTIONS_SEED_FILE, IO_PARTS_SEED_FILE)
    import time
    # h.set("room", "brighter")
    # print(h.get_section_condition("room"))
    # time.sleep(0.5)
    # h.set("room", "off")
    # print(h.get_section_condition("room"))

    print(h.get_section_condition("room2"))
    h.set("room2", "blinking")
    print(h.get_section_condition("room2"))
    time.sleep(0.5)

    # print(h.get_section_condition("window"))
    # h.set("window", "open")
    # print(h.get_section_condition("window"))
    # h.set("window", "close")
    # print(h.get_section_condition("window"))

    print(h.get_section_contents())

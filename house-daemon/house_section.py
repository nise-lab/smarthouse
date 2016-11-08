"""
家具屋 天井等など
複数のハードをまとめてセクション
ex) room は room_led1 と room_led2 をもつ
"""

class HouseSection:
    def __init__(self, hardware, name, message_name, priority):
        self.hardware = hardware
        self.name = name
        self.message_name = message_name
        self.priority = priority
        self.conditions = {}
        self.current_io_part_status = {}
        self.current_condition = "unknown"

    def add_condition(self, name, message_name, priority, io_part_statuses):
        # io_part_statuses は，ハッシュ
        # { "room_led1": "on", "room_led2": "on" }
        self.conditions[name] = {
            "message_name": message_name,
            "priority": priority,
            "io_part_statuses": io_part_statuses
        }

    def set_condition(self, condition_name):
        # section の conditon を変える
        conditon = None
        try:
            conditon = self.conditions[condition_name]
        except KeyError:
            message =  self.name + " には conditon:"
            message += condition_name + "は定義されていません"
            raise Exception(message)

        io_part_statuses = conditon["io_part_statuses"]

        results = []
        for name, status in io_part_statuses.items():
            results.append(self.hardware.set(name, status))

        if results.count("accept") == len(results):
            # すべて accept なら
            self.current_condition = self.update_current_condition()
            return("accept")
        else:
            return("なにか動かなかった")

    def update_current_condition(self):
        # self.current_condition を更新する
        # get_condition を作って毎回更新すると gpio へのアクセスが集中するため
        # 適宜必要なとき（初期化のとき，最新の状態が欲しいとき，とか）に 更新する

        current_condition = "unknown"

        self.current_io_part_status = {}
        io_part_names = self.get_io_part_names()

        for io_part_name in io_part_names:
            status = self.hardware.get_status(io_part_name)
            self.current_io_part_status[io_part_name] = status

        for name, conditon in self.conditions.items():
            if conditon["io_part_statuses"] == self.current_io_part_status:
                self.current_condition = name

        return(self.current_condition)

    def get_io_part_names(self):
        # io_part の 名前の一覧を取得
        # [ "room_led1", "room_led2" ]
        sample_condition = None

        try:
            sample_condition = list(self.conditions.values())[0]
        except IndexError:
            message = self.name + " には conditon が1つも定義されていません"
            raise Exception(message)

        return(list(sample_condition["io_part_statuses"].keys()))

if __name__ == "__main__":
    pass

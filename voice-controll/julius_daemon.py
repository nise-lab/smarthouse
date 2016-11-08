# juliusモジュールから指定のワードを感知し，実行に移すモジュール
#
# 引数
# -a がついたら already モード
# このモードの場合 スタンバイキーワードなしで命令を感知し実行
# -m がついたら OSX モード
# jsay コマンドの代わりに say コマンドを使う
# -n がついたら no GPIO モード
# GPIO の操作はしない
# 参考
# http://cubic9.com/Devel/%C5%C5%BB%D2%B9%A9%BA%EE/irMagician/%C0%D6%B3%B0%C0%FE%B3%D8%BD%AC%A5%EA%A5%E2%A5%B3%A5%F3R2-D2/
#http://www.orsx.net/blog/archives/4938

import sys
import os
import socket as sock
import json
import codecs
import re
import time
import datetime
import requests

class JuliusDaemon:
    def __init__(self):
        COMMAND_JSON = "julius_commands.json"
        JULIUS_HOST = "127.0.0.1"
        JULIUS_PORT = 10500

        # 定義ファイルの読み込み
        self.commands = json.load(codecs.open(COMMAND_JSON, "r", "utf-8"))

        # 各種フラグの初期化
        self.need_standby = "-a" not in sys.argv
        self.osx_mode     = "-m" in sys.argv
        self.no_gpio_mode  = "-n" in sys.argv
        self.is_standby   = False

        # Juliusの出力から必要なデータを抽出するための正規表現
        self.regexp = re.compile('.*\<WHYPO( WORD="(?P<command>.+?)"| CLASSID="(?P<word>.+?)"| CM="(?P<cm>[0-9]+\.[0-9]+)"| [a-zA-Z]+=".+?")*\/\>')

        # Juliusの出力ストリームを取得
        self.socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.socket.connect((JULIUS_HOST, JULIUS_PORT))
        self.julius = self.socket.makefile("rb")
        print("ready.")

    def main_loop(self):
        try:
            while True:
                # 出力を1行読んで正規表現とマッチング
                line  = self.julius.readline().decode("utf-8")
                match = self.regexp.match(line)

                # キーワードを認識したら
                if match:
                    # Juliusの出力から必要なデータを抽出
                    word    = match.group("word")
                    command_name = match.group("command")
                    cm      = float(match.group("cm"))
                    # 整形して出力
                    out  = ("word: %s" % (word))
                    out += (", command: %s" % (command_name))
                    out += (", cm: %3.0f%%" % (cm * 100))

                    BORDER_SCORE = 95

                    # 信頼度が BORDER_SCORE % 以上ならコマンドを受理
                    if BORDER_SCORE * 0.01 <= cm:
                        print(out + " > accepted.")
                        self.accept(command_name)
                    else:
                        print(out + " > score is low.")

        except KeyboardInterrupt:
            self.julius.close()
            self.socket.close()

    def accept(self, command_name):
        # スタンバイ
        # already モード ならば無効
        if command_name == "standby" and self.need_standby:
            self.standby()

        # キャンセル
        # already モード ならば無効
        elif command_name == "cancel" and self.need_standby and self.is_standby:
            self.cancel()

        # 命令コマンド
        elif self.is_standby or not self.need_standby:
            if command_name == "what_time":
                # 時報
                self.excute_what_time()
                self.is_standby = False
            elif command_name in self.commands:
                # その他
                self.execute(command_name)
                self.is_standby = False
            else:
                # コマンドの動作が未定義
                print("エラー：命令が未定義")
        else:
            print("スタンバイ状態ではありません")

    def execute(self, command_name):
        voice_message = self.commands[command_name]["voice"]
        section_name = self.commands[command_name]["section"]
        condition = self.commands[command_name]["method"]

        self.say(voice_message)
        print(command_name + " を実行")
        if self.no_gpio_mode:
            return("success")

        headers = {"Content-Type": "application/json"}
        payload = {"condition": condition}

        # house-daemon
        HOST = "localhost"
        PORT = "5000"

        url = "http://" + HOST + ":" + PORT
        url += "/sections/" + section_name + "/condition"

        requests.put(url, data=json.dumps(payload), headers=headers)

        return("success")

    def excute_what_time(self):
        date     = datetime.datetime.today()
        sentence = date.strftime("現在の時刻は、%H時、%M分です")
        self.say(sentence)

    def standby(self):
        self.say("命令を受け付けます")
        self.is_standby = True

    def cancel(self):
        self.say("受付をキャンセルしました")
        self.is_standby = False

    def say(self, content):
        if self.osx_mode:
            os.system("say " + content)
        else:
            os.system("jsay " + content)

if __name__ == '__main__':
    jd = JuliusDaemon()
    jd.main_loop()

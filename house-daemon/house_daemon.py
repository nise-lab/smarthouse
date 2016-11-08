# Python3 自体は pyenv 等を入れる
#
# デフォルトの sudo では pi の PATH を継承しないので
# visudo を編集し，sudo でパスを継承するようにする
# 参考
# Qiita - sudo時にPATHを引き継ぐ方法 https://goo.gl/Ic1wYq
#
# 設計の参考
# Python の Flask で REST API を作ってみる https://goo.gl/1d1Tba

import json
import os
import datetime
from functools import wraps
from flask import Flask, abort, request, render_template, url_for, jsonify, send_from_directory

from house import House

HOST = "0.0.0.0"
PORT = 5000

# 本番環境
HOUSE_SECTIONS_SEED_FILE = "house_sections.json"
IO_PARTS_SEED_FILE = "io_parts.json"

# テスト環境
# HOUSE_SECTIONS_SEED_FILE = "house_sections_test.json"
# IO_PARTS_SEED_FILE = "io_parts_test.json"

house = House(HOUSE_SECTIONS_SEED_FILE, IO_PARTS_SEED_FILE)
app = Flask(__name__)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

def consumes(content_type):
    # Content-Type の検証
    def _consumes(function):
        @wraps(function)
        def __consumes(*argv, **keywords):
            if request.headers['Content-Type'] != content_type:
                abort(400)
            return function(*argv, **keywords)
        return __consumes
    return _consumes

@app.route("/")
def index():
    sections = house.get_section_contents(sorted_mode=True)
    year = datetime.date.today().year
    return render_template('index.html', sections=sections, year=year)

@app.route("/sections")
def show_sections():
    data = house.get_section_contents()
    return(jsonify(data))

@app.route("/sections/<string:section_name>")
def show_section(section_name):
    data = house.get_section_content(section_name)
    return(jsonify(data))

@app.route("/sections/<string:section_name>/condition", methods=['PUT'])
@consumes('application/json')
def update_section_conditon(section_name):
    condition_name = request.json["condition"]
    result = house.set(section_name, condition_name)
    return(jsonify(result))

@app.route("/sections/<string:section_name>/condition")
def show_section_condition(section_name):
    return(jsonify(house.get_section_condition(section_name)))

@app.route("/sections/<string:section_name>/condition/<string:condition_name>")
def update_section_conditon_debug(section_name, condition_name):
    # REST から外れてしまうがデバッグ用のルーティング (PUTするのめんどくさい！)
    result = house.set(section_name, condition_name)
    return(jsonify(result))

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=80, debug=True)
    app.run(host=HOST, port=PORT, debug=True)

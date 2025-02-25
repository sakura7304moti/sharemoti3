"""
スマブラ切り抜きまとめのルーティング
"""
import json
import os
from flask import Blueprint, request, jsonify, send_file
from src.route.service.module.utils import const
from src.route.service import ssbulist_service

#改行文字を取得
NEW_LINE_TEXT = const.get_new_line_text()

#保存先
p = const.Path()
DATA_PATH = p.share_folder()

# Blueprintのオブジェクトを生成する
app = Blueprint('ssbuList',__name__)

@app.route("/ssbu/search",methods=['GET'])
def ssbulist_search():
    records = ssbulist_service.search()
    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        )
    }
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace("\\", "").replace('"[{', "[{").replace('}]"', "}]")
    if len(records) == 0:
        json_data = "[]"
    response = jsonify(json_data)
    return response

@app.route('/ssbu/download',methods=['GET'])
def ssbulist_download():
    path = request.args.get('path','')
    rec = ssbulist_service.select(path)
    path = os.path.join(DATA_PATH,'スマブラ','切り抜き',rec.path)
    return send_file(path , mimetype='video/mp4')

"""
ホロライブのオリ曲や歌っていたのルーティング
"""
import json
from flask import Blueprint, jsonify
from src.route.service import holosong_service
from src.route.service.module.utils import const

opt = const.Option()

#改行文字を取得
NEW_LINE_TEXT = const.get_new_line_text()

# Blueprintのオブジェクトを生成する
app = Blueprint('holosong',__name__)
@app.route("/holoSong/search",methods=["GET"])
def holosong_select():
    records = holosong_service.cover_songs()
    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        )
    }
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace('"[{', "[{").replace('}]"', "}]")
    
    #改行文字だけ残してバックスラッシュは削除
    json_data = json_data.replace('\\n',NEW_LINE_TEXT)
    json_data = json_data.replace('\\','')
    json_data = json_data.replace(NEW_LINE_TEXT,'\\n')
    
    if len(records) == 0:
        json_data = "[]"
    response = jsonify(json_data)
    return response

@app.route("/holoSong/hololist", methods=["GET"])
def holosong_get_hololist():
    json_data = json.dumps(opt.holo_wiki_members(), ensure_ascii=False)
    response = jsonify(json_data)
    return response

"""
ホロライブのオリキョクを取得する
"""
@app.route('/holoSong/ori',methods=["GET"])
def holosong_ori():
    records = holosong_service.original_songs()
    # 辞書にまとめる
    result = {
        "records": json.dumps(
            records, default=lambda obj: obj.__dict__(), ensure_ascii=False
        )
    }
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    json_data = json_data.replace('"[{', "[{").replace('}]"', "}]")
    
    #改行文字だけ残してバックスラッシュは削除
    json_data = json_data.replace('\\n',NEW_LINE_TEXT)
    json_data = json_data.replace('\\','')
    json_data = json_data.replace(NEW_LINE_TEXT,'\\n')
    
    if len(records) == 0:
        json_data = "[]"
    response = jsonify(json_data)
    return response
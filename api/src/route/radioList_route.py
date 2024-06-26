"""
オム子レイディオのルーティング
"""
import json
import os
from flask import Blueprint, request, jsonify, send_file
from src.route.service.module.utils import const
from src.route.service import radiolist_service

#改行文字を取得
NEW_LINE_TEXT = const.get_new_line_text()

#保存先
p = const.Path()
DATA_PATH = p.share_folder()

# Blueprintのオブジェクトを生成する
app = Blueprint('radioList',__name__)

@app.route("/radio/search",methods=['GET'])
def radiolist_search():
    records = radiolist_service.search()
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

@app.route('/radio/download',methods=['GET'])
def radiolist_download():
    id = int(request.args.get('id',-1))
    rec = radiolist_service.select(id)
    path = os.path.join(DATA_PATH,'オムコレイディオ','mp3',rec.file_name+'.mp3')
    return send_file(path , mimetype='audio/mpeg')

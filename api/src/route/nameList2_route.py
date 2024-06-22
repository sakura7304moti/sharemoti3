"""
あだ名一覧2のルーティング
"""
import json
from flask import Blueprint, request, jsonify
from main.src.modules import main_const
from api.src.route.service import namelist2_service

#改行文字を取得
NEW_LINE_TEXT = main_const.get_new_line_text()

# Blueprintのオブジェクトを生成する
app = Blueprint('nameList2',__name__)

# nameListの初期設定
namelist2_service.create_db()

@app.route("/nameList2/search", methods=["GET"])
def namelist2_search():
    records = namelist2_service.search()
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

@app.route("/nameList2/insert", methods=["POST"])
def namelist2_insert():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    name = json_data.get("name", "")
    ssbu_name = json_data.get("ssbuName", "")

    result = namelist2_service.insert(name, ssbu_name)
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result.__dict__(), ensure_ascii=False)
    response = jsonify(json_data)
    return response

@app.route("/nameList2/update", methods=["POST"])
def namelist2_update():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    id = int(json_data.get("id","-1"))
    name = json_data.get("name", "")
    ssbu_name = json_data.get("ssbuName", "")

    result = namelist2_service.update(id, name, ssbu_name)
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result.__dict__(), ensure_ascii=False)
    response = jsonify(json_data)
    return response

@app.route("/nameList2/delete", methods=["POST"])
def namelist2_delete():
    json_data = request.json
    id = int(json_data.get("id",-1))
    result = namelist2_service.delete(id)
    # JSON文字列に変換
    json_data = json.dumps(result.__dict__(), ensure_ascii=False)
    response = jsonify(json_data)
    return response
"""
あだ名一覧のルーティング
"""
import json
from flask import Blueprint, request, jsonify
from src.route.service.module.utils import const
from src.route.service import namelist_service

opt = const.Option()
#改行文字を取得
NEW_LINE_TEXT = const.get_new_line_text()

# Blueprintのオブジェクトを生成する
app = Blueprint('nameList',__name__)

# nameListの初期設定
namelist_service.create_db()

@app.route("/nameList/search", methods=["POST"])
def namelist_search():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    key = json_data.get("key", "")
    val = json_data.get("val", "")

    records = namelist_service.search(key, val)
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


@app.route("/nameList/insert", methods=["POST"])
def namelist_insert():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    key = json_data.get("key", "")
    val = json_data.get("val", "")

    result = namelist_service.insert(key, val)
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    response = jsonify(json_data)
    return response


@app.route("/nameList/update", methods=["POST"])
def namelist_update():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    bkey = json_data.get("bkey", "")
    bval = json_data.get("bval", "")
    key = json_data.get("key", "")
    val = json_data.get("val", "")

    result = namelist_service.update(bkey, bval, key, val)
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    response = jsonify(json_data)
    return response


@app.route("/nameList/delete", methods=["POST"])
def namelist_delete():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    key = json_data.get("key", "")
    val = json_data.get("val", "")

    res = namelist_service.delete(key, val)
    result = {"status": res}
    # レスポンスとしてJSONデータを返す
    # JSON文字列に変換
    json_data = json.dumps(result, ensure_ascii=False)
    response = jsonify(json_data)
    return response


@app.route("/nameList/names", methods=["GET"])
def nameList_names():
    records = opt.ssbu_names()
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
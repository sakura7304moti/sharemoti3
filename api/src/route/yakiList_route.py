"""
焼き直し条約2のルーティング
"""
import json
from flask import Blueprint, request, jsonify
from src.route.route_base import success_status
from src.route.service.module.utils import const
from src.route.service import yakilist_service

# Blueprintのオブジェクトを生成する
app = Blueprint('yakiList2',__name__)

@app.route("/yakiList/search", methods=["GET"])
def yakiList2_search():
    df = yakilist_service.search()
    records = df.to_json(orient='records',force_ascii=False)
    return jsonify(records)

@app.route("/yakiList/insert", methods=["POST"])
def yakiList2_insert():
    json_data = request.json
    word = json_data.get("word", "")
    yaki = json_data.get("yaki", "")

    yakilist_service.insert(word, yaki)
    return success_status()

@app.route("/yakiList/update", methods=["POST"])
def yakiList2_update():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    id = int(json_data.get("id","-1"))
    word = json_data.get("word", "")
    yaki = json_data.get("yaki", "")

    yakilist_service.update(id, word, yaki)
    return success_status()

@app.route("/yakiList/delete", methods=["POST"])
def yakiList2_delete():
    json_data = request.json
    id = int(json_data.get("id",-1))
    yakilist_service.delete(id)
    return success_status()
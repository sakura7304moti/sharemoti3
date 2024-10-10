"""
名言集のルーティング
"""
import json
from flask import Blueprint, request, jsonify
from src.route.service.module.utils import const,interface
from src.route.service import wordlist_service

def to_condition():
    json_data = request.json
    id = int(json_data.get("id", 0))
    word = json_data.get("word", "")
    detail = json_data.get("detail", "")
    condition = interface.Word(
        id,
        word,
        detail
    )
    return condition

def success_status():
    return jsonify({"status": 'success'})

# Blueprintのオブジェクトを生成する
app = Blueprint('wordList',__name__)

@app.route("/wordList/search", methods=["POST"])
def wordlist_search():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    text = json_data.get("text", "")

    df = wordlist_service.search(text)
    records = df.to_json(orient='records',force_ascii=False)
    return jsonify(records)
    

@app.route("/wordList/insert", methods=["POST"])
def wordlist_insert():
    condition = to_condition()
    wordlist_service.insert(condition)
    return success_status()

@app.route("/wordList/update", methods=["POST"])
def wordlist_update():
    condition = to_condition()
    wordlist_service.update(condition)
    return success_status()


@app.route("/wordList/delete", methods=["POST"])
def wordlist_delete():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    id = int(json_data.get("id", 0))
    wordlist_service.delete(id)
    return success_status()
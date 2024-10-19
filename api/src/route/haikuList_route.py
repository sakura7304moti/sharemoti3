"""
俳句一覧のルーティング
"""
import json
from flask import Blueprint, request, jsonify
from src.route.route_base import success_status
from src.route.service.module.utils import const,interface
from src.route.service import haikulist_service

def to_condition():
    json_data = request.json
    id = int(json_data.get("id", 0))
    first = json_data.get("first","")
    second = json_data.get("second","")
    third = json_data.get("third","")
    poster = json_data.get("poster","")
    detail = json_data.get("detail","")
    return interface.Haiku(
        id,
        first,second,third,
        poster,detail
    )

# Blueprintのオブジェクトを生成する
app = Blueprint('haikuList',__name__)

@app.route("/haikuList/search",methods=["GET"])
def haikuList_search():
    df = haikulist_service.search()
    records = df.to_json(orient='records',force_ascii=False)
    return jsonify(records)

@app.route("/haikuList/insert",methods=["POST"])
def haikuList_insert():
    condition = to_condition()
    haikulist_service.insert(condition)
    return success_status()

@app.route("/haikuList/update",methods=["POST"])
def haikuList_update():
    condition = to_condition()
    haikulist_service.update(condition)
    return success_status()

@app.route("/haikuList/delete",methods=["POST"])
def haikuList_delete():
    json_data = request.json
    id = int(json_data.get("id",-1))
    haikulist_service.delete(id)
    return success_status()
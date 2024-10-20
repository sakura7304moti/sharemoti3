"""
あだ名一覧2のルーティング
"""
from flask import Blueprint, request, jsonify
from src.route.route_base import success_status
from src.route.service import namelist2_service

app = Blueprint('nameList2',__name__)

@app.route("/nameList2/search", methods=["GET"])
def namelist2_search():
    df = namelist2_service.search()
    records = df.to_json(orient='records',force_ascii=False)
    return jsonify(records)


@app.route("/nameList2/insert", methods=["POST"])
def namelist2_insert():
    json_data = request.json
    name = json_data.get("name", "")
    ssbu_name = json_data.get("ssbuName", "")
    namelist2_service.insert(name, ssbu_name)
    return success_status()
    

@app.route("/nameList2/update", methods=["POST"])
def namelist2_update():
    json_data = request.json
    id = int(json_data.get("id","-1"))
    name = json_data.get("name", "")
    ssbu_name = json_data.get("ssbuName", "")
    namelist2_service.update(id, name, ssbu_name)
    return success_status()

@app.route("/nameList2/delete", methods=["POST"])
def namelist2_delete():
    json_data = request.json
    id = int(json_data.get("id",-1))
    namelist2_service.delete(id)
    return success_status()
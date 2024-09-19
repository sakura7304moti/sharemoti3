"""
ホロメンのツイートのルーティング
"""
import json


from flask import Blueprint, request, jsonify
from src.route.service import holotwitter_service as service
from src.route.service.module.utils import interface

def to_search_condition():
    json_data = request.json
    text = json_data.get("text", "")
    acount_name = json_data.get("acountName", "")
    start_date = json_data.get("startDate", "")
    page_no = int(json_data.get("pageNo", "1"))
    page_size = 20
    condition = interface.HoloTwitterSearchCondition(
        text=text,
        acount_name=acount_name,
        start_date=start_date,
        page_no=page_no,
        page_size=page_size
    )
    return condition

# Blueprintのオブジェクトを生成する
app = Blueprint('holotwitter',__name__)

@app.route("/holotwitter/search", methods=["POST"])
def search_tweet():
    """
    ツイートの検索
    """
    condition = to_search_condition()
    df, total_count = service.search(condition)
    records = df.to_json(orient='records',force_ascii=False)

    #1つのjsonにまとめる
    records_json = json.loads(records)

    #メディアの取得
    for rec in records_json:
        medias = service.get_media(rec.get("id"))
        rec["medias"] = json.loads(medias.to_json(orient='records',force_ascii=False))

    response = {
        "records" : records_json,
        "totalCount":total_count
    }

    return jsonify(json.dumps(response))

@app.route("/holotwitter/acount", methods=["GET"])
def get_acount():
    """
    アカウントの一覧を取得
    """
    df = service.get_acount()
    records = df.to_json(orient='records',force_ascii=False)
    return jsonify(records)

@app.route("/holotwitter/media/<int:id>",methods=["GET"])
def get_media(id:int):
    """
    メディアの一覧を取得
    """
    df = service.get_media(id)
    records = df.to_json(orient='records',force_ascii=False)
    return jsonify(records)
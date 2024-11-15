"""
追加履歴のルーティング
"""
import json


from flask import Blueprint, request, jsonify, send_file


from src.route.service import top_news_service as service

# Blueprintのオブジェクトを生成する
app = Blueprint('topNews',__name__)

@app.route("/topNews/<int:pageNo>", methods=["GET"])
def ssbu_clip_search(pageNo:int):
    """
    履歴の検索
    """
    df, total_count  = service.get_top_news(pageNo)

    records = df.to_json(orient='records',force_ascii=False)
    records_json = json.loads(records)
    response = {
        "records" : records_json,
        "totalCount":total_count
    }
    return jsonify(json.dumps(response))
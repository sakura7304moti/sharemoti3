"""
pixivのルーティング
"""
import pandas as pd
import json
import ast



from flask import Blueprint, request, jsonify


from src.route.service import pixiv_service

# Blueprintのオブジェクトを生成する
app = Blueprint('pixiv',__name__)

@app.route("/pixiv/search/illust", methods=["POST"])
def pixiv_illust_search():
    """
    イラストの検索
    """
    json_data = request.json
    hashtags_text = json_data.get("hashtags", "[]")
    hashtags = ast.literal_eval(hashtags_text)
    user_id = json_data.get("userId", 0)
    min_total_bookmarks = json_data.get("minTotalBookmarks", 0)
    min_total_view = json_data.get("minTotalView", 0)
    page_no = json_data.get("pageNo", 1)
    page_size = json_data.get("pageSize", 20)

    df,count = pixiv_service.search_illust(
        hashtags = hashtags,
        user_id = user_id,
        min_total_bookmarks = min_total_bookmarks,
        min_total_view = min_total_view,
        page_no = page_no,
        page_size = page_size
    )

    records = df.to_json(orient='records')
    result = {
        "records" : records,
        "totalCount" : count
    }
    response = json.dumps(
        result, 
        ensure_ascii=False, 
        indent=2
    )
    return jsonify(response)

@app.route("/pixiv/images", methods=["GET"])
def pixiv_get_images():
    """
    イラストの画像データを取得
    """
    id = int(request.args.get('id', 0))
    if id < 1:
        response = jsonify(message="idのパラメータは必須です")
        response.status_code = 400
        return response

    df = pixiv_service.get_images(id)
    records = df.to_json(orient='records')
    return jsonify(records)

@app.route("/pixiv/search/hashtags", methods=["GET"])
def pixiv_search_hashtags():
    """
    ハッシュタグの検索
    """
    name = request.args.get('name', "")
    df = pixiv_service.search_hashtags(name)
    records = df.to_json(orient='records')
    return jsonify(records)

@app.route("/pixiv/search/users", methods=["GET"])
def pixiv_search_users():
    """
    ユーザーの検索
    """
    name = request.args.get('name', "")
    df = pixiv_service.search_users(name)
    records = df.to_json(orient='records')
    return jsonify(records)
"""
pixivのルーティング
"""
import pandas as pd
import json
import ast
import requests
import mimetypes


from io import BytesIO
from flask import Blueprint, request, jsonify, send_file, Response
from markupsafe import escape


from src.route.service import pixiv_service
from src.route.service.module.utils import const

opt = const.Option()

# Blueprintのオブジェクトを生成する
app = Blueprint('pixiv',__name__)

@app.route("/pixiv/search/illust", methods=["POST"])
def pixiv_illust_search():
    """
    イラストの検索
    """
    json_data = request.json
    print(json_data)

    text = json_data.get("text", "")
    hashtags = json_data.get("hashtags", [])
    user_ids = json_data.get("userIds", [])
        
    min_total_bookmarks = int(json_data.get("minTotalBookmarks", 0))
    min_total_view = int(json_data.get("minTotalView", 0))
    page_no = int(json_data.get("pageNo", 1))
    page_size = int(json_data.get("pageSize", 20))

    df = pixiv_service.search_illust(
        text = text,
        hashtags = hashtags,
        user_ids = user_ids,
        min_total_bookmarks = min_total_bookmarks,
        min_total_view = min_total_view,
        page_no = page_no,
        page_size = page_size
    )

    records = df.to_json(orient='records',force_ascii=False)
    return jsonify(records)

@app.route("/pixiv/search/illust/count", methods=["POST"])
def pixiv_illust_search_count():
    """
    イラストの検索
    """
    json_data = request.json

    text = json_data.get("text", "")
    hashtags = json_data.get("hashtags", [])
    user_ids = json_data.get("userIds", [])
        
    min_total_bookmarks = json_data.get("minTotalBookmarks", 0)
    min_total_view = json_data.get("minTotalView", 0)

    count = pixiv_service.search_illust_count(
        text = text,
        hashtags = hashtags,
        user_ids = user_ids,
        min_total_bookmarks = min_total_bookmarks,
        min_total_view = min_total_view
    )

    return str(count)

@app.route("/pixiv/illust/<int:id>", methods=["GET"])
def pixiv_get_illust(id:int):
    """
    イラストデータを取得
    """
    illust = pixiv_service.get_illust(id)
    return jsonify(json.dumps(illust))


@app.route('/pixiv/image/download', methods=["GET"])
def pixiv_image_download():
    headers = {'Referer': 'https://www.pixiv.net'}
    image_url = request.args.get('url', "")

    if image_url == "":
        response = jsonify(message="urlが空")
        response.status_code = 400
        return response

    mime_type, _ = mimetypes.guess_type(image_url)

    response = requests.get(image_url, headers=headers)

    if response.status_code == 200:
        image = BytesIO(response.content)
        return send_file(image, mimetype=mime_type)
    else:
        return Response('Image not found', status=404)


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
    records = df.to_json(orient='records',force_ascii=False)
    return jsonify(records)

@app.route("/pixiv/search/hashtags", methods=["GET"])
def pixiv_search_hashtags():
    """
    ハッシュタグの検索
    """
    name = request.args.get('name', "")
    id = int(request.args.get('id', 0))
    df = pixiv_service.search_hashtags(name, id)
    records = df.to_json(orient='records',force_ascii=False)
    return jsonify(records)

@app.route("/pixiv/search/users", methods=["GET"])
def pixiv_search_users():
    """
    ユーザーの検索
    """
    name = request.args.get('name', "")
    df = pixiv_service.search_users(name)
    records = df.to_json(orient='records',force_ascii=False)
    return jsonify(records)

@app.route("/pixiv/option/holoname", methods=["GET"])
def pixiv_holoname():
    """
    ホロメンの選択用データ
    """
    df = opt.holo_pixiv_selecter()
    records = df.to_json(orient='records',force_ascii=False)
    return jsonify(records)
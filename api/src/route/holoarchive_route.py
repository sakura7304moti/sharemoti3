"""
ホロライブのアーカイブのスクレイピング
"""
import json
from flask import Blueprint, jsonify, request
from src.route.service import holoarchive_service

# Blueprintのオブジェクトを生成する
app = Blueprint('holoarchive',__name__)

"""
チャンネル情報の一覧
"""
@app.route("/holoArchive/search/channel",methods=["GET"])
def holomovie_channel():
    df = holoarchive_service.search_chennel()
    records = df.to_json(orient='records',force_ascii=False)
    records_json = json.loads(records)
    response = {
        "records":records_json
    }
    return jsonify(json.dumps(response))

"""
動画情報の一覧
"""
@app.route("/holoArchive/search/movie",methods=["POST"])
def holomovie_movie():
    json_data = request.json  # POSTメソッドで受け取ったJSONデータを取得
    # JSONデータから必要なパラメータを抽出
    page_no = json_data.get("pageNo", 1)
    page_size = json_data.get("pageSize", 20)
    title = json_data.get("title", "")
    from_date = json_data.get("fromDate", "")
    to_date = json_data.get("toDate", "")
    channel_id = json_data.get("channelId", "")
    movie_type = json_data.get("movieType","")

    
    df,total_count = holoarchive_service.search_records(
        page_no,page_size,
        title,
        from_date,to_date,
        channel_id,
        movie_type
    )
    records = df.to_json(orient='records',force_ascii=False)
    records_json = json.loads(records)

    response = {
        "records" : records_json,
        "totalPages":total_count
    }
    return jsonify(json.dumps(response))

"""
チャンネルURLの一覧
"""
@app.route("/holoArchive/channelUrl",methods=["GET"])
def holochannel():
    df = holoarchive_service.search_chennel()
    records = df.to_json(orient='records',force_ascii=False)
    records_json = json.loads(records)
    response = {
        "records" : records_json
    }
    return jsonify(json.dumps(response))
"""
ホロメンのツイートのルーティング
"""
import json
import uuid
import yt_dlp
import os


from flask import Blueprint, request, jsonify, send_file
from src.route.service import holotwitter_service as service
from src.route.service.module.utils import interface, const


path_model = const.Path()
DOWNLOAD_DIR = path_model.yt_dlp_temp()


def to_search_condition():
    """
    jsonを検索条件に変換する
    """
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

@app.route("/holotwitter/movie", methods=["GET"])
def download_movie():
    """
    動画のダウンロード
    """
    # クエリパラメータからURLを取得
    video_url = request.args.get('url')
    
    if not video_url:
        return jsonify({"error": "URLパラメータが必要です"}), 400
    
    # ファイルを保存する一時ファイル名を生成
    temp_file = os.path.join(DOWNLOAD_DIR, f"{uuid.uuid4()}.mp4")
    
    # yt-dlpの設定
    ydl_opts = {
        #'format': 'best',  # 最高品質を選択
        'outtmpl': temp_file,  # 出力ファイルの名前を指定
        #'merge_output_format': 'mp4',  # MP4形式で保存
        #'hls_prefer_native': True,  # ネイティブHLSダウンローダーを使用
    }
    
    try:
        # 動画をダウンロード
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        # ダウンロードしたファイルを送信
        return send_file(temp_file, download_name='video.mp4')
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    """
    finally:
        # ダウンロードしたファイルを削除
        if os.path.exists(temp_file):
            os.remove(temp_file)
    """
    
"""
スマブラの切り抜きのルーティング
"""
import json
import os


from flask import Blueprint, request, jsonify, send_file


from src.route.service import ssbu_clip_service as service
from src.route.service.module.utils import interface,const

def to_search_condition():
    """
    検索条件
    """
    json_data = request.json
    text = json_data.get("text", "")
    char_name = json_data.get("charName", "")
    ssbu_name = json_data.get("ssbuName", "")
    date = json_data.get("date", "")
    cate = json_data.get("cate", "")
    page_no = int(json_data.get("pageNo", 0))
    return interface.SsbuClipSearchCondition(
        text = text,
        char_name = char_name,
        ssbu_name = ssbu_name,
        date = date,
        cate = cate,
        page_no = page_no
    )

def to_clip_condition():
    """
    切り抜きデータ
    """
    json_data = request.json
    id = int(json_data.get("id", 0))
    file_name = json_data.get("fileName", "")
    char_name = json_data.get("charName", "")
    dir_name = json_data.get("dir_name", "")
    date = json_data.get("date", "")
    cates =  json_data.get("cates", [])
    return interface.SsbuClip(
        id = id,
        file_name=file_name,
        char_name=char_name,
        dir_name=dir_name,
        date=date,
        cates=cates
    )

# Blueprintのオブジェクトを生成する
app = Blueprint('ssbu_clip',__name__)

@app.route("/ssbu_clip/search", methods=["POST"])
def ssbu_clip_search():
    """
    切り抜きの検索
    """
    condition = to_search_condition()
    df, total_count  = service.search(condition)

    records = df.to_json(orient='records',force_ascii=False)
    records_json = json.loads(records)
    response = {
        "records" : records_json,
        "totalCount":total_count
    }
    return jsonify(json.dumps(response))

@app.route("/ssbu_clip/date", methods=["GET"])
def ssbu_clip_date():
    """
    日付の入力候補
    """
    date_list = service.date()
    json_data = json.dumps(date_list)
    return jsonify(json_data)

@app.route("/ssbu_clip/category", methods=["GET"])
def ssbu_clip_category():
    """
    種類の入力候補
    """
    category_list = service.category()
    json_data = json.dumps(category_list)
    return jsonify(json_data)



@app.route("/ssbu_clip/movie", methods=["GET"])
def ssbu_clip_movie():
    """
    動画データの取得
    """
    dir_name = request.args.get('dir_name', "")
    file_name = request.args.get('file_name', "")

    if dir_name == "" or file_name == "":
        response = jsonify(message="フォルダかファイル名が空です")
        response.status_code = 400
        return response
    

    # 緑色のANSIエスケープコード
    GREEN = "\033[92m"
    RESET = "\033[0m"

    path = service.get_movie(dir_name, file_name)

    # 緑色で出力
    print(f"{GREEN}{path}{RESET}")
    return send_file(path , mimetype='video/mp4')

@app.route("/ssbu_clip/update", methods=["GET"])
def ssbu_clip_update():
    """
    切り抜きをテーブルに再追加
    """
    try:
        service.save_clips()
        return jsonify(json.dumps({
            "status":"success"
        }))
    except Exception as e:
        return jsonify(json.dumps({
            "status":"failed",
            "detail":str(e)
        }))
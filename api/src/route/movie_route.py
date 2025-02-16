"""
動画のページのルーティング
"""

"""
アプリのアップロードの流れ
・ファイルのアップロードAPIを呼び出して、保存先のファイル名を取得する
・DBに入力内容を保存するAPIを呼び出して、完了
"""

import datetime
import mimetypes
import json
import os
from PIL import Image
from flask import Blueprint, flash, request, jsonify, send_file, abort
from werkzeug.utils import secure_filename
from src.route.route_base import success_status
from src.route.service.module.utils import interface
from src.route.service import movie_service
from src.route.service.module.utils import const


# Blueprintのオブジェクトを生成する
app = Blueprint("movie", __name__)

p = const.Path()
UPLOAD_FOLDER = p.movie_uploads()
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {"mp4", "mov", "webm", "mpg"}

THUMBNAIUL_FOLDER = p.movie_thumbnails_uploads()
if not os.path.exists(THUMBNAIUL_FOLDER):
    os.makedirs(THUMBNAIUL_FOLDER)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def to_condition():
    """
    動画のアップロード内容
    """
    json_data = request.json
    id = int(json_data.get("id", "0"))
    title = json_data.get("title", "")
    detail = json_data.get("detail", "")
    file_name = json_data.get("fileName", "")
    thumbnail_flg = int(json_data.get("thumbnailFlg", "0"))
    staff_cd = json_data.get("staffCd", "")
    hashtags = json_data.get("hashtags", [])
    return (
        interface.Movie(
            id=id,
            title=title,
            detail=detail,
            file_name=file_name,
            thumbnail_flg=thumbnail_flg,
            staff_cd=staff_cd,
        ),
        hashtags,
    )


@app.route("/movie/upload", methods=["GET", "POST"])
def movie_upload():
    # check if the post request has the file part
    print(request.files)
    if "file" not in request.files:
        flash("No file part")
        jsondata = {"fileName": ""}
        response = jsonify(jsondata)
        return response

    file = request.files["file"]
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == "":
        print("No selected file")
        jsondata = {"fileName": ""}
        response = jsonify(jsondata)
        return response

    # ext ok filename ok
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        ext = filename.rsplit(".", 1)[-1].lower()

        # 現在の日時を取得
        now = datetime.datetime.now()
        formatted_datetime = now.strftime("%Y%m%d%H%M%S")
        save_file_name = formatted_datetime + "." + ext

        save_path = os.path.join(UPLOAD_FOLDER, save_file_name)
        file.save(save_path)

        # サムネイルの作成
        movie_service.create_thumbnail(save_path)

        jsondata = {"fileName": save_file_name}
        response = jsonify(jsondata)
        return response


@app.route("/movie/thumbnail/<name>", methods=["POST"])
def upload_thumbnail(name: str):
    if "file" not in request.files:
        flash("No file part")
        return jsonify({"fileName": ""})

    file = request.files["file"]
    if file.filename == "":
        print("No selected file")
        return jsonify({"fileName": ""})

    # 拡張子なしのファイル名を取得
    filename = secure_filename(name).rsplit(".", 1)[0]  # name から拡張子を削除

    # 一時的に保存（Pillow は一度保存しないと処理できない）
    temp_path = os.path.join(THUMBNAIUL_FOLDER, secure_filename(file.filename))
    file.save(temp_path)

    # 画像を JPG に変換
    try:
        img = Image.open(temp_path)
        save_file_name = f"{filename}.jpg"
        save_path = os.path.join(THUMBNAIUL_FOLDER, save_file_name)

        img.convert("RGB").save(save_path, "JPEG", quality=95)
        os.remove(temp_path)  # 一時ファイルを削除

        return jsonify({"fileName": save_file_name})

    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({"fileName": ""})


@app.route("/movie", methods=["PUT"])
def movie_create():
    condition, hashtags = to_condition()
    if condition.id == 0:
        print("作成処理を実行")
        id = movie_service.create_movie(condition)
        for name in hashtags:
            movie_service.create_hashtag(id, name)
    else:
        print("更新処理を実行")
        movie_service.update_movie(condition)
        movie_service.delete_hashtag(condition.id)
        for hashtag in hashtags:
            movie_service.create_hashtag(condition.id, hashtag)
    return success_status()


@app.route("/movie/<name>", methods=["GET"])
def movie_download(name: str):
    if name == "":
        return abort(400)

    path = os.path.join(UPLOAD_FOLDER, name)
    if not os.path.exists(path):
        return abort(404)
    mime_type, _ = mimetypes.guess_type(path)
    return send_file(path, mimetype=mime_type)


@app.route("/movie/<name>", methods=["DELETE"])
def movie_delete(name: str):
    if name == "":
        return abort(400)

    path = os.path.join(UPLOAD_FOLDER, name)
    if not os.path.exists(path):
        return abort(404)

    id = movie_service.get_movie_id(name)
    movie_service.delete_movie(id)  # DBの削除
    os.remove(path)  # ファイルの削除
    return success_status()


@app.route("/movie/hashtag", methods=["GET"])
def movie_hashtag():
    df = movie_service.hashtag_list()
    records = df.to_json(orient="records", force_ascii=False)
    return jsonify(records)


@app.route("/movie/hashtag/name", methods=["PUT"])
def movie_hashtag_name_change():
    json_data = request.json
    before = json_data.get("before", "")
    after = json_data.get("after", "")
    if before == "" or after == "":
        return abort(404)
    movie_service.change_hashtagname(before, after)
    return success_status()


@app.route("/movie/hashtag/<name>", methods=["PUT"])
def movie_hashtag_update(name: str):
    is_group = (
        False if request.args.get("isGroup", "false") == "false" else True
    )  # クエリパラメータがあれば星をつける
    movie_service.update_group(name, is_group)
    return success_status()


@app.route("/movie/hashtag/<name>", methods=["DELETE"])
def movie_hashtag_delete(name: str):
    if name == "":
        return abort(404)
    movie_service.delete_hashtag_by_name(name)
    return success_status()


@app.route("/movie/info/<id>", methods=["GET"])
def get_movie_info(id: int):
    df, hashtag_df = movie_service.get_movie(id)
    movie = df.iloc[0].to_dict()

    # 検索結果
    # records = df.iloc[0].to_json(orient="records", force_ascii=False)
    # records_json = json.loads(records)

    # ハッシュタグの一覧
    hashtag_records = hashtag_df.to_json(orient="records", force_ascii=False)
    tag_json = json.loads(hashtag_records)
    response = {
        "movie": movie,
        "hashtags": tag_json,
    }
    return jsonify(json.dumps(response))


@app.route("/movie", methods=["GET"])
def movie_search():
    keyword = request.args.get("keyword", "")
    hashtag = request.args.get("hashtag", "")
    page_no = int(request.args.get("page", "1"))
    PAGE_SIZE = 4

    df, total_count, hashtag_df = movie_service.search_movie(
        keyword, hashtag, page_no, PAGE_SIZE
    )

    # 検索結果
    records = df.to_json(orient="records", force_ascii=False)
    records_json = json.loads(records)

    # ハッシュタグの一覧
    hashtag_records = hashtag_df.to_json(orient="records", force_ascii=False)
    tag_json = json.loads(hashtag_records)
    response = {
        "records": records_json,
        "totalCount": total_count,
        "hashtags": tag_json,
    }
    return jsonify(json.dumps(response))


@app.route("/movie/batch/thumbnail", methods=["GET"])
def update_thumbnail_all():
    movie_service.update_thumbnail_all()
    return success_status()


@app.route("/movie/thumbnail/<name>", methods=["GET"])
def get_thumbnail(name: str):
    path = movie_service.get_thumbnail_path(name)
    if not os.path.exists(path):
        return abort(404)
    mime_type, _ = mimetypes.guess_type(path)
    return send_file(path, mimetype=mime_type)

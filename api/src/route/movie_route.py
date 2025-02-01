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

        file.save(os.path.join(UPLOAD_FOLDER, save_file_name))

        jsondata = {"fileName": save_file_name}
        response = jsonify(jsondata)
        return response


@app.route("/movie", methods=["PUT"])
def movie_create():
    condition, hashtags = to_condition()
    id = movie_service.create_movie(condition)
    for name in hashtags:
        movie_service.create_hashtag(id, name)
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

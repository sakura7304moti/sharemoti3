"""
画像一覧のルーティング
"""
import datetime
import json
import os
from flask import Blueprint, flash, request, jsonify, send_file
from werkzeug.utils import secure_filename
from src.route.route_base import success_status
from src.route.service.module.utils import interface
from src.route.service import imagelist_service
from src.route.service.module.utils import const




# Blueprintのオブジェクトを生成する
app = Blueprint('imageList',__name__)

# 保存先のフォルダーを取得・作成
p = const.Path()
UPLOAD_FOLDER = os.path.join(p.share_folder(), '画像', 'おばあちゃんち')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    # ファイルアップロードを許可するか判別する
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def to_condition():
    """
    検索条件
    """
    json_data = request.json
    id = int(json_data.get("id", "0"))
    file_name = json_data.get("fileName", "")
    ext = json_data.get("ext", "")
    title = json_data.get("title", "")
    detail = json_data.get("detail", "")
    return interface.Image(
        id = id,
        file_name = file_name,
        ext = ext,
        title = title,
        detail = detail
    )


@app.route('/imageList/insert',methods=['POST'])
def imagelist_insert():
    condition = to_condition()
    imagelist_service.insert(condition)
    return success_status()
    
@app.route('/imageList/upload', methods=['GET', 'POST'])
def imagelist_upload():
    # check if the post request has the file part
    print(request.files)
    if 'file' not in request.files:
        flash('No file part')
        jsondata = {"fileName":''}
        response = jsonify(jsondata)
        return response
    
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        print('No selected file')
        jsondata = {"fileName":''}
        response = jsonify(jsondata)
        return response

    #ext ok filename ok
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[-1].lower()
        
        # 現在の日時を取得
        now = datetime.datetime.now()
        formatted_datetime = now.strftime("%Y%m%d%H%M%S")
        save_file_name = formatted_datetime + '.' + ext
        
        file.save(os.path.join(UPLOAD_FOLDER, save_file_name))
        
        jsondata = {"fileName":save_file_name}
        response = jsonify(jsondata)
        return response
        
@app.route('/imageList/download/<int:id>',methods=['GET'])
def imagelist_download(id:int):
    file_name = imagelist_service.get_file_name(id)
    
    path = os.path.join(UPLOAD_FOLDER,file_name)
    print(f'download path -> {path}')
    if 'png' in file_name:
        minetype = 'image/png'
    else:
        minetype = 'image/jpeg'
    return send_file(path, mimetype=minetype)

@app.route("/imageList/search/<int:page>",methods=['GET'])
def imagelist_search(page:int):
    PAGE_SIZE = 8
    df,total_count = imagelist_service.search(page, PAGE_SIZE)

    records = df.to_json(orient='records',force_ascii=False)
    records_json = json.loads(records)
    response = {
        "records" : records_json,
        "totalCount":total_count
    }
    return jsonify(json.dumps(response))

@app.route("/imageList/update",methods=["POST"])
def imagelist_update():
    condition = to_condition()
    imagelist_service.update(condition)
    return success_status()

@app.route("/imageList/delete/<int:id>",methods=["DELETE"])
def imagelist_delete(id:int | None):
    if(id == None):
        return jsonify({'message': 'id not found'}), 404
    
    imagelist_service.delete(id)
    return success_status()
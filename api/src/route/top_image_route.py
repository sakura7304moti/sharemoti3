"""
トップ画像
"""
from flask import Blueprint, send_file
from src.route.service import top_image_service

# Blueprintのオブジェクトを生成する
app = Blueprint('topImage',__name__)

@app.route('/topImage/image',methods=['GET'])
def top_image_single():
    path = top_image_service.get_image()
    return send_file(path, mimetype='image/jpeg')
"""
切り抜き統計のルーティング
"""
import json
from flask import Blueprint, request, jsonify
from src.route.service.module.utils import const
from src.route.service import ssbu_clip_toukei_service

# Blueprintのオブジェクトを生成する
app = Blueprint('ssbu_clip_toukei',__name__)

@app.route("/ssbu_clip/toukei/count/<text>", methods=["GET"])
def ssbu_clip_toukei_count(text:str):
    df = ssbu_clip_toukei_service.category_rank(text)
    records = df.to_json(orient='records',force_ascii=False)
    return jsonify(records)

@app.route("/ssbu_clip/toukei/first/<text>", methods=["GET"])
def ssbu_clip_toukei_first(text:str):
    df = ssbu_clip_toukei_service.category_first(text)
    records = df.to_json(orient='records',force_ascii=False)
    return jsonify(records)
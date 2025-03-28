"""
名言コレクションのルーティング
"""

from flask import Blueprint, flash, request, jsonify, send_file, abort
from src.route.service import word_collection_service as service
from src.route.service.module.utils import interface


# Blueprintのオブジェクトを生成する
app = Blueprint("word_collection", __name__)


def to_search_condition():
    json = request.json
    keyword = json.get("keyword", "")
    date_order = json.get("dateOrder", "")
    text_order = json.get("textOrder", "")
    kinen = int(json.get("kinen", "0"))
    year = int(json.get("year", "0"))
    return interface.SearchWordCellectionCondition(
        keyword=keyword,
        date_order=date_order,
        text_order=text_order,
        kinen=kinen,
        year=year,
    )


@app.route("/wordCollection/search", methods=["POST"])
def word_collection_search():
    condition = to_search_condition()
    df = service.search_word(condition)
    records = df.to_json(orient="records", force_ascii=False)
    return jsonify(records)


@app.route("/wordCollection/kinen", methods=["GET"])
def word_collection_kinen():
    ls = service.get_kinen_count()
    return jsonify(ls)


@app.route("/wordCollection/year", methods=["GET"])
def word_collection_years():
    ls = service.get_word_year()
    return jsonify(ls)

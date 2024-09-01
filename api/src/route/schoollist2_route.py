"""
学校一覧のルーティング
"""
from flask import Blueprint, request, jsonify


from src.route.service import schoollist2_service as service
from src.route.service.module.utils import interface


def to_school_condition():
    json_data = request.json
    id = int(json_data.get("id", 0))
    school_name = json_data.get("schoolName", "")
    principal = json_data.get("principal", "")
    detail = json_data.get("detail", "")
    slogan = json_data.get("slogan", "")
    condition = interface.SchoolQueryRecord(
        id,
        school_name,
        principal,
        detail,
        slogan
    )
    return condition

def to_comment_condition():
    json_data = request.json
    id = int(json_data.get("id", 0))
    school_id = int(json_data.get("schoolId", 0))
    star = int(json_data.get("star", 0))
    title = json_data.get("title", "")
    comment = json_data.get("comment", "")
    post_person = json_data.get("postPerson", "")
    condition = interface.SchoolCommentQueryRecord(
        id,
        school_id,
        star,
        title,
        comment,
        post_person
    )
    return condition

def success_status():
    return jsonify({"status": "success"})



# Blueprintのオブジェクトを生成する
app = Blueprint('school',__name__)

@app.route("/school/list", methods=["GET"])
def school_list():
    """
    学校の一覧
    """
    df = service.get_school()
    records = df.to_json(orient='records',force_ascii=False)
    return jsonify(records)

@app.route("/school/comment/<int:id>", methods=["GET"])
def school_comment(id:int):
    """
    学校のコメントを取得
    """
    df = service.get_comment(id)
    records = df.to_json(orient='records',force_ascii=False)
    return jsonify(records)

@app.route("/school/create/school", methods=["POST"])
def school_create_school():
    """
    学校の作成
    """
    condition = to_school_condition()
    service.create_school(condition)
    return success_status()

@app.route("/school/create/comment", methods=["POST"])
def school_create_comment():
    """
    コメントの作成
    """
    condition = to_comment_condition()
    service.create_comment(condition)
    return success_status()

@app.route("/school/edit/school", methods=["POST"])
def school_edit_school():
    """
    学校の編集
    """
    condition = to_school_condition()
    service.update_school(condition)
    return success_status()
    
@app.route("/school/edit/comment", methods=["POST"])
def school_edit():
    """
    コメントの編集
    """
    condition = to_comment_condition()
    service.update_comment(condition)
    return success_status()

@app.route("/school/delete/school/<int:id>", methods=["DELETE"])
def school_delete_school(id:int):
    """
    学校の削除
    """
    service.delete_school(id)
    return success_status()

@app.route("/school/delete/comment/<int:id>", methods=["DELETE"])
def school_delete_comment(id:int):
    """
    学校の削除
    """
    service.delete_comment(id)
    return success_status()
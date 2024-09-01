from src.route.service.module import schoollist2 as queryServce
from src.route.service.module.utils import interface

def make_table():
    """
    テーブルの作成
    """
    queryServce.make_table()

def get_school():
    """
    学校の一覧を取得
    """
    return queryServce.get_school()

def get_comment(id:int):
    """
    コメントの一覧を取得
    """
    return queryServce.get_comment(id)

def create_school(condition:interface.SchoolQueryRecord):
    """
    学校の作成
    """
    queryServce.create_school(condition)

def create_comment(condition:interface.SchoolCommentQueryRecord):
    """
    コメントの作成
    """
    queryServce.create_comment(condition)

def update_school(condition:interface.SchoolQueryRecord):
    """
    学校の編集
    """
    queryServce.update_school(condition)

def update_comment(condition:interface.SchoolCommentQueryRecord):
    """
    コメントの編集
    """
    queryServce.update_comment(condition)

def delete_school(id:int):
    """
    学校の削除。コメントも消える。
    """
    queryServce.delete_school(id)

def delete_comment(id:int):
    """
    コメントの削除
    """
    queryServce.delete_comment(id)
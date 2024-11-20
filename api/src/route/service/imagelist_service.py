from pandas import DataFrame
from src.route.service.module.utils import interface
from src.route.service.module import imagelist

"""
画像一覧
"""

def create_db():
    """
    テーブル作成
    """
    imagelist.init()

def insert(condition:interface.Image):
    """
    レコード追加
    """
    imagelist.insert(condition)

def update(condition:interface.Image):
    """
    レコード更新
    """
    imagelist.update(condition)

def delete(id:int):
    """
    レコード削除
    """
    return imagelist.delete(id)

def search() -> tuple[DataFrame, int]:
    """
    レコード一覧を取得
    """
    return imagelist.search()
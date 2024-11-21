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

def search(page:int, page_size:int) -> tuple[DataFrame, int]:
    """
    レコード一覧を取得
    """
    return imagelist.search(page, page_size)

def get_file_name(id:int) -> str:
    """
    IDに対する画像のファイル名を取得
    """
    return imagelist.get_file_name(id)
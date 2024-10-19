from src.route.service.module.utils import interface
from src.route.service.module import haikulist

"""
俳句一覧
"""

def insert(condition:interface.Haiku):
    """
    レコード追加
    """
    haikulist.insert(condition)

def update(condition:interface.Haiku):
    """
    レコード更新
    """
    haikulist.update(condition)

def delete(id:int):
    """
    レコード削除
    """
    haikulist.delete(id)

def search():
    """
    レコード検索
    """
    return haikulist.select()
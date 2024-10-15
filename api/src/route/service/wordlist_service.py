from src.route.service.module import wordlist
from src.route.service.module.utils import interface
"""
名言集
"""

def insert(condition:interface.Word):
    """
    レコード追加
    """
    wordlist.insert(condition)

def update(condition:interface.Word):
    """
    レコード更新
    """
    wordlist.update(condition) 

def delete(id:int):
    """
    レコード削除
    """
    wordlist.delete(id)

def search(text:str = ""):
    """
    レコード検索
    """
    return wordlist.search(text)
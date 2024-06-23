from src.route.service.module import imagelist

"""
画像一覧
"""

def create_db():
    """
    テーブル作成
    """
    imagelist.init()

def insert(file_name:str,ext:str,title:str,detail:str):
    """
    レコード追加
    """
    return imagelist.insert(file_name, ext, title, detail)

def update(id:int,title:str,detail:str):
    """
    レコード更新
    """
    return imagelist.update(id, title, detail)

def delete(id:int):
    """
    レコード削除
    """
    return imagelist.delete(id)

def search():
    """
    レコード一覧を取得
    """
    return imagelist.search()
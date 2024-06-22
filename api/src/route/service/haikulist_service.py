from api.src.route.service.module import haikulist

"""
俳句一覧
"""

def create_db():
    """
    テーブル作成
    """
    haikulist.init()

def insert(first:str,second:str,third:str,poster:str,detail:str):
    """
    レコード追加
    """
    return haikulist.insert(first, second, third, poster, detail)

def update(id:int,first:str,second:str,third:str,poster:str,detail:str):
    """
    レコード更新
    """
    return haikulist.update(id, first, second, third, poster, detail)

def delete(id:int):
    """
    レコード削除
    """
    return haikulist.delete(id)

def search(id:int,haiku_text:str,poster:str,detail:str):
    """
    レコード検索
    """
    return haikulist.select(id, haiku_text, poster, detail)
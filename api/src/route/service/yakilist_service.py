from api.src.route.service.module import yakilist

def create_db():
    """
    テーブル作成
    """
    yakilist.init()

def insert(word:str, yaki:str):
    """
    レコード追加
    """
    return yakilist.insert(word, yaki)

def update(id:int, word:str, yaki:str):
    """
    レコード更新
    """
    return yakilist.update(id, word, yaki)

def delete(id:int):
    """
    レコード削除
    """
    return yakilist.delete(id)

def search():
    """
    レコード取得
    """
    return yakilist.search()
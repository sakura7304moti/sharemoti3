from api.src.route.service.module import namelist
"""
スマブラのページ用のあだ名一覧
"""
def create_db():
    """
    テーブル作成
    """
    namelist.init()

def insert(key: str = "", val: str = ""):
    """
    レコードの追加
    """
    return namelist.insert(key, val)

def update(bkey: str = "", bval: str = "", key: str = "", val: str = ""):
    """
    レコードの更新
    """
    return namelist.update(bkey, bval, key, val)

def delete(key: str = "", val: str = ""):
    """
    レコードの削除
    """
    return namelist.delete(key, val)

def search(key: str = "", val: str = ""):
    """
    レコードの検索
    """
    return namelist.search(key, val)
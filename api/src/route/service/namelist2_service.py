from src.route.service.module import namelist2
"""
あだ名一覧
"""
def insert(name:str, ssbu_name:str):
    """
    レコード追加
    """
    namelist2.insert(name, ssbu_name)

def update(id:int, name:str, ssbu_name:str):
    """
    レコード更新
    """
    namelist2.update(id, name, ssbu_name)

def delete(id:int):
    """
    レコード削除
    """
    namelist2.delete(id)

def search():
    """
    レコード取得
    """
    return namelist2.search()
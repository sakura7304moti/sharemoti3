from src.route.service.module import voicelist

"""
ボイス
"""

def search():
    """
    一覧を取得
    """
    return voicelist.search()

def select(select_id:int):
    """
    音声データを取得
    """
    return voicelist.select(select_id)
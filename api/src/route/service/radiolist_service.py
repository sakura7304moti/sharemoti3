from src.route.service.module import radiolist
"""
オムコレイディオ
"""

def search():
    """
    一覧を取得
    """
    return radiolist.search()

def select(select_id:int):
    """
    動画データを取得
    """
    return radiolist.select(select_id)
from src.route.service.module import movielist

"""
完成品一覧
"""

def search():
    """
    一覧を取得
    """
    return movielist.search()

def select(select_id:int):
    """
    動画データを取得
    """
    return movielist.select(select_id)
from api.src.route.service.module import karaokelist
"""
カラオケ
"""

def search():
    """
    一覧を取得
    """
    return karaokelist.search()

def select(select_id:int):
    """
    音声データを取得
    """
    return karaokelist.select(select_id)
from src.route.service.module import ssbulist

"""
スマブラの切り抜き
"""
def search():
    """
    動画の一覧を取得
    """
    return ssbulist.search()

def select(path:str):
    """
    動画データを取得
    """
    return ssbulist.select(path)
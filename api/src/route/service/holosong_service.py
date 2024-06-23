from src.route.service.module import holosong

"""
ホロライブ非公式wikiのスクレイピング
"""

def cover_songs():
    """
    歌ってみたの一覧
    """
    return holosong.get_cover_songs()

def original_songs():
    """
    オリ曲の一覧
    """
    return holosong.get_original_songs()

def memory_movies():
    """
    記念配信の一覧
    """
    return holosong.get_memory_movies()
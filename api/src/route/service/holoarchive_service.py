from src.route.service.module import holoarchive
import math

"""
ホロライブのYouTube動画一覧
"""

def update_archives():
    """
    テーブルに更新
    """
    holoarchive.update_archives()

def search_records(
    page_no = 1,
    page_size = 20,
    title = '',
    from_date = '',
    to_date = '',
    channel_id = '',
    movie_type = ''
):
    """
    レコード検索
    """
    df = holoarchive.search_movie(
        page_no,
        page_size,
        title,
        from_date,
        to_date,
        channel_id,
        movie_type
    )
    pages = holoarchive.search_movie_count(
        page_no,
        title,
        from_date,
        to_date,
        channel_id,
        movie_type
    )
    total_count = math.ceil(pages/page_size)
    return df, total_count

def search_chennel():
    """
    チャンネルの一覧を取得
    """
    return holoarchive.search_channel()


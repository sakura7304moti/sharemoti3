from api.src.route.service.module import holoarchive

"""
ホロライブのYouTube動画一覧
"""

def update_archives():
    """
    テーブルに更新
    """
    holoarchive.update_archives()

def make_db():
    """
    テーブル作成
    """
    holoarchive.make_database()

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
    records = holoarchive.search_movie(
        page_no,
        page_size,
        title,
        from_date,
        to_date,
        channel_id,
        movie_type
    )
    total_count = holoarchive.search_movie_count(
        page_no,
        title,
        from_date,
        to_date,
        channel_id,
        movie_type
    )
    return records, total_count

def search_chennel():
    """
    チャンネルの一覧を取得
    """
    return holoarchive.search_channel()


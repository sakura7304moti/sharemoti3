from api.src.route.service.module import hololewd_scraper,hololewd_sqlite

"""
Hololewd
"""

def get_rows():
    """
    直近の1000件のhololewdのポストを取得
    """
    hololewd_scraper.get_rows()

def flair_texts_update():
    """
    ホロメンの名前を更新
    """
    hololewd_scraper.flair_texts_update()

def update_db():
    """
    ポストテーブルを更新
    検索も実行される
    """
    hololewd_scraper.update_db()

def make_db():
    """
    hololewdのテーブル作成
    """
    hololewd_sqlite.make_table()

def insert(
    flair_text:str,
    url:str,
    date:str,
    score:int):
    """
    レコード追加
    """
    hololewd_sqlite.insert_hololewd(
        flair_text,
        url,
        date,
        score
    )

def search(
    page_no:int=1,
    page_size:int=30,
    flair_text:str='',
    min_score:int=100
):
    """
    レコード検索
    """
    return hololewd_sqlite.search(
        page_no,
        page_size,
        flair_text,
        min_score
    )
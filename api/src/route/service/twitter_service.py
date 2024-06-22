from api.src.route.service.module import twitter_scraper,twitter_sqlite

def get_tweet(hashtag:str, date:int):
    """
    ツイートを取得
    Args:
        hashtag (str): ハッシュタグ
        date (int): 今日から遡る日数
    """
    return twitter_scraper.get_tweet(hashtag, date)

def make_db():
    """
    テーブル作成
    """
    return twitter_sqlite.init()

def search(
        page_no:int=1,
        page_size:int=30,
        hashtag:str='',
        start_date:str='',
        end_date:str='',
        user_name:str='',
        mode:str='',
        min_like:int=0,
        max_like:int=0):
    """
    レコード検索
    """
    return twitter_sqlite.search(
        page_no,
        page_size,
        hashtag,
        start_date,
        end_date,
        user_name,
        mode,
        min_like,
        max_like
    )
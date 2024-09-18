from src.route.service.module import holotwitter_scraper
from src.route.service.module import holotwitter_sqlite as queryServce
from src.route.service.module.utils import interface

def scraping():
    """
    ホロメンのツイート取得処理
    """
    holotwitter_scraper.scraping()

def get_acount():
    """
    ホロメンのアカウントの一覧を取得
    """
    return queryServce.get_acount()

def search(condition:interface.HoloTwitterSearchCondition):
    """
    ホロメンのツイートを検索する
    """
    return queryServce.search_tweet(condition)
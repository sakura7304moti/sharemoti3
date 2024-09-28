# スマブラの切り抜き
from src.route.service.module import ssbu_clip as queryService
from src.route.service.module.utils import interface

def search(condition:interface.SsbuClipSearchCondition):
    """
    切り抜きの検索
    """
    return queryService.search(condition)

def date():
    """
    日付の入力候補
    """
    return queryService.get_dates()

def category():
    """
    種類の入力候補
    """
    return queryService.get_category()

def get_movie(dir_name:str, file_name:str):
    """
    切り抜きを渡して動画のフルパスを取得
    """
    return queryService.get_movie(dir_name, file_name)

def save_clips():
    """
    切り抜きのテーブルアップデート
    """
    queryService.save_clips()
from src.route.service.module import word_collection
from src.route.service.module.utils import interface


def search_word(condition: interface.SearchWordCellectionCondition):
    """
    名言の検索
    """
    return word_collection.search_word(condition)


def get_kinen_count():
    """
    500n記念の数を取得
    """
    return word_collection.get_kinen_count()

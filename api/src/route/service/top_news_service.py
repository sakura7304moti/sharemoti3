from src.route.service.module import top_news

def get_top_news(page_no:int, page_size = 5):
    """
    最近追加したニュースを取得
    """
    return top_news.get_news(page_no, page_size)
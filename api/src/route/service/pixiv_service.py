from src.route.service.module import pixiv_scraper,pixiv_sqlite

def scraping():
    """
    ・pixivをスクレイピング
    ・DBの更新
    """
    pixiv_scraper.holo_pixiv_update()

def search_illust(
    hashtags:list[str] = [],
    user_id:int = 0,
    min_total_bookmarks:int = 0,
    min_total_view:int = 0,
    page_no:int = 1,
    page_size:int = 20
):
    """
    pixivの検索
    Args:
        hashtags : 含めるハッシュタグの一覧
        user_id : ユーザーid
        min_total_bookmarks : ブックマークの最小値
        min_total_view : 閲覧数の最小値
        page_no : 1からスタート、ページ番号
        page_size : 取得最大レコード数
    Returns:
        DataFrame : 検索結果
        totalCount : レコード件数
    """
    df = pixiv_sqlite.search_illust(
        hashtags = hashtags,
        user_id = user_id,
        min_total_bookmarks = min_total_bookmarks,
        min_total_view = min_total_view,
        page_no = page_no,
        page_size = page_size
    )
    count = pixiv_sqlite.search_illust_count(
        hashtags = hashtags,
        user_id = user_id,
        min_total_bookmarks = min_total_bookmarks,
        min_total_view = min_total_view
    )
    return df,count

def get_images(id:int):
    """
    画像データの一覧を取得
    Args:
        id : イラストid
    Returns:
        DataFrame : id, line, その他はサイズ別の画像URL
    """
    return pixiv_sqlite.get_images(id)

def search_hashtags(name:str):
    """
    ハッシュタグの部分一致検索
    Args:
        name : ハッシュタグ名・翻訳語のハッシュタグ名
    Returns:
        DataFrame
    """
    return pixiv_sqlite.search_hashtags(name)

def search_users(name:str):
    """
    ユーザーの検索
    Args:
        name : ユーザーid・ユーザー名(部分一致)・ユーザーアカウント名
    Returns:
        DataFrame
    """
    return pixiv_sqlite.search_users(name)
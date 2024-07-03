import sqlite3
from src.route.service.module.utils import const
import pandas as pd
import json

p = const.Path()
dbname = p.db_pixiv()

def db_connection():
    """
    pixivのdbの接続情報
    """
    return sqlite3.connect(dbname)

# イラストの検索
def search_illust_param_set(
    hashtags:list[str],
    user_id:int,
    min_total_bookmarks:int,
    min_total_view:int
):
    """
    検索用のクエリ・パラメータを取得
    """
    args = {
        'user':user_id,
        'bookmark':min_total_bookmarks,
        'view':min_total_view
    }

    query = """
    SELECT 
        id,
        title AS title,
        type AS type,
        caption AS caption,
        user_id AS userId,
        create_date AS createDate,
        page_count AS pageCount,
        width AS width,
        height AS height,
        sanity_level AS sanityLevel,
        total_view AS totalView,
        total_bookmarks AS totalBookmarks,
        illust_ai_type AS illustAiType
    FROM illust
    WHERE id in (
            SELECT hs.id FROM illust AS il
            LEFT JOIN hashtag AS hs ON il.id = hs.id
            where 1 = 1 
    """
    if user_id > 0:
        query = query + 'and il.user_id = :user '
    
    if min_total_bookmarks > 0:
        query = query + 'and il.total_bookmarks >= :bookmark '
    
    if min_total_view > 0:
        query = query + 'and il.total_view >= :view '

    query = query + ' )'

    for tag in hashtags:
        query = query + f"and id in (select id from hashtag where name = '{tag}') "

    return query, args

def search_illust(
    hashtags:list[str] = [],
    user_id:int = 0,
    min_total_bookmarks:int = 0,
    min_total_view:int = 0,
    page_no:int = 1,
    page_size:int = 20
):
    """
    ページング検索
    """
    base_query,args = search_illust_param_set(
            hashtags,
            user_id,
            min_total_bookmarks,
            min_total_view
    )
    
    offset = (max(page_no - 1,0))*page_size
    
    query = f"""
        {base_query}
        ORDER BY create_date, id desc
        LIMIT {page_size} OFFSET {offset}
    """
    with db_connection() as conn:
        df = pd.read_sql(query, conn, params = args)
        return df

def search_illust_count(
    hashtags:list[str] = 0,
    user_id:int = 0,
    min_total_bookmarks:int = 0,
    min_total_view:int = 0
):
    """
    ページング無しの件数
    """
    base_query,args = search_illust_param_set(
        hashtags,
        user_id,
        min_total_bookmarks,
        min_total_view
    )
    query = f"SELECT count(*) as cn from ({base_query})"
    with db_connection() as conn:
        df = pd.read_sql(query, conn, params = args)
        return df.iloc[0, 0]

def get_images(id:int):
    """
    イラストのIDを元に画像データを取得
    """
    query = """
        SELECT
            id,
            line,
            image_url_square_medium as imageUrlSquareMedium,
            image_url_medium as imageUrlMedium,
            image_url_large as imageUrlLarge,
            original_image_url as originalImageUrl
        FROM image
        WHERE id = :id
        order by line
    """
    args = {"id":id}
    with db_connection() as conn:
        df = pd.read_sql(query, conn, params = args)
        return df

def search_hashtags(name:str):
    """
    ハッシュタグの検索
    """
    query ="""
    SELECT 
        distinct(name) as name,
        translated_name as translatedName
    FROM hashtag
    WHERE name like :name OR translated_name like :name
    """

    args = {"name":f"%{name}%"}
    with db_connection() as conn:
        df = pd.read_sql(query, conn, params = args)
        return df

def search_users(name:str):
    """
    ユーザーの検索
    """
    query = """
    SELECT
        id,
        name,
        account,
        profile_image_url_square_medium as profileImageUrlSquareMedium,
        profile_image_url_medium as profileImageUrlMedium,
        profile_image_url_large as profileImageUrlLarge
    FROM user
    WHERE id = :name OR name like :likeName OR account = :name
    """

    args = {"name":name, "likeName":f"%{name}%"}
    with db_connection() as conn:
        df = pd.read_sql(query, conn, params = args)
        return df
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
    text:str,
    hashtags:list[str],
    user_ids:list[int],
    min_total_bookmarks:int,
    min_total_view:int
):
    """
    検索用のクエリ・パラメータを取得
    """
    args = {
        'text':f"%{text}%",
        'bookmark':min_total_bookmarks,
        'view':min_total_view
    }

    query = """
    SELECT 
        id,
        title AS title,
        type AS type,
        '' AS caption,
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
    
    if min_total_bookmarks > 0:
        query = query + 'and il.total_bookmarks >= :bookmark '
    
    if min_total_view > 0:
        query = query + 'and il.total_view >= :view '

    query = query + ' )'

    """
    修正前
    for tag in hashtags:
        query = query + f"and id in (select id from hashtag where name = '{tag}') "

    for user_id in user_ids:
        query = query + f"and id in (select id from illust where user_id = '{user_id}')"
    """
    


    for i, tag in enumerate(hashtags):
        param_name = f"tag{i}"
        query += f"and id in (select id from hashtag where name = :{param_name}) "
        args[param_name] = tag
    
    for i, user_id in enumerate(user_ids):
        param_name = f"user_id{i}"
        query += f"and id in (select id from illust where user_id = :{param_name}) "
        args[param_name] = user_id

    if text != '':
        query = query + """
        and id in (
            select il.id from illust as il 
            left join user as us on il.user_id = us.id 
            left join hashtag as hs on il.id = hs.id 
            where
                il.title LIKE :text OR 
                us.name LIKE :text OR
                hs.name LIKE :text OR
                hs.translated_name LIKE :text
            
        )
        """

    return query, args

def search_illust(
    text:str,
    hashtags:list[str] = [],
    user_ids:list[int] = [],
    min_total_bookmarks:int = 0,
    min_total_view:int = 0,
    page_no:int = 1,
    page_size:int = 20
):
    """
    ページング検索
    """
    base_query,args = search_illust_param_set(
            text,
            hashtags,
            user_ids,
            min_total_bookmarks,
            min_total_view
    )
    
    offset = max(page_no - 1,0)*page_size
    
    query = f"""
        {base_query}
        ORDER BY create_date desc, id desc
        LIMIT {page_size} OFFSET {offset}
    """
    with db_connection() as conn:
        df = pd.read_sql(query, conn, params = args)
        return df

def search_illust_count(
    text:str,
    hashtags:list[str] = 0,
    user_ids:list[int] = [],
    min_total_bookmarks:int = 0,
    min_total_view:int = 0
):
    """
    ページング無しの件数
    """
    base_query,args = search_illust_param_set(
        text,
        hashtags,
        user_ids,
        min_total_bookmarks,
        min_total_view
    )
    query = f"SELECT count(*) as cn from ({base_query})"
    with db_connection() as conn:
        df = pd.read_sql(query, conn, params = args)
        return int(df.iloc[0, 0])

def get_illust_data(id:int):
    query = """
        SELECT 
            id,
            title AS title,
            type AS type,
            '' AS caption,
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
        where id = :id
    """
    with db_connection() as conn:
        df = pd.read_sql(query, conn, params = {
            "id" : id
        })
    illust_json = df.to_json(orient='records',force_ascii=False)[1:-1]
    return illust_json
    
    

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

def search_hashtags(name:str, id:int):
    """
    ハッシュタグの検索
    """
    query ="""
    SELECT 
        distinct(name) as name,
        translated_name as translatedName
    FROM hashtag
    WHERE 1 = 1 
    """
    if id > 0:
        query = query + "and id = :id "
    if name != '':
        query = query + "and name like :name OR translated_name like :name "

    args = {"name":f"%{name}%", "id":id}
    with db_connection() as conn:
        df = pd.read_sql(query, conn, params = args)
        df['name'] = df['name'].astype(str)
        df = df.sort_values('name')
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
    order by name
    """

    args = {"name":name, "likeName":f"%{name}%"}
    with db_connection() as conn:
        df = pd.read_sql(query, conn, params = args)
        return df
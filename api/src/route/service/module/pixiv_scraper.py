#-----------------------------------------
# 必要な変数をセット
#-----------------------------------------
import os
import sys
import time
import sqlite3


from tqdm import tqdm
from pixivpy3 import *


from src.route.service.module.utils import const

#-----------------------------------------
# 必要な変数をセット
#-----------------------------------------
def get_api():
    """
    検索に使用する
    """
    api = AppPixivAPI()
    api.auth(refresh_token="kBn2GtDM4l3JJiVXLJBsa0BOl0s_p2JUU9wQlTHalqk")
    return api

p = const.Path()
dbname = p.db_pixiv()
save_dir = os.path.join(p.archive(), "pixiv")
opt = const.Option()
members = opt.holo_wiki_members()

api = get_api()

#-----------------------------------------
# API検索
#-----------------------------------------
def search_illusts(query:str):
    """
    pixivで指定したキーワードで全データ検索
    """
    # 検索条件
    illusts = []
    keyword = f"{query} 000user"
    
    # 初回検索（最初のページを取得）
    json_result = api.search_illust(word=keyword)
    time.sleep(1)
    illusts.extend(json_result.illusts)
    
    # 検索結果が無くなるまで検索
    while json_result:
        illusts.extend(json_result.illusts)
        
        # 次のページが存在する場合は次のページを取得
        if 'next_url' in json_result:
            next_qs = api.parse_qs(json_result.next_url)
            if next_qs is None:
                return illusts
            json_result = api.search_illust(**next_qs)
            time.sleep(1)
        else:
            return illusts

#-----------------------------------------
# テーブル追加
#-----------------------------------------
def execute_query_only(query:str):
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    cur.execute(query)
    
    con.commit()
    con.close()


def make_tables():
    """
    テーブル作成
    """
    illust_query = """CREATE TABLE IF NOT EXISTS illust(
                            id INTEGER PRIMARY KEY,
                            title STRING,
                            type STRING,
                            caption STRING,
                            user_id INTEGER,
                            create_date STRING,
                            page_count INTEGER,
                            width INTEGER,
                            height INTEGER,
                            sanity_level INTEGER,
                            total_view INTEGER,
                            total_bookmarks INTEGER,
                            illust_ai_type INTEGER
                        )
                    """
    
    hashtag_query = """CREATE TABLE IF NOT EXISTS hashtag(
                            id INTEGER NOT NULL,
                            name STRING NOT NULL,
                            translated_name STRING
                        )
                    """
    
    user_query = """CREATE TABLE IF NOT EXISTS user(
                        id INTEGER PRIMARY KEY,
                        name STRING,
                        account STRING,
                        profile_image_url_square_medium STRING,
                        profile_image_url_medium STRING,
                        profile_image_url_large STRING
                    )
                 """
    
    image_query = """CREATE TABLE IF NOT EXISTS image(
                        id INTEGER NOT NULL,
                        line INTEGER NOT NULL,
                        image_url_square_medium STRING,
                        image_url_medium STRING,
                        image_url_large STRING,
                        original_image_url STRING
                    )
                  """
    
    querys = [
        illust_query, hashtag_query, user_query, image_query
    ]
    for query in querys:
        execute_query_only(query)


#-----------------------------------------
# レコード追加
#-----------------------------------------

def execute(query:str, args:dict):
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    cur.execute(query, args)
    
    con.commit()
    con.close()

def insert_illust_query():
    return """
            INSERT INTO illust
            SELECT * FROM
            (
                SELECT
                    :id,
                    :title,
                    :type,
                    :caption,
                    :user_id,
                    :create_date,
                    :page_count,
                    :width,
                    :height,
                    :sanity_level,
                    :total_view,
                    :total_bookmarks,
                    :illust_ai_type
                WHERE NOT EXISTS
                (
                    SELECT 1 FROM illust WHERE
                    id = :id
                )
            )
            """

def args_illust(illust):
    return {
        'id':illust.id,
        'title':illust.title,
        'type':illust.type,
        'caption':illust.caption,
        'user_id':illust.user.id,
        'create_date':illust.create_date,
        'page_count':illust.page_count,
        'width':illust.width,
        'height':illust.height,
        'sanity_level':illust.sanity_level,
        'total_view':illust.total_view,
        'total_bookmarks':illust.total_bookmarks,
        'illust_ai_type':illust.illust_ai_type
    }

def insert_hashtag_query():
    return """
        INSERT INTO hashtag
            SELECT * FROM
            (
                SELECT
                    :id,
                    :name,
                    :translated_name
                WHERE NOT EXISTS
                (
                    SELECT 1 FROM hashtag
                    WHERE
                        id = :id
                        and name =:name
                )
            )
    """

def args_list_hashtag(illust):
    args_list = []
    for tag in illust.tags:
        args_list.append(
            {
                'id' : illust.id,
                'name' : tag.name,
                'translated_name' :tag.translated_name
            }
        )
    return args_list

def insert_user_query():
    return """
        INSERT INTO user
            SELECT * FROM
            (
                SELECT
                    :id,
                    :name,
                    :account,
                    :profile_image_url_square_medium,
                    :profile_image_url_medium,
                    :profile_image_url_large
                WHERE NOT EXISTS
                (
                    SELECT 1 FROM user
                    WHERE id = :id
                )
            )
    """

def args_user(illust):
    return {
        "id":illust.user.id,
        "name":illust.user.name,
        "account":illust.user.account,
        "profile_image_url_square_medium":illust.user.profile_image_urls.get('square_medium'),
        "profile_image_url_medium":illust.user.profile_image_urls.get('medium'),
        "profile_image_url_large":illust.user.profile_image_urls.get('large')
    }

def insert_image_query():
    return """
        INSERT INTO image
            SELECT * FROM
            (
                SELECT
                    :id,
                    :line,
                    :image_url_square_medium,
                    :image_url_medium,
                    :image_url_large,
                    :original_image_url
                WHERE NOT EXISTS
                (
                    SELECT 1 FROM image
                    WHERE id = :id and line = :line
                )
            )
    """

def args_list_image(illust):
    args_list = []
    urls = [page.image_urls for page in illust.meta_pages]
    if len(urls) == 0:
        urls.append(illust.image_urls)
        
    for index, image_url in enumerate(urls):
        args_list.append({
            "id":illust.id,
            "line":index,
            "image_url_square_medium":image_url.square_medium,
            "image_url_medium":image_url.medium,
            "image_url_large":image_url.large,
            "original_image_url":image_url.original
        })
    return args_list

#-----------------------------------------
# 更新クエリ
#-----------------------------------------
def update_illust_query():
    return """
        UPDATE illust 
        SET 
            title = :title,
            type = :type,
            caption = :caption,
            user_id = :user_id,
            create_date = :create_date,
            page_count = :page_count,
            width = :width,
            height = :height,
            sanity_level = :sanity_level,
            total_view = :total_view,
            total_bookmarks = :total_bookmarks,
            illust_ai_type = :illust_ai_type
        WHERE id = :id
    """

def update_user_query():
    return """
        UPDATE user
        SET
            name = :name,
            account = :account,
            profile_image_url_square_medium = :profile_image_url_square_medium,
            profile_image_url_medium = :profile_image_url_medium,
            profile_image_url_large = :profile_image_url_large
        WHERE id = :id
    """

#-----------------------------------------
# illustを元にテーブルの更新
#-----------------------------------------

def execute_illust(illust):
    query = insert_illust_query()
    args = args_illust(illust)
    execute(query, args)

    query = update_illust_query()
    execute(query, args)


def execute_hashtag(illust):
    query = insert_hashtag_query()
    args_list = args_list_hashtag(illust)
    for args in args_list:
        execute(query, args)

def execute_user(illust):
    query = insert_user_query()
    args = args_user(illust)
    execute(query, args)

    query = update_user_query()
    execute(query, args)

def execute_image(illust):
    query = insert_image_query()
    args_list = args_list_image(illust)
    for args in args_list:
        execute(query, args)
    

def update_db(illust):
    """
    イラストのオブジェクトを元にDBを更新
    """
    execute_illust(illust)
    execute_hashtag(illust)
    execute_user(illust)
    execute_image(illust)

#-----------------------------------------
# Main
#-----------------------------------------
def holo_pixiv_update():
    """
    全ホロメンのPixivアートをDBに保存
    """
    make_tables()
    for member in tqdm(members):
        tqdm.write(f"\rName: \033[92m{member}\033[0m", end='')
        query = f"{member} 000user"
        illusts = search_illusts(query)
        for illust in illusts:
            update_db(illust)
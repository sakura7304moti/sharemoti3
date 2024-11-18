"""
検索につかうやつ
"""
from src.route.service.module.utils import const, interface
from src.route.service.module import holotwitter_scraper

import math

p = const.Path()
dbname = p.db_holotwitter()
query_base = const.PsqlBase()

def get_acount():
    """
    アカウントの一覧を取得
    """
    query = """
    SELECT
        name,
        screen_name as "screenName",
        profile_image as "profileImage"
    from holo.holox_user
    order by name
    """
    return query_base.execute_df(query)

def search_tweet(condition:interface.HoloTwitterSearchCondition):
    """
    ツイートを検索
    ・部分一致文字列
    ・アカウント名
    ・ページNo
    ・ページサイズは外から指定はできるが、20固定
    ・日付の範囲

    取得要素
    ・id
    ・ツイート内容
    ・作成日
    ・ユーザー名
    """
    def to_query(cond:interface.HoloTwitterSearchCondition):
        query = """
        SELECT
            tw.id,
            tw.text,
            datetime(tw.created_at, '+9 hours') as "createdAt",
            tw.user_screen_name as "userScreenName",
            us.name as "userName",
            us.profile_image as "profileImage" 
        from
            holo.holox_tweet as tw
        left join holo.holox_user as us 
        on tw.user_screen_name = us.screen_name
        where 1 = 1 
        """
        if cond.text != "":
            query += "and (tw.text like %(likeText)s or tw.user_screen_name like %(likeText)s) "

        if cond.acount_name != "":
            query += "and tw.user_screen_name = %(acountName)s "

        if cond.start_date != "":
            query += "and tw.created_at >= %(startDate)s "

        query += """
        order by tw.created_at desc 
        """
        return query
    
    # 1ページのレコード取得
    query = to_query(condition)
    query += "limit %(pageSize)s offset %(offset)s"
    args = condition.to_args()
    args["offset"] = (max(condition.page_no - 1,0))*condition.page_size
    df = query_base.execute_df(query, args) 

    # ページ数を取得
    sub_query = to_query(condition)
    page_query = f"""
    SELECT count(*) as total from (
        {sub_query}
    ) A"""
    page_df = query_base.execute_df(page_query, args)
    total_count = math.ceil(int(page_df["total"].iloc[0]) / condition.page_size )
    
    return df,total_count

"""
あと作成するエンドポイント
・IDに対するメディアのリスト
・動画のURLをもとにダウンロード yt-dlp
"""

def get_media(id:int):
    """
    メディアのリスト
    """
    query = """
    SELECT
        type,
        url,
        media_url as "mediaUrl",
        meta_image_url as "metaImageUrl"
    from holo.holox_media
        where tweet_id = %(id)s
    """
    return query_base.execute_df(query, {"id":id})
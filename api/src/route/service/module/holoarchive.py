import datetime
from datetime import datetime,timedelta
import requests
from tqdm import tqdm
import os


from tqdm import tqdm

from src.route.service.module.utils import const, interface

psql_model = const.PsqlBase()
#p = const.Path()
opt = const.Option()
channel_url_list = opt.youtube_holo_channels()

"""
データベース用の関数
"""
def search_movie(
    page_no = 1,
    page_size = 20,
    title = '',
    from_date = '',
    to_date = '',
    channel_id = '',
    movie_type = ''
):
    # SELECTクエリを実行
    query,args = search_query_args(
        page_size = page_size,
        page_no = page_no,
        title = title,
        from_date = from_date,
        to_date = to_date,
        channel_id = channel_id,
        movie_type = movie_type
    )
    return psql_model.execute_df(query,args)

def search_movie_count(
    page_size = 0,
    title = '',
    from_date = '',
    to_date = '',
    channel_id = '',
    movie_type = ''
):
    """
    ページ数を取得する
    """
    query,args = search_query_args(
        1,
        0,
        title,
        from_date,
        to_date,
        channel_id,
        movie_type
    )# page_no = 1 , page_size = 0(max)
    count_query = f'select count(*) as total from ({query}) as movie'
    df = psql_model.execute_df(count_query,args)
    return int(df["total"].iloc[0]) 

def search_query_args(
    page_no = 1,
    page_size = 20,
    title = '',
    from_date = '',
    to_date = '',
    channel_id = '',
    movie_type = ''
):
    """
    検索に使用する。クエリとargsを取得。
    """
    #ページング設定
    offset = (max(page_no - 1,0))*page_size 
    
    query = """
        SELECT 
            id,
            url,
            title,
            published_date as "date",
            channel_id as "channelId",
            view_count as "viewCount",
            thumbnail_url as "thumbnailUrl",
            movie_type as "movieType"
        FROM holo.youtube_movie where 1 = 1 
    """
    if title != '':
        query = query + "and title like %(title)s "
    if from_date != '':
        query = query + "and published_date >= %(from_date)s "
    if to_date != '':
        query = query + "and published_date <= %(to_date)s "
    if channel_id != '':
        query = query + "and channel_id = %(channel_id)s "
    if movie_type != '':
        query = query + "and movie_type = %(movie_type)s "
    
    query = query + "order by published_date desc,title "
    
    if page_size != 0:
        query = query + "limit %(page_size)s offset %(offset)s "
    
    args = {
        'title' : f'%{title}%',
        'from_date' : from_date,
        'to_date' : to_date,
        'channel_id' : channel_id,
        'movie_type' : movie_type,
        'page_size' : page_size,
        'offset' : offset
    }
    return query , args

def search_channel():
    df = psql_model.execute_df(
        """
            SELECT 
                id,
                channel_id as "channelId",
                channel_name as "channelName",
                description,
                header_url as "headerUrl",
                avatar_url as "avatarUrl"
            FROM holo.youtube_channel                       
        """
    )
    return df

def insert_movie(
    id:str,
    url:str,
    title:str,
    date:str,
    channel_id:str,
    view_count:int,
    thumbnail_url:str,
    movie_type:str
):
    if is_exists_video(id):
        update_movie(
            id,
            url,
            title,
            view_count,
            thumbnail_url
        )
    else:
        query = """
        INSERT INTO holo.youtube_movie (id, url, title, published_date, channel_id, view_count, thumbnail_url, movie_type) 
                VALUES (%(id)s, %(url)s, %(title)s, %(date)s, %(channel_id)s, %(view_count)s, %(thumbnail_url)s, %(movie_type)s)
        """
        args = {
            "id":id,
            "url":url,
            "title":title,
            "date":date,
            "channel_id":channel_id,
            "view_count":view_count,
            "thumbnail_url":thumbnail_url,
            "movie_type":movie_type
        }
        psql_model.execute_commit(query, args)


def insert_channel(
    channel_id:str,
    channel_name:str,
    description:str,
    header_url:str,
    avatar_url:int
):
    query = """
    INSERT INTO holo.youtube_channel (channel_id, channel_name, description, header_url, avatar_url) 
               VALUES (%(channel_id)s, %(channel_name)s, %(description)s, %(header_url)s, %(avatar_url)s)
    """
    args = {
        "channel_id":channel_id,
        "channel_name":channel_name,
        "description":description,
        "header_url":header_url,
        "avatar_url":avatar_url
    }

    psql_model.execute_commit(query, args)

def update_movie(
    id:str,
    url:str,
    title:str,
    view_count:int,
    thumbnail_url:str,
):
    query = """
    UPDATE holo.youtube_movie SET
        url = %(url)s,
        title = %(title)s,
        view_count = %(view_count)s,
        thumbnail_url = %(thumbnail_url)s
    WHERE id = %(id)s
    """
    args = {
        "id":id,
        "url":url,
        "title":title,
        "view_count":view_count,
        "thumbnail_url":thumbnail_url
    }
    
    psql_model.execute_commit(query, args)

def update_channel(
    channel_id:str,
    channel_name:str,
    description:str,
    header_url:str,
    avatar_url:int
):
    query = """
    UPDATE holo.youtube_channel SET
        channel_name = %(channel_name)s,
        description = %(description)s,
        header_url = %(header_url)s,
        avatar_url = %(avatar_url)s 
    WHERE channel_id = %(channel_id)s
    """
    args = {
        "channel_id":channel_id,
        "channel_name":channel_name,
        "description":description,
        "header_url":header_url,
        "avatar_url":avatar_url
    }
    
    psql_model.execute_commit(query, args)

def is_exists_video(id:str):
    query = f"""
    select
        id
    from holo.youtube_movie
    where id = '{id}'
    """ 
    df = psql_model.execute_df(query)
    return len(df) > 0

def get_api_key():
    try:
        share_path = os.environ['SHAREMOTI_YOUTUBE_API']
        return share_path
    except Exception as e:
        print(f"\033[31m APIキーの取得エラー {e.with_traceback} \033[0m")

def update_archives():
    channel_df = search_channel()
    for _, row in tqdm(channel_df.iterrows(), total=len(channel_df)):
        id = row['id']
        channel_id = row['channelId']

        playlist_id = get_playlist_id(id)
        videos = get_videos_from_playlist(playlist_id, days=30)

        # DBに追加
        for video in videos:
            video_id = video['video_id']
            insert_movie(
                id = video_id,
                url = 'https://www.youtube.com/watch?v=' + video_id,
                title = video['title'],
                date = video['published_at'].strftime("%Y-%m-%d %H:%M:%S"),
                channel_id=channel_id,
                view_count=0,
                thumbnail_url=f'http://img.youtube.com/vi/{video_id}/maxresdefault.jpg',
                movie_type=video['type']
            )

def get_playlist_id(channel_id:str):
    """
    チャンネルIDからアップロードプレイリストIDを取得
    """
    API_KEY = get_api_key()
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        "part": "contentDetails",
        "id": channel_id,
        "key": API_KEY,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()  # エラー時に例外を発生させる
    data = response.json()
    
    # アップロードプレイリストIDを取得
    return data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

def get_videos_from_playlist(playlist_id, days=5):
    """
    プレイリストIDから動画一覧を取得し、過去指定日数以内の動画を返す
    """
    API_KEY = get_api_key()
    url = "https://www.googleapis.com/youtube/v3/playlistItems"
    one_month_ago = datetime.utcnow() - timedelta(days=days)
    next_page_token = None
    videos = []

    while True:
        params = {
            "part": "snippet",
            "playlistId": playlist_id,
            "maxResults": 50,
            "key": API_KEY,
            "pageToken": next_page_token,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        for item in data["items"]:
            video_id = item["snippet"]["resourceId"]["videoId"]
            video_title = item["snippet"]["title"]
            published_at = item["snippet"]["publishedAt"]
            
            # 公開日をチェック
            published_date = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")

            # 進捗を更新
            step_days = abs((one_month_ago - published_date).days - 30)

            if published_date >= one_month_ago:
                # 動画の種別を判定
                video_type = ''
                if '#short' in video_title:
                    video_type = 'short'

                videos.append({
                    "video_id": video_id,
                    "title": video_title,
                    "published_at": published_date,
                    "type": video_type,
                })

        # 次のページがあるか確認
        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break

    return videos

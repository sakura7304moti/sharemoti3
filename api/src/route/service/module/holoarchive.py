import sqlite3
import yt_dlp
import datetime
import math


from typing import List
from tqdm import tqdm
from pytube import YouTube

from src.route.service.module.utils import const, interface

p = const.Path()
opt = const.Option()
channel_url_list = opt.youtube_holo_channels()


"""
検索用の関数
"""
def get_yt_info(url:str):
    """
    yt-dlpでチャンネルの情報を取得。数秒かかる。
    """
    # オプションを設定
    ydl_opts = {
        'quiet': True,  # 出力を非表示
        'extract_flat': True,  # プレイリスト内の各動画を一つのリストに展開
        # その他のオプションは必要に応じて設定
    }
    
    # yt-dlpオブジェクトを生成
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    
    # プレイリストからURLリストを取得
    with ydl:
        result = ydl.extract_info(url, download=False)
    return result

def get_channel_info(result):
    """
    チャンネルの情報を元にconst.ChannelInfoを作成
    """
    #チャンネルid
    channel_id = result['uploader_id']

    #チャンネル名
    channel_name = result['channel'].replace('"','')
    
    #概要
    description = ''
    try:
        description = result['description'].replace('"','')
    except:
        pass
    
    
    #ヘッダー画像URL
    header_url = ''
    try:
        for rec in result['thumbnails']:
            if 'resolution' in rec:
                if rec['resolution'] == '1920x1080':
                    header_url = rec['url']
    except:
        pass
                
    #プロフィール画像URL
    avatar_url = result['thumbnails'][-2]['url']
    return interface.ChannelInfo(channel_id,channel_name,description,header_url,avatar_url)

def get_thumbnail_url(id):
    return f'http://img.youtube.com/vi/{id}/maxresdefault.jpg'

def get_movie_info(entrie):
    id = entrie['id']
    url = entrie['url']
    title = entrie['title'].replace('"','')
    if 'view_count' in entrie:
        view_count = entrie['view_count']
        thumbnail_url = get_thumbnail_url(id)
        return [id,url,title,view_count,thumbnail_url]
    else:
        return None
    
def get_movie_list(entries):
    movie_list = []
    for rec in entries:
        info = get_movie_info(rec)
        if info is not None:
            movie_info = interface.MovieInfo(info[0],info[1],info[2],'','',info[3],info[4],'')
            movie_list.append(movie_info)
    return movie_list

def inferece_channenl(url:str) -> interface.Archive:
    """
    チャンネルの情報やアーカイブを取得する
    """
    result = get_yt_info(url)
    channel = get_channel_info(result)
    #動画
    movie = get_movie_list(result['entries'][0]['entries'])

    #ショート
    short = get_movie_list(result['entries'][1]['entries'])

    #live
    try:
        live = get_movie_list(result['entries'][2]['entries'])
    except:
        live = get_movie_list(result['entries'][1]['entries'])
        short = []

    archive = interface.Archive(channel,movie,short,live)
    return archive

def get_upload_date(url:str):
    """
    # オプションを設定
    ydl_opts = {
        'quiet': True,  # 出力を非表示
        'date':True,
        'output':'%(upload_date)'
        # その他のオプションは必要に応じて設定
    }
    
    # yt-dlpオブジェクトを生成
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    
    # プレイリストからURLリストを取得
    with ydl:
        result = ydl.extract_info(url, download=False)
        stamp = result['release_timestamp']
        if stamp is None:
            stamp = result['upload_date']
            # yyyymmdd形式の文字列をdatetimeオブジェクトに変換
            dt = datetime.datetime.strptime(stamp, '%Y%m%d')
        
            # yyyy-mm-dd形式の文字列に変換
            stamp = dt.strftime('%Y-%m-%d')
            return stamp
        else:
            return str(datetime.datetime.fromtimestamp(stamp))
    """
    # YouTubeオブジェクトの作成
    yt = YouTube(url)

    # 投稿日の取得
    publish_date = yt.publish_date
    return publish_date

    
        

def holo_archives() -> List[interface.Archive]:
    archives = []
    for url in tqdm(channel_url_list,desc="get archives"):
        archive = inferece_channenl(url)
        archives.append(archive)
    return archives

def update_archives():
    #日付以外全て取得する
    archives = holo_archives()

    #追加前にレコード取得
    make_database()
    movies = search_movie()
    channels = search_channel()

    # ----- チャンネル単位のループ -----
    for archive in tqdm(archives,desc="archives"):
        #チャンネルの追加・更新
        if archive.channel.channel_id in [c.channel_id for c in channels]:
            update_channel(
                archive.channel.channel_id,
                archive.channel.channel_name,
                archive.channel.description,
                archive.channel.header_url,
                archive.channel.avatar_url)
        else:
            insert_channel(
                archive.channel.channel_id,
                archive.channel.channel_name,
                archive.channel.description,
                archive.channel.header_url,
                archive.channel.avatar_url)
            
            
        #動画の追加・更新
        for movie in archive.movie:
            if movie.id in [m.id for m in movies]:
                update_movie(
                    movie.id,
                    movie.url,
                    movie.title,
                    movie.view_count,
                    movie.thumbnail_url,
                )
            else:
                upload_date = get_upload_date(movie.url)
                insert_movie(
                    movie.id,
                    movie.url,
                    movie.title,
                    upload_date,
                    archive.channel.channel_id,
                    movie.view_count,
                    movie.thumbnail_url,
                    'movie'
                )
        #ショートの追加・更新
        for movie in archive.short:
            if movie.id in [m.id for m in movies]:
                update_movie(
                    movie.id,
                    movie.url,
                    movie.title,
                    movie.view_count,
                    movie.thumbnail_url,
                )
            else:
                upload_date = get_upload_date(movie.url)
                insert_movie(
                    movie.id,
                    movie.url,
                    movie.title,
                    upload_date,
                    archive.channel.channel_id,
                    movie.view_count,
                    movie.thumbnail_url,
                    'short'
                )
        #ライブの追加・更新
        for movie in archive.live:
            if movie.id in [m.id for m in movies]:
                update_movie(
                    movie.id,
                    movie.url,
                    movie.title,
                    movie.view_count,
                    movie.thumbnail_url,
                )
            else:
                upload_date = get_upload_date(movie.url)
                insert_movie(
                    movie.id,
                    movie.url,
                    movie.title,
                    upload_date,
                    archive.channel.channel_id,
                    movie.view_count,
                    movie.thumbnail_url,
                    'live'
                )

"""
データベース用の関数
"""
dbname = p.db_youtube()
def make_database():
    #dbファイル作成
    conn = sqlite3.connect(dbname)
    conn.close()

    #動画のテーブル
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS movie(
                id STRING PRIMARY KEY,
                url STRING,
                title STRING,
                date STRING,
                channel_id STRING,
                view_count INTEGER,
                thumbnail_url STRING,
                movie_type STRING
                )
                """)
    # データベースへコミット。これで変更が反映される。
    conn.commit()
    conn.close()

    #チャンネルのテーブル
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS channel(
                channel_id STRING PRIMARY KEY,
                channel_name STRING,
                description STRING,
                header_url STRING,
                avatar_url STRING
                )
                """)
    # データベースへコミット。これで変更が反映される。
    conn.commit()
    conn.close()

def search_movie(
    page_no = 1,
    page_size = 20,
    title = '',
    from_date = '',
    to_date = '',
    channel_id = '',
    movie_type = ''
) -> List[interface.MovieInfo]:
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

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
    cursor.execute(query,args)
    results = cursor.fetchall()
    
    # 接続を閉じる
    conn.close()

    # 結果を表示
    records = []
    for row in results:
        rec = interface.MovieInfo(*row)
        records.append(rec)

    return records

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
    
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    #件数のみ取得
    count_query = f'select count(*) from ({query})'
    cursor.execute(count_query,args)
    results = cursor.fetchall()
    conn.close()

    count = results[0][0]
    page_count = math.floor(count/page_size)

    return page_count

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
    
    query = "SELECT * FROM movie where 1 = 1 "
    if title != '':
        query = query + "and title like :title "
    if from_date != '':
        query = query + "and date >= :from_date "
    if to_date != '':
        query = query + "and date <= :to_date "
    if channel_id != '':
        query = query + "and channel_id = :channel_id "
    if movie_type != '':
        query = query + "and movie_type = :movie_type "
    
    query = query + "order by date desc,title "
    
    if page_size != 0:
        query = query + "limit :page_size offset :offset "
    
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

def search_channel() -> List[interface.ChannelInfo]:
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM channel")
    results = cursor.fetchall()

    # 接続を閉じる
    conn.close()

    # 結果をまとめる
    records = []
    for row in results:
        rec = interface.ChannelInfo(*row)
        records.append(rec)
    
    return records

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
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    query = """
    INSERT OR IGNORE INTO movie (id, url, title, date, channel_id, view_count, thumbnail_url, movie_type) 
               VALUES (:id, :url, :title, :date, :channel_id, :view_count, :thumbnail_url, :movie_type)
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
    
    cursor.execute(query,args)
    conn.commit()
    conn.close()

def insert_channel(
    channel_id:str,
    channel_name:str,
    description:str,
    header_url:str,
    avatar_url:int
):
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    query = """
    INSERT INTO channel (channel_id, channel_name, description, header_url, avatar_url) 
               VALUES (:channel_id, :channel_name, :description, :header_url, :avatar_url)
    """
    args = {
        "channel_id":channel_id,
        "channel_name":channel_name,
        "description":description,
        "header_url":header_url,
        "avatar_url":avatar_url
    }
    
    cursor.execute(query,args)
    conn.commit()
    conn.close()

def update_movie(
    id:str,
    url:str,
    title:str,
    view_count:int,
    thumbnail_url:str,
):
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    query = """
    UPDATE movie SET
        url = :url,
        title = :title,
        view_count = :view_count,
        thumbnail_url = :thumbnail_url
    WHERE id = :id
    """
    args = {
        "id":id,
        "url":url,
        "title":title,
        "view_count":view_count,
        "thumbnail_url":thumbnail_url
    }
    
    cursor.execute(query,args)
    conn.commit()
    conn.close()

def update_channel(
    channel_id:str,
    channel_name:str,
    description:str,
    header_url:str,
    avatar_url:int
):
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    query = """
    UPDATE channel SET
        channel_name = :channel_name,
        description = :description,
        header_url = :header_url,
        avatar_url = :avatar_url 
    WHERE channel_id = :channel_id
    """
    args = {
        "channel_id":channel_id,
        "channel_name":channel_name,
        "description":description,
        "header_url":header_url,
        "avatar_url":avatar_url
    }
    
    cursor.execute(query,args)
    conn.commit()
    conn.close()



    
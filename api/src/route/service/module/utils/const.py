import glob
import os
from typing import List
import pandas as pd
import yaml
import requests
import sqlite3
import datetime
import psycopg2


from sqlalchemy import create_engine


from .interface import HoloName, SsbuNameRecord

def get_new_line_text() -> str:
    """改行用の空文字を取得"""
    return "jsdlkjflasjfiojadispfosdjfposdj"

def tmp_file_name(ext:str):
    """一時ファイルの保存先を取得"""
    tmp_dir = Path.rembg_temp
    os.makedirs(tmp_dir,exist_ok=True)
    files = glob.glob(os.path.join(tmp_dir,'*'))
    return os.path.join(tmp_dir, f"{str(len(files)).zfill(8)}.{ext}")

def  line_notify(notification_message:str):
    """
    LINEに通知する
    """
    line_notify_token = 'dMby6IiqpTb24ZwgV2T3wQyHw5CBII7uky7fR38nuQv'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'message: {notification_message}'}
    requests.post(line_notify_api, headers = headers, data = data)

def line_handler(func):
    """
    エラー時にlineに通知するデコレータ
    """
    def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                line_notify(f"""{func.__name__}
{e}""")
    return wrapper


class Path:
    """
    パスの取得に使用する
    """


    def root_path(self):
        """
        APIのルートのパス
        """
        path = os.path.abspath(__file__)
        for _ in range(6):
            path = os.path.dirname(path)
        return path
    

    def option(self):
        return os.path.join(self.root_path(), 'option')
    

    def archive(self):
        return os.path.join(self.root_path(), 'archive')
    

    def database(self):
        return os.path.join(self.root_path(), 'src', 'database')
    

    def image_uploads(self):
        """
        画像一覧のページの画像置き場
        """
        return os.path.join(self.archive(), 'img_uploads')
    

    def rembg_temp(self):
        """
        画像の背景除去の一時ファイル置き場
        """
        return os.path.join(self.archive(), 'rembg_temp')
    
    def yt_dlp_temp(self):
        """
        YouTubeの動画データの置き場
        """
        return os.path.join(self.archive(), 'yt_dlp')
    

    def share_folder(self):
        """
        共有フォルダのパス
        """
        try:
            share_path = os.environ['SHARE_FOLDER']
            return share_path
        except Exception as e:
            print(f"\033[31m 共有フォルダのパス取得エラー {e.with_traceback} \033[0m")

    def holo_album(self):
        """
        ホロライブのアルバムのcsv
        """
        return os.path.join(self.archive(), 'holo_album', 'album.csv')
    
    def ssbu_caterogy(self):
        """
        切り抜きの種類のcsv
        """
        return os.path.join(self.option(), 'ssbu_category.csv')
    

    def db_main_share(self):
        """
        名言集などのDB
        """
        return os.path.join(self.database(), 'main_share.db')
    
    def db_ssbu_clip(self):
        """
        スマブラの切り抜き
        """
        return os.path.join(self.database(), 'ssbu.db')
    

    def db_hololewd(self):
        """
        ホロライブのエロ画像のDB
        """
        return os.path.join(self.database(), 'hololewd.db')
    

    def db_twitter(self):
        """
        twitterのDB
        """
        return os.path.join(self.database(), 'twitter.db')
    
    def db_holotwitter(self):
        """
        ホロメンのツイート保存用twitterのDB
        """
        return os.path.join(self.database(), 'holotwitter.db')
    

    def db_youtube(self):
        """
        ホロライブのアーカイブDB
        """
        return os.path.join(self.database(), 'youtube.db')
    
    def db_pixiv(self):
        """
        ホロライブのpixivのDB
        """
        return os.path.join(self.database(), 'pixiv.db')
    
class Option:

    def __init__(self):
        self.p = Path()

    """
    csvやyamlの読み取りに使用する
    """
    def ssbu_names(self) -> List[SsbuNameRecord]:
        """
        スマブラのキャラ名・画像URL・アイコンURL
        """
        df_path = os.path.join(self.p.option(), 'ssbu_names.csv')
        df = pd.read_csv(df_path)
        records = []
        for _, row in df.iterrows():
            name = row["name"]
            url = row["url"]
            icon = row["icon"]
            rec = SsbuNameRecord(name,url,icon)
            records.append(rec)
        return records
    
    def ssbu_category(self):
        """
        カテゴリーのリストを取得
        """
        df = pd.read_csv(os.path.join(self.p.ssbu_caterogy()), index_col=False)
        return df['name'].to_list()
    
    def twitter_holo_hashtags(self) -> List[HoloName]:
        """
        ホロライブのハッシュタグの一覧 + アイコンの画像URL
        """
        df_path = os.path.join(self.p.option(), 'holo_names.csv')
        df = pd.read_csv(df_path)
        df = df.drop_duplicates(subset='hashtag')
        records = []
        for _, row in df.iterrows():
            hashtag = row["hashtag"]
            url = row["url"]
            rec = HoloName(hashtag,url)
            records.append(rec)
        return records
    
    def twitter_base_hashtags(self):
        """
        ホロライブ以外で収集したいハッシュタグの一覧
        """
        df_path = os.path.join(self.p.option(), 'twitter_base_hashtags.csv')
        df = pd.read_csv(df_path)
        return df['hashtag']
    
    def youtube_holo_channels(self) -> List[str]:
        """
        ホロライブのYouTubeチャンネル一覧
        """
        df_path = os.path.join(self.p.option(), 'holo_youtube_channel_url.csv')
        df = pd.read_csv(df_path)
        return df['0'].tolist()
    
    def hololewd_flair_texts(self):
        """
        ホロライブのエロ画像のメンバー名一覧
        """
        path = os.path.join(self.p.option(), 'holo_lewd_flair_texts.csv')
        df = pd.read_csv(path)
        return df['flair_text'].tolist()
    
    def holo_wiki_cover(self) -> str:
        """
        ホロライブ非公式Wikiの歌ってみたのURL
        """
        yaml_path = os.path.join(self.p.option(), 'holo_wiki_urls.yaml')
        with open(yaml_path) as file:
            yml = yaml.safe_load(file)
            return yml['cover']
    
    def holo_wiki_original(self) -> str:
        """
        ホロライブ非公式Wikiのオリ曲のURL
        """
        yaml_path = os.path.join(self.p.option(), 'holo_wiki_urls.yaml')
        with open(yaml_path) as file:
            yml = yaml.safe_load(file)
            return yml['ori']
        
    def holo_wiki_memory(self) -> str:
        """
        ホロライブ非公式Wikiの記念配信のURL
        """
        yaml_path = os.path.join(self.p.option(), 'holo_wiki_urls.yaml')
        with open(yaml_path) as file:
            yml = yaml.safe_load(file)
            return yml['memory']
        
    #ホロメン一覧
    def holo_wiki_members(self):
        holo_path = os.path.join(self.p.option(), "holo_names.csv")
        df = pd.read_csv(holo_path)
        df = df[df["name"].notna()]
        df = df.drop_duplicates(subset='name')
        names = df["name"].tolist()
        return names

    #pixivのホロメン選択に使用
    def holo_pixiv_selecter(self):
        holo_path = os.path.join(self.p.option(), "holo_names.csv")
        df = pd.read_csv(holo_path)
        df = df[df["name"].notna()]
        df = df.drop_duplicates(subset='name')
        return df
    

class DbBase:
    def __init__(self, dbname:str):
        self.dbname = dbname

    def db_connection(self):
        """
        メインのdbの接続情報
        """
        return sqlite3.connect(self.dbname)

    def execute_commit(self, query:str, param: dict | None = None):
        """
        クエリを実行するだけ。commitが必要な場合はこっち。
        """
        con = sqlite3.connect(self.dbname)
        cur = con.cursor()
        if param is None:
            cur.execute(query)
        else:
            cur.execute(query, param)
        
        con.commit()
        con.close()

    def execute_df(self, query:str, param: dict | None = None):
        """
        クエリを実行してデータフレームを取得
        """
        with self.db_connection() as conn:
            if param is None:
                return pd.read_sql(sql = query, con = conn)
            else:
                return pd.read_sql(sql = query, con = conn, params = param)

    def current_time(self):
        """
        現在の日時を取得。
        create_atやupdate_atの日時セットに。
        """
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
class PsqlBase:
    def db_url(self):
        """
        接続URL
        """
        try:
            url = os.environ['SHAREMOTI_DB']
            return url
        except Exception as e:
            print(f"\033[31m DBのURL取得エラー {e.with_traceback} \033[0m")

    def db_connection(self):
        """
        メインのdbの接続情報
        """
        return create_engine("postgresql+psycopg2://sakura0moti:music0@192.168.0.31/sharemoti")

    def execute_commit(self, query:str, param: dict | None = None):
        """
        クエリを実行するだけ。commitが必要な場合はこっち。
        """
        with self.db_connection() as con:
            cur = con.cursor()
            if param is None:
                cur.execute(query)
            else:
                cur.execute(query, param)
            
            con.commit()
            con.close()

    def execute_df(self, query:str, param: dict | None = None):
        """
        クエリを実行してデータフレームを取得
        """
        if param is None:
            return pd.read_sql(sql = query, con = self.db_connection())
        else:
            return pd.read_sql(sql = query, con = self.db_connection(), params = param)

    def current_time(self):
        """
        現在の日時を取得。
        create_atやupdate_atの日時セットに。
        """
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
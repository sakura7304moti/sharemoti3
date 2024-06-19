import glob
import os
from typing import List
import pandas as pd
import yaml

from api.src.route.service.module.utils.interface import HoloName, SsbuNameRecord

def get_new_line_text() -> str:
    """改行用の空文字を取得"""
    return "jsdlkjflasjfiojadispfosdjfposdj"

def tmp_file_name(ext:str):
    """一時ファイルの保存先を取得"""
    tmp_dir = Path.rembg_temp
    os.makedirs(tmp_dir,exist_ok=True)
    files = glob.glob(os.path.join(tmp_dir,'*'))
    return os.path.join(tmp_dir, f"{str(len(files)).zfill(8)}.{ext}")

class Path:
    """
    パスの取得に使用する
    """

    @property
    def root_path(self):
        """
        APIのルートのパス
        """
        path = os.path.abspath(__file__)
        for _ in range(6):
            path = os.path.dirname(path)
        return path
    
    @property
    def option(self):
        return os.path.join(self.root_path, 'option')
    
    @property
    def archive(self):
        return os.path.join(self.root_path, 'arhcive')
    
    @property
    def database(self):
        return os.path.join(self.root_path, 'src', 'database')
    
    @property
    def image_uploads(self):
        """
        画像一覧のページの画像置き場
        """
        return os.path.join(self.archive, 'img_uploads')
    
    @property
    def rembg_temp(self):
        """
        画像の背景除去の一時ファイル置き場
        """
        return os.path.join(self.archive, 'revmg_temp')
    
    @property
    def share_folder(self):
        """
        共有フォルダのパス
        """
        try:
            share_path = os.environ['SHARE_FOLDER']
            return share_path
        except Exception as e:
            print(f"\033[31m 共有フォルダのパス取得エラー {e.with_traceback} \033[0m")
    
    @property
    def db_main_share(self):
        """
        名言集などのDB
        """
        return os.path.join(self.database, 'main_share.db')
    
    @property
    def db_hololewd(self):
        """
        ホロライブのエロ画像のDB
        """
        return os.path.join(self.database, 'hololewd.db')
    
    @property
    def db_twitter(self):
        """
        twitterのDB
        """
        return os.path.join(self.database, 'hololewd.db')
    
    @property
    def db_youtube(self):
        """
        ホロライブのアーカイブDB
        """
        return os.path.join(self.database, 'youtube.db')
    
class Option:
    """
    csvやyamlの読み取りに使用する
    """
    def ssbu_names(self) -> List[SsbuNameRecord]:
        """
        スマブラのキャラ名・画像URL・アイコンURL
        """
        df_path = os.path.join(Path.option, 'ssbu_names.csv')
        df = pd.read_csv(df_path)
        records = []
        for _, row in df.iterrows():
            name = row["name"]
            url = row["url"]
            icon = row["icon"]
            rec = SsbuNameRecord(name,url,icon)
            records.append(rec)
        return records
    
    def twitter_holo_hashtags(self) -> List[HoloName]:
        """
        ホロライブのハッシュタグの一覧 + アイコンの画像URL
        """
        df_path = os.path.join(Path.option, 'holo_twitter_hashtag.csv')
        df = pd.read_csv(df_path)
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
        df_path = os.path.join(Path.option, 'twitter_base_hashtags.csv')
        df = pd.read_csv(df_path)
        return df['hashtag']
    
    def youtube_holo_channels(self) -> List[str]:
        """
        ホロライブのYouTubeチャンネル一覧
        """
        df_path = os.path.join(Path.option, 'holo_youtube_channel_url.csv')
        df = pd.read_csv(df_path)
        return df['0'].tolist()
    
    def hololewd_flair_texts(self):
        """
        ホロライブのエロ画像のメンバー名一覧
        """
        path = os.path.join(Path.option, 'holo_lewd_flair_texts.csv')
        df = pd.read_csv(path)
        return df['flair_text'].tolist()
    
    def holo_wiki_cover(self):
        """
        ホロライブ非公式Wikiの歌ってみたのURL
        """
        yaml_path = os.path.join(Path.option, 'holo_wiki_urls.yaml')
        with open(yaml_path) as file:
            yml = yaml.safe_load(file)
            return yml['cover']
        
    def holo_wiki_original(self):
        """
        ホロライブ非公式Wikiのオリジナル曲のURL
        """
        yaml_path = os.path.join(Path.option, 'holo_wiki_urls.yaml')
        with open(yaml_path) as file:
            yml = yaml.safe_load(file)
            return yml['ori']
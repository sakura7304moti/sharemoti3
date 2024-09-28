import os
import glob
from typing import List
import pandas as pd
import math

from tqdm import tqdm


from src.route.service.module.utils import const, interface

# テーブル操作
p = const.Path()
dbname = p.db_main_share()
query_base = const.DbBase(dbname)

# 切り抜きのベースのパス
SSBU_CLIP_DIR = os.path.join(p.share_folder(), 'スマブラ', '切り抜き')


# ---------------
# 切り抜きの保存用
# ---------------

def get_category():
    """
    カテゴリーのリスト
    """
    opt = const.Option()
    return opt.ssbu_category()

def ssbu_names():
    """
    スマブラのキャラ名
    """
    opt = const.Option()
    return opt.ssbu_names()


def make_table():
    """
    切り抜きデータを保管するテーブルを作成
    """
    ssbu_clip_query = """
    CREATE TABLE IF NOT EXISTS ssbu_clip (
        id INTEGER PRIMARY KEY,
        title TEXT,
        file_name TEXT,
        dir_name TEXT,
        char_name TEXT,
        date TEXT
    );
    """

    ssbu_category_query = """
    CREATE TABLE IF NOT EXISTS ssbu_category (
        id INTEGER,
        name TEXT
    );
    """
    for query in [ssbu_clip_query, ssbu_category_query]:
        query_base.execute_commit(query)

def get_files():
    """
    切り抜きのパスの一覧
    """
    path_list = glob.glob(os.path.join(SSBU_CLIP_DIR,'*','*','*.mp4'))
    path_list.sort()
    return path_list

def get_clip(path:str, index:int, category_list:List[str]) -> interface.SsbuClip:
    """
    パスを切り抜きデータに変換
    """
    file_name = os.path.basename(path)
    result = file_name.split('_')
    if len(result) > 1:
        char_name = result[0]
        title = file_name.replace('.mp4', '').replace(char_name + '_', '')
    else:
        char_name = ''
        title = ''
    dir_name = os.path.dirname(path.replace(SSBU_CLIP_DIR, ''))
    date = os.path.basename(dir_name)
    cates = [c for c in category_list if c in file_name]

    clip = interface.SsbuClip(
        index,
        title,
        file_name,
        char_name,
        dir_name,
        date,
        cates
    )
    return clip

def get_clips():
    """
    全てのパスを切り抜きデータに変換
    """
    path_list = get_files()
    cates = get_category()

    clips = []
    for index,path in enumerate(path_list):
        clip = get_clip(path, index, cates)
        clips.append(clip)
    return clips

def clear_tables():
    """
    テーブルの中身をクリア
    """
    querys = [
        "DELETE FROM ssbu_clip",
        "DELETE FROM ssbu_category"
    ]
    for query in querys:
        query_base.execute_commit(query)

def insert_clip(condition:interface.SsbuClip):
    """
    テーブルにデータを追加
    """
    # 切り抜きの追加
    clip_query = """
    INSERT INTO ssbu_clip(
        id,
        title,
        file_name,
        dir_name,
        char_name,
        date
    )
    VALUES(
        :id,
        :title,
        :fileName,
        :dirName,
        :charName,
        :date
    )
    """
    clip_args = condition.to_args()
    query_base.execute_commit(clip_query, clip_args)

    # 種類の追加
    cate_query = """
    INSERT INTO ssbu_category(
        id,
        name
    )
    VALUES(
        :id,
        :name
    )
    """
    for c in condition.cates:
        cate_args = {
            "id":condition.id,
            "name":c
        }
        query_base.execute_commit(cate_query, cate_args)

def save_clips():
    """
    切り抜きを全て保存
    """
    clips = get_clips()

    make_table()
    clear_tables()

    for clip in tqdm(clips):
        insert_clip(clip)

# ---------------
# 検索用
# ---------------
def get_dates() -> pd.DataFrame:
    """
    日付の一覧を取得
    """
    query = """
    SELECT
        distinct date
    from ssbu_clip
    """
    ls = query_base.execute_df(query)["date"].to_list()
    ls.sort(reverse=True)
    return ls

def search(condition:interface.SsbuClipSearchCondition):
    """
    切り抜き検索
    ・部分一致テキスト
    ・あだ名
    ・キャラ名
    ・日時
    ・種類
    """
    def to_query(cd:interface.SsbuClipSearchCondition):
        # 検索条件 -> クエリ文
        query = """
            WITH clip AS(
            SELECT
                sc.id as id,
                sc.title as title,
                sc.file_name as fileName,
                sc.dir_name as dirName,
                sc.char_name as charName,
                CASE
                    WHEN n1.val is NULL THEN n2.ssbu_name
                    ELSE n1.val
                END as ssbuName,
                sc.date as date
            FROM ssbu_clip as sc
            left join nameList as n1
                on n1.key = sc.char_name
            left join nameList2 as n2
                on n2.name = sc.char_name
            )
            SELECT
                *
            FROM clip
            WHERE 1 = 1 
        """
        if cd.text != "":
            query += """
                AND (
                    clip.fileName like :text
                    OR clip.dirName like :text
                    OR clip.date like :text
                ) """

        if cd.char_name != "":
            query += "AND clip.charName = :charName "
        
        if cd.ssbu_name != "":
            query += "AND clip.ssbuName = :ssbuName "

        if cd.date != "":
            query += "AND clip.date = :date "
        
        if cd.cate != "":
            query += """
                AND EXISTS(
                    SELECT
                        1
                    FROM ssbu_category as ct
                    WHERE
                        ct.id = clip.id
                        AND ct.name = :cate
                )
            """
        query += " order by clip.date desc, clip.fileName"
        return query
    
    def get_records(cd:interface.SsbuClipSearchCondition):
        # 1ページのレコード
        query = to_query(cd)
        query += " limit :pageSize offset :offset"
        args = cd.to_args()
        args["offset"] = (max(cd.page_no - 1,0))*cd.page_size
        df = query_base.execute_df(query, args)

        # 画像のURLをはっつける
        names = ssbu_names()
        urls = []
        icons = []
        for item in df['ssbuName'].to_list():
            recs = [n for n in names if n.name == item]
            if len(recs) == 1:
                urls.append(recs[0].url)
                icons.append(recs[0].icon)
        df["fullIcon"] = urls
        df["smallIcon"] = icons
        return df
    
    def get_total_count(cd:interface.SsbuClipSearchCondition):
        # ページ数
        sub_query = to_query(cd)
        page_query = f"""
            SELECT 
                count(*) as total
            from ({sub_query}) A"""
        args = cd.to_args()
        page_df = query_base.execute_df(page_query, args)
        total_count = math.ceil(int(page_df["total"].iloc[0]) / condition.page_size )
        return total_count
    
    # メインの処理
    df = get_records(condition)
    total_count = get_total_count(condition)
    return df, total_count

def get_movie(dir_name:str, file_name:str):
    """
    動画のフルパスを取得
    """
    return f"{SSBU_CLIP_DIR}{dir_name}/{file_name}"
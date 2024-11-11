import os
import glob
from typing import List
import pandas as pd
import math

from tqdm import tqdm


from src.route.service.module.utils import const, interface

# テーブル操作
p = const.Path()
query_model = const.PsqlBase()

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
        "DELETE FROM sharemoti.ssbu_clip",
        "ALTER SEQUENCE ssbu_clip_id RESTART WITH 1",
        "DELETE FROM sharemoti.ssbu_category"
    ]
    for query in querys:
        query_model.execute_commit(query)

def insert_clip(condition:interface.SsbuClip):
    """
    テーブルにデータを追加
    """
    # 切り抜きの追加
    clip_query = """
    INSERT INTO sharemoti.ssbu_clip(
        title,
        file_name,
        dir_name,
        char_name,
        date
    )
    VALUES(
        %(title)s,
        %(fileName)s,
        %(dirName)s,
        %(charName)s,
        %(date)s
    )
    """
    clip_args = condition.to_args()
    query_model.execute_commit(clip_query, clip_args)

    # 種類の追加
    cate_query = """
    INSERT INTO sharemoti.ssbu_category(
        id,
        name
    )
    VALUES(
        %(id)s,
        %(name)s
    )
    """
    for c in condition.cates:
        cate_args = {
            "id":condition.id + 1,
            "name":c
        }
        query_model.execute_commit(cate_query, cate_args)

def save_clips():
    """
    切り抜きを全て保存
    """
    clips = get_clips()

    #make_table()
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
    from sharemoti.ssbu_clip
    """
    ls = query_model.execute_df(query)["date"].to_list()
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
                sc.file_name as "fileName",
                sc.dir_name as "dirName",
                sc.char_name as "charName",
                n.ssbu_name as "ssbuName",
                sc.date as date
            FROM sharemoti.ssbu_clip as sc
            left join sharemoti.name as n
                on n.name = sc.char_name
            )
            SELECT
                *
            FROM clip
            WHERE 1 = 1 
        """
        if cd.text != "":
            query += """
                AND (
                    clip."fileName" like %(text)s
                    OR clip."dirName" like %(text)s
                    OR clip.date like %(text)s
                ) """

        if cd.char_name != "":
            query += """AND clip."charName" = %(charName)s """
        
        if cd.ssbu_name != "":
            query += """AND clip."ssbuName" = %(ssbuName)s """

        if cd.date != "":
            query += "AND clip.date = %(date)s "
        
        if cd.cate != "":
            query += """
                AND EXISTS(
                    SELECT
                        1
                    FROM sharemoti.ssbu_category as ct
                    WHERE
                        ct.id = clip.id
                        AND ct.name = %(cate)s
                )
            """
        query += """ order by clip.date desc, clip."fileName" """
        return query
    
    def get_records(cd:interface.SsbuClipSearchCondition):
        # 1ページのレコード
        query = to_query(cd)
        query += " limit %(pageSize)s offset %(offset)s"
        args = cd.to_args()
        args["offset"] = (max(cd.page_no - 1,0))*cd.page_size
        df = query_model.execute_df(query, args)

        # 画像のURLをはっつける
        names = ssbu_names()
        urls = []
        icons = []
        for item in df['ssbuName'].to_list():
            recs = [n for n in names if n.name == item]
            if len(recs) == 1:
                urls.append(recs[0].url)
                icons.append(recs[0].icon)
            else:
                urls.append('')
                icons.append('')
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
        page_df = query_model.execute_df(page_query, args)
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
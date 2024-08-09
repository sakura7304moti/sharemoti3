"""
スマブラのクリップ一覧
"""
import os
import glob

from src.route.service.module.utils import const,interface
p = const.Path()
DATA_PATH = p.share_folder()

"""
クリップの一覧を取得
"""
def search():
    path_list = glob.glob(os.path.join(DATA_PATH,'スマブラ','切り抜き','*','*','*.mp4'))
    records = []
    for path in path_list:
        id = path_list.index(path)
        file_name = os.path.basename(path).split('.')[0]
        dir_path = os.path.dirname(path)
        date = os.path.basename(dir_path)
        dir_path_u = os.path.dirname(dir_path)
        year = os.path.basename(dir_path_u)
        file_path = os.path.join(year, date, os.path.basename(path))
        rec = interface.ssbuListRecord(id,file_name,date,year, file_path)
        
        records.append(rec)
    return records

"""
IDをもとに動画の要素を取得
"""
def select(path:str):
    movie_path = os.path.join(DATA_PATH,'スマブラ','切り抜き', path)
    if os.path.exists(movie_path):
        file_name = os.path.basename(path).split('.')[0]
        dir_path = os.path.dirname(path)
        date = os.path.basename(dir_path)
        dir_path_u = os.path.dirname(dir_path)
        year = os.path.basename(dir_path_u)
        file_path = os.path.join(year, date, os.path.basename(path))
        rec = interface.ssbuListRecord(id,file_name,date,year, file_path)
        return rec

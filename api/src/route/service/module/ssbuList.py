"""
スマブラのクリップ一覧
"""
import os
import glob

from api.src.route.service.module.utils import const,interface
DATA_PATH = const.Path.file_data_dir

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
        rec = interface.ssbuListRecord(id,file_name,date,year)
        records.append(rec)
    return records

"""
IDをもとに動画の要素を取得
"""
def select(select_id:int):
    path_list = glob.glob(os.path.join(DATA_PATH,'スマブラ','切り抜き','*','*','*.mp4'))
    for path in path_list:
        id = path_list.index(path)
        if id == select_id:
            file_name = os.path.basename(path).split('.')[0]
            dir_path = os.path.dirname(path)
            date = os.path.basename(dir_path)
            dir_path_u = os.path.dirname(dir_path)
            year = os.path.basename(dir_path_u)
            rec = interface.ssbuListRecord(id,file_name,date,year)
            break
    return rec

"""
カラオケ動画の一覧
"""
import os
import glob

from api.src.route.service.module.utils import const
DATA_PATH = const.Path.file_data_dir


"""
音声の一覧を取得
"""
def search():
    path_list = glob.glob(os.path.join(DATA_PATH,'カラオケ','音声のみ','*','*.mp3'))
    records = []
    for path in path_list:
        id = path_list.index(path)
        file_name = os.path.basename(path).split('.')[0]
        dir_path = os.path.dirname(path)
        date = os.path.basename(dir_path)

        rec = file_const.KaraokeListRecord(id,file_name,date)
        records.append(rec)
    return records

"""
IDをもとに動画の要素を取得
"""
def select(select_id:int):
    path_list = glob.glob(os.path.join(DATA_PATH,'カラオケ','音声のみ','*','*.mp3'))
    for path in path_list:
        id = path_list.index(path)
        if id == select_id:
            file_name = os.path.basename(path).split('.')[0]
            dir_path = os.path.dirname(path)
            date = os.path.basename(dir_path)
            rec = file_const.KaraokeListRecord(id,file_name,date)
            print(rec)
            break
    return rec

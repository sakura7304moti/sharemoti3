"""
ヴォイスの一覧
"""
import os
import glob


from api.src.route.service.module.utils import const,interface
DATA_PATH = const.Path.file_data_dir


"""
音声の一覧を取得
"""
def search():
    path_list = glob.glob(os.path.join(DATA_PATH,'ボイス','*.mp3'))
    records = []
    for path in path_list:
        id = path_list.index(path)
        file_name = os.path.basename(path).split('.')[0]
        rec = interface.VoiceListRecord(id,file_name)
        records.append(rec)
    return records

"""
IDをもとに動画の要素を取得
"""
def select(select_id:int):
    path_list = glob.glob(os.path.join(DATA_PATH,'ボイス','*.mp3'))
    for path in path_list:
        id = path_list.index(path)
        if id == select_id:
            file_name = os.path.basename(path).split('.')[0]
            rec = interface.VoiceListRecord(id,file_name)
            break
    return rec

"""
トップ用に画像をランダムで取得
"""
import os
import glob
import random

from src.route.service.module.utils import const,interface
p = const.Path()
DATA_PATH = p.share_folder()

"""
画像の一覧を取得
"""

# 画像の一覧
def image_list():
    path_list = glob.glob(os.path.join(DATA_PATH,'画像','写真','旅の思い出','*','*','*.jpg'))
    return path_list

# リストからランダムに選択する
def get_image(path_list:list[str]):
    index = random.randint(0, len(path_list) - 1)
    return path_list[index]
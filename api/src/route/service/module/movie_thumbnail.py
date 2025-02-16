# 動画のサムネイル画像を一括で作成する処理
# ファイル名を元に画像のデータを取得する
from src.route.service.module.utils import const
import glob
import os
import cv2
import random

p = const.Path()
UPLOAD_FOLDER = p.movie_uploads()

THUMNAIL_FOLDER = p.movie_thumbnails_uploads()
query_model = const.PsqlBase()


def get_update_movies():
    query = """
    SELECT
        file_name as "fileName"
    from sharemoti.movie
    where
        thumbnail_flg = 1
    """
    df = query_model.execute_df(query)
    names = df["fileName"].tolist()
    return names


def create_thumbnail(path: str):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print(f"動画がひらけませんでした -> {path}")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames == 0:
        print(f"フレームが見つかりませんでした -> {path}")
        return

    frame_no = random.randint(0, total_frames - 1)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
    ret, frame = cap.read()
    if ret:
        save_path = get_thumbnail_path(path)
        cv2.imwrite(save_path, frame)
    else:
        print(f"フレームが読み取れませんでした -> {path}")


def update_thumbnail_all():
    names = get_update_movies()
    for name in names:
        path = os.path.join(UPLOAD_FOLDER, name)
        create_thumbnail(path)


def get_thumbnail_path(file_name: str):
    return os.path.join(
        THUMNAIL_FOLDER, os.path.basename(file_name).split(".")[0] + ".jpg"
    )

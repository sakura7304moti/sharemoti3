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


def update_thumbnail_all():
    movies = glob.glob(os.path.join(UPLOAD_FOLDER, "*"))
    for path in movies:
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            print(f"動画がひらけませんでした -> {path}")
            continue

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames == 0:
            print(f"フレームが見つかりませんでした -> {path}")
            continue

        frame_no = random.randint(0, total_frames - 1)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        ret, frame = cap.read()
        if ret:
            save_path = get_thumbnail_path(path)
            cv2.imwrite(save_path, frame)
        else:
            print(f"フレームが読み取れませんでした -> {path}")


def get_thumbnail_path(file_name: str):
    return os.path.join(
        THUMNAIL_FOLDER, os.path.basename(file_name).split(".")[0] + ".jpg"
    )

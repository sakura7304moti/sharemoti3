"""
OmuTube
"""

import math
import random
import cv2
import os


from src.route.service.module.utils import const, interface
from src.route.service.module import movie_thumbnail

query_model = const.PsqlBase()
path_model = const.Path()

"""
・作成
・更新
・削除
"""


def create(condition: interface.Movie):
    query = """
    INSERT INTO sharemoti.movie(
        title,
        detail,
        file_name,
        thumbnail_flg,
        staff_cd,
        create_at,
        update_at
    ) VALUES (
        %(title)s,
        %(detail)s,
        %(fileName)s,
        %(thumbnailFlg)s,
        %(staffCd)s,
        %(current_time)s, 
        %(current_time)s
    )
    """
    args = condition.to_args()
    args["current_time"] = query_model.current_time()
    query_model.execute_commit(query, args)

    # サムネイル作成
    path = os.path.join(path_model.movie_uploads(), condition.file_name)
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
        save_path = movie_thumbnail.get_thumbnail_path(path)
        cv2.imwrite(save_path, frame)
    else:
        print(f"フレームが読み取れませんでした -> {path}")


def update(condition: interface.Movie):
    query = """
    UPDATE sharemoti.movie
    SET
        title = %(title)s,
        detail = %(detail)s,
        thumbnail_flg = %(thumbnailFlg)s,
        update_at = %(current_time)s 
    where
        id = %(id)s
    """
    args = condition.to_args()
    args["current_time"] = query_model.current_time()
    query_model.execute_commit(query, args)


def delete(id: int):
    query = "DELETE FROM sharemoti.movie WHERE id = %(id)s"
    args = {"id": id}
    query_model.execute_commit(query, args)


def get_id(file_name: str) -> int:
    query = """
    SELECT
        id as id
    from sharemoti.movie
    where
        file_name = %(fileName)s
    """
    args = {"fileName": file_name}
    df = query_model.execute_df(query, args)
    return int(df.iloc[0]["id"])


def search_params(keyword: str, hashtag: str):
    query = """
    SELECT
        mv.id,
        mv.title,
        mv.detail,
        mv.file_name AS "fileName",
        mv.thumbnail_flg AS "thumbnailFlg",
        mv.staff_cd AS "staffCd",
        TO_CHAR(mv.create_at, 'YYYY-MM-DD') as "createAt",
        TO_CHAR(mv.update_at, 'YYYY-MM-DD') as "updateAt"
    FROM
        sharemoti.movie AS mv
    WHERE
    """
    if keyword == "":
        query += """
        1 = 0  
        """
    else:
        query += """
        mv.title LIKE %(keyword)s
        OR mv.detail LIKE %(keyword)s
        OR EXISTS (
            SELECT
                hs.name
            FROM
                sharemoti.movie_hashtag AS hs
            WHERE
                hs.name LIKE %(keyword)s
                AND mv.id = hs.movie_id
        ) 
        """

    if hashtag == "":
        query += """
        OR 1 = 0 
        """
    else:
        query += """
        OR EXISTS (
            SELECT
                hs.name
            FROM
                sharemoti.movie_hashtag AS hs
            WHERE
                hs.name = %(hashtag)s
                AND mv.id = hs.movie_id
        ) 
        """

    if keyword == "" and hashtag == "":
        query += """
        OR 1 = 1
        """
    query += """
    ORDER BY
        mv.create_at DESC,
        mv.update_at DESC
    """
    args = {"keyword": f"%{keyword}%", "hashtag": hashtag}
    return query, args


def search(keyword: str, hashtag: str, page_no: int, page_size: int):
    query, args = search_params(keyword, hashtag)
    query += " limit %(pageSize)s offset %(offset)s"
    args["offset"] = (max(page_no - 1, 0)) * page_size
    args["pageSize"] = page_size
    return query_model.execute_df(query, args)


def search_total_count(keyword: str, hashtag: str, page_size: int):
    sub_query, args = search_params(keyword, hashtag)
    query = f"""
    SELECT 
        count(*) as total
    from ({sub_query}) A
    """
    df = query_model.execute_df(query, args)
    total = int(df["total"].iloc[0])
    return math.ceil(total / page_size)


def get_movie_hashtags(id_list: list[int]):
    id_where = "({})".format(",".join(map(str, id_list)))
    query = f"""
    SELECT
        movie_id as "movieId",
        name,
        is_group as "isGroup"
    from sharemoti.movie_hashtag
    WHERE
        movie_id in {id_where}
    order by movie_id, name 
    """
    df = query_model.execute_df(query)
    return df

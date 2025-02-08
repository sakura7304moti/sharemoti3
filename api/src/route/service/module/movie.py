"""
OmuTube
"""

import math
from src.route.service.module.utils import const, interface

query_model = const.PsqlBase()

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

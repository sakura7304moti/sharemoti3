"""
OmuTube
"""

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

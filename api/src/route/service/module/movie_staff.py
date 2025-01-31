"""
OmuTube
"""

"""
・名前の更新
・プロフィール画像の更新
"""

from src.route.service.module.utils import const, interface

query_model = const.PsqlBase()


def update(staff_cd: int, name: str):
    query = """
    UPDATE sharemoti.movie_staff
    SET
        name = %(name)s,
        update_at = %(current_time)s 
    where 
        staff_cd = %(staffCd)s
    """
    args = {
        "staffCd": staff_cd,
        "name": name,
        "current_time": query_model.current_time(),
    }
    query_model.execute_commit(query, args)


def change_icon(staff_cd: int, icon_path: str):
    """
    サーバー側に写真は適当なUIDのファイル名で保存した前提
    """
    query = """
    UPDATE sharemoti.movie_staff
    SET
        icon = %(icon)s,
        update_at = %(current_time)s 
    where 
        staff_cd = %(staffCd)s
    """
    args = {
        "staffCd": staff_cd,
        "icon": icon_path,
        "current_time": query_model.current_time(),
    }
    query_model.execute_commit(query, args)

"""
OmuTube
"""

from src.route.service.module.utils import const, interface

query_model = const.PsqlBase()

"""
・作成
・削除
"""


def create(movie_id: int, name: str):
    query = """
    INSERT INTO sharemoti.movie_hashtag(
        movie_id,
        name,
        is_group
    )
    SELECT
        %(id)s,
        %(name)s,
        0
    WHERE NOT EXISTS(
        SELECT 1 FROM sharemoti.movie_hashtag as hs
        where hs.movie_id = %(id)s and hs.name = %(name)s
    )
    
    """
    args = {"id": movie_id, "name": name}
    query_model.execute_commit(query, args)


def delete(movie_id: int, name: str):
    query = """
    DELETE FROM sharemoti.movie_hashtag 
    WHERE 
        movie_id = %(id)s AND name = %(name)s
    """
    args = {"id": movie_id, "name": name}
    query_model.execute_commit(query, args)


def delete_movie(movie_id: int):
    query = """
    DELETE FROM sharemoti.movie_hashtag 
    WHERE 
        movie_id = %(id)s
    """
    args = {"id": movie_id}
    query_model.execute_commit(query, args)


def hashtag_list():
    query = """
    SELECT
        name,
        max(is_group) as "isGroup"
    from sharemoti.movie_hashtag
    group by name
    order by name
    """
    return query_model.execute_df(query)


def update_group(name: str, is_group: bool):
    query = """
    UPDATE sharemoti.movie_hashtag
    SET
        is_group = %(isGroup)s
    where
        name = %(name)s
    """
    args = {"name": name, "isGroup": 1 if is_group else 0}
    query_model.execute_commit(query, args)


def change_tagname(before_name: str, after_name: str):
    query = """
    UPDATE sharemoti.movie_hashtag
    SET
        name = %(after)s
    WHERE
        name = %(before)s
    """
    args = {"before": before_name, "after": after_name}
    query_model.execute_commit(query, args)


def delete_hashtag_by_name(name: str):
    query = """
    DELETE FROM sharemoti.movie_hashtag
    where name = %(name)s
    """
    args = {"name": name}
    query_model.execute_commit(query, args)

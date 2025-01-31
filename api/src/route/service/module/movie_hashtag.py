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
        name
    )
    SELECT
        %(id)s,
        %(name)s
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

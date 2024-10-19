"""
俳句一覧
"""
from src.route.service.module.utils import const,interface
query_model = const.PsqlBase()

def insert(condition:interface.Haiku):
    query = """
        INSERT INTO sharemoti.haiku (
            first, 
            second,
            third,
            poster,
            detail,
            create_at,
            update_at
        ) VALUES (
            %(first)s, 
            %(second)s, 
            %(third)s, 
            %(poster)s, 
            %(detail)s, 
            %(current_time)s, 
            %(current_time)s
        )"""
    args = condition.to_args()
    args['current_time'] = query_model.current_time()
    query_model.execute_commit(query, args)

def update(condition:interface.Haiku):
    query = """
    UPDATE sharemoti.haiku 
    SET 
        first = %(first)s, 
        second = %(second)s, 
        third = %(third)s, 
        poster = %(poster)s, 
        detail = %(detail)s, 
        update_at = %(current_time)s 
    WHERE 
        id = %(id)s
    """
    args = condition.to_args()
    args['current_time'] = query_model.current_time()
    query_model.execute_commit(query, args)

def delete(id:int):
    query = "DELETE FROM sharemoti.haiku WHERE id = %(id)s"
    args = {"id":id}
    query_model.execute_commit(query, args)

def select():
    query = """
        SELECT
            id,
            first,
            second,
            third,
            poster,
            detail,
            TO_CHAR(create_at, 'YYYY-MM-DD') as "createAt",
            TO_CHAR(update_at, 'YYYY-MM-DD') as "updateAt"
        from sharemoti.haiku
        order by create_at, id
    """
    return query_model.execute_df(query)
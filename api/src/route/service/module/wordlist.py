"""
名言集 API
"""
from src.route.service.module.utils import const,interface
query_model = const.PsqlBase()

def insert(condition:interface.Word):
    query = """
    INSERT INTO sharemoti.word(
        word,
        detail,
        create_at,
        update_at
    )
    VALUES(
        %(word)s,
        %(detail)s,
        %(current_time)s,
        %(current_time)s
    )
    """
    args = condition.to_args()
    args['current_time'] = query_model.current_time()
    query_model.execute_commit(query, args)

def custom_insert(
        word:str,
        detail:str,
        create_at,
        update_at
):
    query = """
    INSERT INTO sharemoti.word(
        word,
        detail,
        create_at,
        update_at
    )
    VALUES(
        %(word)s,
        %(detail)s,
        %(create_at)s,
        %(update_at)s
    )
    """
    args = {
        "word":word,
        "detail":detail,
        "create_at":create_at,
        "update_at":update_at
    }
    query_model.execute_commit(query, args)


def update(condition:interface.Word):
    query = """
        UPDATE sharemoti.word
        SET
            word = %(word)s,
            detail = %(detail)s,
            update_at = %(current_time)s
        where id = %(id)s    
    """
    args = condition.to_args()
    args['current_time'] = query_model.current_time()
    query_model.execute_commit(query, args)


"""
DELETE
"""
def delete(id:int):
    query = """
        DELETE FROM sharemoti.word
        where id = %(id)s  
    """
    args = {"id" : id}
    query_model.execute_commit(query, args)


"""
SELECT
"""
def search(text: str = ""):
    query = """
        SELECT
            id,
            word,
            detail,
            TO_CHAR(create_at, 'YYYY-MM-DD') as "createAt",
            TO_CHAR(update_at, 'YYYY-MM-DD') as "updateAt"
        from sharemoti.word
        order by create_at, word
    """
    #args = {"text", f"%{text}%"}
    return query_model.execute_df(query)
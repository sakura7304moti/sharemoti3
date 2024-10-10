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
        :word,
        :detail,
        :current_time,
        :current_time
    )
    """
    args = condition.to_args()
    args['current_time'] = query_model.current_time()
    query_model.execute_commit(query, args)


def update(condition:interface.Word):
    query = """
        UPDATE sharemoti.word
        SET
            word = :word,
            detail = :detail,
            update_at = :current_time
        where id = :id    
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
        where id = :id
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
            create_at as createAt,
            update_at as updateAt
        from sharemoti.word
        where text like :text
        order by create_at, word
    """
    args = {"text", text}
    return query_model.execute_df(query, args)
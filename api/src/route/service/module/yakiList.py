"""
焼き直し条約 API
"""
from src.route.service.module.utils import const
query_model = const.PsqlBase()

def exists(
    word:str,
    yaki:str
):
    query = "SELECT * FROM yakiList2 where word = :word and yaki = :yaki"
    args = {
        "word":word,
        "yaki":yaki
    }
    df = query_model.execute_df(query, args)

    return len(df) > 0
    

def insert(
    word:str,
    yaki:str
):
    query = """
        INSERT INTO 
        sharemoti.yaki (
            word, 
            yaki, 
            create_at, 
            update_at
        ) VALUES (
            %(word)s, 
            %(yaki)s, 
            %(current_time)s,
            %(current_time)s
        )"""
    current_time = query_model.current_time()
    args = {
        "word": word, 
        "yaki" : yaki, 
        "current_time" : current_time,
    }
    query_model.execute_commit(query, args)

def insert_custom(
    word:str,
    yaki:str,
    create_at,
    update_at
):
    query = """
        INSERT INTO 
        sharemoti.yaki (
            word, 
            yaki, 
            create_at, 
            update_at
        ) VALUES (
            %(word)s, 
            %(yaki)s, 
            %(create_at)s,
            %(update_at)s
        )"""
    args = {
        "word": word, 
        "yaki" : yaki, 
        "create_at" : create_at,
        "update_at" : update_at
    }
    query_model.execute_commit(query, args)
        
def update(
    id:int,
    word:str,
    yaki:str
):
    query = """
        UPDATE sharemoti.yaki Set 
            word = %(word)s, 
            yaki = %(yaki)s, 
            update_at = %(current_time)s
        WHERE id = %(id)s
    """
    current_time = query_model.current_time()
    args = {
        "id" : id,
        "word" : word,
        "yaki" : yaki,
        "current_time" : current_time
    }
    query_model.execute_commit(query, args)

def delete(id:int):
    query = "DELETE FROM sharemoti.yaki WHERE id = %(id)s"
    args = {"id" : id}
    query_model.execute_commit(query, args)

def search():
    query = """
        SELECT
            id,
            word,
            yaki,
            TO_CHAR(create_at, 'YYYY-MM-DD') as "createAt",
            TO_CHAR(update_at, 'YYYY-MM-DD') as "updateAt"
        from sharemoti.yaki
        order by create_at
    """
    return query_model.execute_df(query)
"""
あだ名一覧2 API
"""
import sqlite3
import datetime

from src.route.service.module.utils import const, interface
p = const.Path()
dbname = p.db_main_share()
query_model = const.PsqlBase()

def exists(
    name:str,
    ssbu_name:str
):
    # データベースに接続する
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    query = "SELECT * FROM nameList2 where name = :name and ssbu_name = :ssbu_name"
    args = {
        "name":name,
        "ssbu_name":ssbu_name
    }

    #検索
    cursor.execute(query,args)
    results = cursor.fetchall()

    #閉じる
    conn.close()

    return len(results) > 0
    

def insert(
    name:str,
    ssbu_name:str
):
    query = """
        INSERT INTO sharemoti.name(
            name, ssbu_name, create_at, update_at
        ) VALUES (
            %(name)s, 
            %(ssbu_name)s, 
            %(current_time)s, 
            %(current_time)s 
        )
    """
    args = {
        "name": name, 
        "ssbu_name" : ssbu_name, 
        "current_time" : query_model.current_time()
    }
    query_model.execute_commit(query, args)
    
def insert_custom(
    name:str,
    ssbu_name:str,
    create_at,
    update_at
):
    query = """
    INSERT INTO sharemoti.name(
        name, ssbu_name, create_at, update_at
    ) VALUES (%(name)s, %(ssbu_name)s, %(create_at)s, %(update_at)s )
    """
    args = {"name": name, "ssbu_name" : ssbu_name, "create_at" : create_at, "update_at" : update_at}
    query_model.execute_commit(query, args)
        
def update(
    id:int,
    name:str,
    ssbu_name:str
):
    query = """
        UPDATE sharemoti.name Set 
            name = %(name)s, 
            ssbu_name = %(ssbu_name)s, 
            update_at = %(current_time)s
        WHERE id = %(id)s
    """
    args = {
        "id" : id,
        "name" : name,
        "ssbu_name" : ssbu_name,
        "current_time" : query_model.current_time()
    }
    query_model.execute_commit(query, args)

def delete(id:int):
    query = "DELETE FROM sharemoti.name WHERE id = %(id)s"
    args = {"id" : id}
    query_model.execute_commit(query, args)

def search():
    query = """
        SELECT
            id,
            name,
            ssbu_name as "ssbuName",
            TO_CHAR(create_at, 'YYYY-MM-DD') as "createAt",
            TO_CHAR(update_at, 'YYYY-MM-DD') as "updateAt"
        from sharemoti.name
        where is_display = TRUE
        order by create_at, name
    """
    return query_model.execute_df(query)
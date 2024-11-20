"""
画像一覧
"""
import sqlite3
import datetime

from src.route.service.module.utils import const, interface
p = const.Path()
dbname = p.db_main_share()
query_model = const.PsqlBase()
    
"""
INSERT
"""
def insert(condition:interface.Image):
    query = """
        INSERT INTO sharemoti.image(
            file_name,
            ext, 
            title, 
            detail, 
            create_at, 
            update_at
        ) VALUES (
            %(fileName)s, 
            %(ext)s,  
            %(title)s, 
            %(detail)s, 
            now(), 
            now()
        )
        """
    query_model.execute_commit(query, condition.to_args())
    
"""
UPDATE
更新できるのはタイトルと詳細のみ
"""
def update(condition:interface.Image):
    query = """
    UPDATE sharemoti.image 
    SET 
        title = %(title)s, 
        detail = %(detail)s, 
        update_at = now() 
    WHERE 
        id = %(id)s
    """
    query_model.execute_commit(query, condition.to_args())
    
    
"""
DELETE
"""
def delete(id:int):
    query = "DELETE FROM sharemoti.image where id = %(id)s"
    args = {'id' : id}
    query_model.execute_commit(query, args)
    
"""
検索
"""
def search(page_no:int, page_size:int):
    base_query = """
        SELECT
            id,
            file_name as "fileName",
            ext,
            title,
            detail,
            create_at as "createAt",
            update_at as "updateAt"
        from sharemoti.image
        order by id
        
    """
    data_query = base_query + " offset :offset limit :limit"

    args = {
        'offset' : max(page_no - 1, 0) * page_size,
        'limit' : page_size
    }
    df = query_model.execute_df(data_query, args)

    count_df = query_model.execute_df(base_query)
    return df, len(count_df)
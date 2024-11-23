"""
画像一覧
"""
import math
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
    before_full_file_name = get_file_name(condition.id)
    after_full_file_name = f'{condition.file_name}.{condition.ext}'
    if before_full_file_name != after_full_file_name:
        query = """
        UPDATE sharemoti.image 
        SET 
            file_name = %(fileName)s, 
            ext = %(ext)s, 
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
            TO_CHAR(create_at, 'YYYY-MM-DD') as "createAt",
            TO_CHAR(update_at, 'YYYY-MM-DD') as "updateAt"
        from sharemoti.image
        order by create_at desc
        
    """
    data_query = base_query + " offset %(offset)s limit %(limit)s"

    args = {
        'offset' : max(page_no - 1, 0) * page_size,
        'limit' : page_size
    }
    df = query_model.execute_df(data_query, args)

    count_df = query_model.execute_df(base_query)
    total_count = math.ceil(len(count_df) / page_size)
    return df, total_count

def get_file_name(id:int) -> str:
    query = """
        SELECT
            (file_name || '.' || ext) as "fileName"
        from sharemoti.image
        where id = %(id)s
    """
    args = {'id':id}
    df = query_model.execute_df(query, args)
    return str(df.iat[0,0])

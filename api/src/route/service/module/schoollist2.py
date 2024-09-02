"""
学校の一覧と学校のコメント
"""

from src.route.service.module.utils import const, interface


p = const.Path()
dbname = p.db_main_share()
query_base = const.DbBase(dbname)


def make_table():
    """
    テーブルの作成
    ・学校
    ・コメント
    """
    school_query = """
    CREATE TABLE IF NOT EXISTS school(
        id INTEGER PRIMARY KEY,
        school_name STRING,
        principal STRING,
        detail STRING,
        slogan STRING,
        create_at STRING,
        update_at STRING
    )
    """

    comment_query = """
    CREATE TABLE IF NOT EXISTS school_comment(
        id INTEGER PRIMARY KEY,
        school_id INTEGER,
        star INTEGER,
        title STRING,
        comment STRING,
        post_person STRING,
        create_at STRING,
        update_at STRING
    )
    """

    query_base.execute_commit(school_query)
    query_base.execute_commit(comment_query)

def get_school():
    """
    学校の一覧を取得
    """
    query = """
    SELECT
        id as Id,
        school_name as SchoolName,
        principal as Principal,
        detail as Detail,
        slogan as Slogan,
        create_at as CreateAt,
        update_at as UpdateAt
    from school
    order by id
    """
    return query_base.execute_df(query)
    
def get_comment(id:int):
    """
    学校のコメントの一覧を取得
    """
    query = """
    SELECT
        id as Id,
        school_id as SchoolId,
        star as Star,
        title as Title,
        comment as Comment,
        post_person as PostPerson,
        create_at as CreateAt,
        update_at as UpdateAt
    from school_comment

    order by id
    """
    args = {"schoolId":id}
    return query_base.execute_df(query, args)
    
def create_school(condition:interface.SchoolQueryRecord):
    """
    学校の作成
    """
    query = """
    INSERT INTO school(
        school_name, 
        principal, 
        detail, 
        slogan, 
        create_at, 
        update_at
    )
    VALUES(
        :schoolName,
        :principal,
        :detail,
        :slogan,
        :currentTime,
        :currentTime
    )
    """
    args = condition.to_args()
    args["currentTime"] = query_base.current_time()
    query_base.execute_commit(query, args)

def create_comment(condition:interface.SchoolCommentQueryRecord):
    """
    コメントの作成
    """
    query = """
    INSERT INTO school_comment(
        school_id,
        star,
        title,
        comment,
        post_person,
        create_at,
        update_at
    )
    VALUES(
        :schoolId,
        :star,
        :title,
        :comment,
        :postPerson,
        :currentTime,
        :currentTime
    )
    """
    args = condition.to_args()
    args["currentTime"] = query_base.current_time()
    query_base.execute_commit(query, args)

def update_school(condition:interface.SchoolQueryRecord):
    """
    学校の編集
    """
    query = """
    UPDATE school
    SET
        school_name = :schoolName,
        principal = :principal,
        detail = :detail,
        slogan = :slogan,
        update_at = :currentTime
    where
        id = :id
    """
    args = condition.to_args()
    args["currentTime"] = query_base.current_time()
    query_base.execute_commit(query, args)

def update_comment(condition:interface.SchoolCommentQueryRecord):
    """
    コメントの編集
    """
    query = """
    UPDATE school_comment
    SET
        school_id = :schoolId,
        star = :star,
        title = :title,
        comment = :comment,
        post_person = :postPerson,
        update_at = :currentTime
    where 
        id = :id
    """
    args = condition.to_args()
    args["currentTime"] = query_base.current_time()
    query_base.execute_commit(query, args)

def delete_school(id:int):
    """
    学校の削除。コメントも消える。
    """
    args = {"id" : id}

    # 学校
    query = "DELETE FROM school where id = :id"
    query_base.execute_commit(query, args)

    # コメント
    query = "DELETE FROM school_comment where school_id = :id"
    query_base.execute_commit(query, args)

def delete_comment(id:int):
    """
    コメントの削除
    """
    query = "DELETE FROM school_comment where id = :id"
    args = {"id" : id}
    query_base.execute_commit(query, args)
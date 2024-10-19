"""
学校の一覧と学校のコメント
"""

from src.route.service.module.utils import const, interface

query_model = const.PsqlBase()

def get_school():
    """
    学校の一覧を取得
    """
    query = """
    SELECT
        sc.id as id,
        sc.school_name as "schoolName",
        sc.principal as principal,
        sc.detail as detail,
        sc.slogan as slogan,
        (
            SELECT 
                round(avg(cm.star),1) 
            FROM sharemoti.school_comment as cm 
            WHERE cm.school_id = sc.id and cm.star > 0
        ) as avgStar,
        TO_CHAR(create_at, 'YYYY-MM-DD') as "createAt",
        TO_CHAR(update_at, 'YYYY-MM-DD') as "updateAt"
    from sharemoti.school as sc
    order by sc.school_name
    """
    return query_model.execute_df(query)
    
def get_comment(id:int):
    """
    学校のコメントの一覧を取得
    """
    query = """
    SELECT
        id,
        school_id as schoolId,
        star as star,
        title as title,
        comment as comment,
        post_person as postPerson,
        TO_CHAR(create_at, 'YYYY-MM-DD') as "createAt",
        TO_CHAR(update_at, 'YYYY-MM-DD') as "updateAt"
    from sharemoti.school_comment
    where school_id = %(schoolId)s
    order by id desc
    """
    args = {"schoolId":id}
    return query_model.execute_df(query, args)
    
def create_school(condition:interface.SchoolQueryRecord):
    """
    学校の作成
    """
    query = """
    INSERT INTO sharemoti.school(
        school_name, 
        principal, 
        detail, 
        slogan, 
        create_at, 
        update_at
    )
    VALUES(
        %(schoolName)s,
        %(principal)s,
        %(detail)s,
        %(slogan)s,
        %(currentTime)s,
        %(currentTime)s
    )
    """
    args = condition.to_args()
    args["currentTime"] = query_model.current_time()
    query_model.execute_commit(query, args)

def create_scrool_custom(condition:interface.SchoolQueryRecord, create_at, update_at):
    query_model = const.PsqlBase()
    query = """
    INSERT INTO sharemoti.school(
        school_name, 
        principal, 
        detail, 
        slogan, 
        create_at, 
        update_at
    )
    VALUES(
        %(schoolName)s,
        %(principal)s,
        %(detail)s,
        %(slogan)s,
        %(create_at)s,
        %(update_at)s
    )
    """
    args = condition.to_args()
    args["create_at"] = create_at
    args["update_at"] = update_at
    query_model.execute_commit(query, args)

def create_comment(condition:interface.SchoolCommentQueryRecord):
    """
    コメントの作成
    """
    query = """
    INSERT INTO sharemoti.school_comment(
        school_id,
        star,
        title,
        comment,
        post_person,
        create_at,
        update_at
    )
    VALUES(
        %(schoolId)s,
        %(star)s,
        %(title)s,
        %(comment)s,
        %(postPerson)s,
        %(currentTime)s,
        %(currentTime)s
    )
    """
    args = condition.to_args()
    args["currentTime"] = query_model.current_time()
    query_model.execute_commit(query, args)

def create_comment_custom(condition:interface.SchoolCommentQueryRecord, create_at, update_at):
    """
    コメントの作成
    """
    query_model = const.PsqlBase()
    query = """
    INSERT INTO sharemoti.school_comment(
        school_id,
        star,
        title,
        comment,
        post_person,
        create_at,
        update_at
    )
    VALUES(
        %(schoolId)s,
        %(star)s,
        %(title)s,
        %(comment)s,
        %(postPerson)s,
        %(create_at)s,
        %(update_at)s
    )
    """
    args = condition.to_args()
    args["create_at"] = create_at
    args["update_at"] = update_at
    query_model.execute_commit(query, args)

def update_school(condition:interface.SchoolQueryRecord):
    """
    学校の編集
    """
    query = """
    UPDATE sharemoti.school
    SET
        school_name = %(schoolName)s,
        principal = %(principal)s,
        detail = %(detail)s,
        slogan = %(slogan)s,
        update_at = %(currentTime)s
    where
        id = %(id)s
    """
    args = condition.to_args()
    args["currentTime"] = query_model.current_time()
    query_model.execute_commit(query, args)

def update_comment(condition:interface.SchoolCommentQueryRecord):
    """
    コメントの編集
    """
    query = """
    UPDATE sharemoti.school_comment
    SET
        school_id = %(schoolId)s,
        star = %(star)s,
        title = %(title)s,
        comment = %(comment)s,
        post_person = %(postPerson)s,
        update_at = %(currentTime)s
    where 
        id = %(id)s
    """
    args = condition.to_args()
    args["currentTime"] = query_model.current_time()
    query_model.execute_commit(query, args)

def delete_school(id:int):
    """
    学校の削除。コメントも消える。
    """
    args = {"id" : id}

    # 学校
    query = "DELETE FROM sharemoti.school where id = %(id)s"
    query_model.execute_commit(query, args)

    # コメント
    query = "DELETE FROM sharemoti.school_comment where school_id = %(id)s"
    query_model.execute_commit(query, args)

def delete_comment(id:int):
    """
    コメントの削除
    """
    query = "DELETE FROM sharemoti.school_comment where id = %(id)s"
    args = {"id" : id}
    query_model.execute_commit(query, args)
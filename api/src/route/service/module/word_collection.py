"""
検索機能
・キーワード
・日付順フラグ
・記念日数値
"""

from src.route.service.module.utils import const, interface

query_model = const.PsqlBase()


def search_word(condition: interface.SearchWordCellectionCondition):
    query = """
    SELECT
        wd.id,
        wd.word,
        wd.detail,
        TO_CHAR(create_at, 'YYYY-MM-DD') as "createAt",
        TO_CHAR(update_at, 'YYYY-MM-DD') as "updateAt"
    FROM
        sharemoti.word AS wd
    where 1 = 1 
    """

    if condition.keyword != "":
        query += """
        -- キーワード条件
        and wd.id in (
            SELECT
                s.id
            from 
                sharemoti.word as s
            WHERE
                s.word like %(keyword)s
                or s.detail like %(keyword)s
        ) 
        """

    if condition.kinen > 0:
        query += """
        -- 登録番号の範囲指定
        and wd.id IN (
            SELECT
                s2.id
            FROM
                sharemoti.word AS s2
            order by s2.id
            offset %(kinenBefore)s limit 500
        )
        """

    query += "  order by "
    if condition.date_order != "" and condition.text_order != "":
        query += " wd.update_at desc "
    if condition.date_order == "" and condition.text_order == "":
        query += " wd.update_at desc "

    if condition.date_order == "desc" and condition.text_order == "":
        query += " wd.create_at desc, wd.word asc "
    if condition.date_order == "asc" and condition.text_order == "":
        query += " wd.create_at asc, wd.word asc "

    if condition.date_order == "" and condition.text_order == "desc":
        query += " wd.word desc "
    if condition.date_order == "" and condition.text_order == "asc":
        query += " wd.word asc "

    print(query)
    return query_model.execute_df(query, condition.to_args())


def get_kinen_count():
    query = """
    SELECT
        count(*) as total
    from sharemoti.word
    """
    df = query_model.execute_df(query)
    total = int(df.iloc[0, 0])
    count = total // 500

    # 600 -> 1 -> 500
    # 1200 -> 2 -> 500, 1000
    return [(c + 1) * 500 for c in range(count)]

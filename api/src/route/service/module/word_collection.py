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
        rank() OVER (ORDER BY wd.id asc) as "wordRank",
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
            select
                s3.id
            from (
                SELECT
                    s2.id,
                    rank() OVER (ORDER BY id asc) as "rn"
                FROM
                    sharemoti.word AS s2
            ) as s3
            where
                s3."rn" >= %(kinenBefore)s and %(kinenAfter)s >= s3."rn"
            
        )
        """

    if condition.year > 0:
        query += """
        -- 更新日の年指定
        and EXTRACT(year from wd.create_at) = %(year)s 
        """

    query += "  order by "
    if condition.date_order != "" and condition.text_order != "":
        query += " wd.update_at desc "
    if condition.date_order == "" and condition.text_order == "":
        query += " wd.update_at desc "

    if condition.date_order == "desc" and condition.text_order == "":
        query += " wd.id desc, wd.word asc "
    if condition.date_order == "asc" and condition.text_order == "":
        query += " wd.id asc, wd.word asc "

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


def get_word_years():
    query = """
    SELECT
        distinct(EXTRACT(year from create_at)) as "year"
    from sharemoti.word
    order by "year" desc
    """
    df = query_model.execute_df(query)
    return df["year"].tolist()

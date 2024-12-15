from src.route.service.module.utils import const
query_model = const.PsqlBase()

def category_rank(text:str):
    """
    ウルトラCや思い出などのキャラ別の件数
    """
    query = """
    WITH t AS (
        SELECT
            n.ssbu_name,
            COUNT(CASE WHEN s.title LIKE %(text)s THEN 1 END) AS total
        FROM sharemoti.name AS n
        LEFT JOIN sharemoti.ssbu_clip AS s ON s.char_name = n.name
        where n.ssbu_name <> 'その他' and ssbu_name <> 'Mrゲーム＆ウォッチ' and ssbu_name <> 'クッパ Jr'
        GROUP BY n.ssbu_name
    )
    SELECT 
    ssbu_name as name,
        total,
        RANK() OVER (ORDER BY total DESC) AS rank
    FROM t
    ORDER BY total DESC, ssbu_name asc
    """
    args = {
        "text" : f'%{text}%'
    }
    return query_model.execute_df(query, args)

def category_first(text:str):
    query = """
    WITH A AS (
        SELECT
            n.ssbu_name AS name,
            MIN(CASE WHEN LENGTH(s.date) = 8 AND s.title LIKE %(text)s THEN s.date END) AS date_text
        FROM
            sharemoti.name AS n
        LEFT JOIN sharemoti.ssbu_clip AS s ON s.char_name = n.name
        where n.ssbu_name <> 'その他' and ssbu_name <> 'Mrゲーム＆ウォッチ' and ssbu_name <> 'クッパ Jr'
        GROUP BY
            n.ssbu_name
    )
    SELECT
        name,
        COALESCE(
            TO_CHAR(TO_DATE(date_text, 'YYYYMMDD'), 'YYYY"年"MM"月"DD"日'),
            null
        ) AS date
    FROM
        A
    order by date desc nulls last;
    """
    args = {
        "text" : f'%{text}%'
    }
    return query_model.execute_df(query, args)

def stamp_list(text:str):
    query = """
    WITH
	A1 AS (
		SELECT
			n.ssbu_name,
			COUNT(
				CASE
					WHEN s.title LIKE %(text)s THEN 1
				END
			) AS total
		FROM
			sharemoti.name AS n
			LEFT JOIN sharemoti.ssbu_clip AS s ON s.char_name = n.name
		WHERE
			n.ssbu_name <> 'その他'
			AND n.ssbu_name <> 'Mrゲーム＆ウォッチ'
			AND n.ssbu_name <> 'クッパ Jr'
		GROUP BY
			n.ssbu_name
	),
	A2 AS (
		SELECT
			ssbu_name AS name,
			CASE
				WHEN t.total > 0 THEN 1
				ELSE 0
			END AS comp,
			sn.id
		FROM
			A1 AS t
		left JOIN sharemoti.ssbu_names as sn on t.ssbu_name = sn."name"
	)
	SELECT 
		name,
		comp
	from A2 order by A2.id
    """
    args = {
        "text" : f'%{text}%'
    }
    return query_model.execute_df(query, args)
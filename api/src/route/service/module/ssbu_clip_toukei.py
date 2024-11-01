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
        where n.ssbu_name <> 'その他'
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
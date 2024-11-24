from src.route.service.module.utils import const, interface
import math

# テーブル操作
p = const.Path()
query_model = const.PsqlBase()

def get_news(page_no:int, page_size = 5):
    query = """
        -- 各テーブルで直近で追加したデータを日別5件取得
        WITH p1 AS (
            SELECT
                1 AS page_id,
                '名言集' AS page,
                '/wordList' as url,
                TO_CHAR(create_at,
                    'YYYY-MM-DD') AS "createdAt",
                count(TO_CHAR(create_at,
                        'YYYY-MM-DD')) AS total
            FROM
                sharemoti.word
            GROUP BY
                TO_CHAR(create_at,
                    'YYYY-MM-DD')
            ORDER BY
                TO_CHAR(create_at,
                    'YYYY-MM-DD')
                DESC
            LIMIT 5
        ),
        p2 AS (
            SELECT
                2 AS page_id,
                'あだ名' AS page,
                '/nameList' as url,
                TO_CHAR(create_at,
                    'YYYY-MM-DD') AS "createdAt",
                count(TO_CHAR(create_at,
                        'YYYY-MM-DD')) AS total
            FROM
                sharemoti.name
            WHERE
                create_at IS NOT NULL
            GROUP BY
                TO_CHAR(create_at,
                    'YYYY-MM-DD')
            ORDER BY
                TO_CHAR(create_at,
                    'YYYY-MM-DD')
                DESC
            LIMIT 5
        ),
        p3 AS (
            SELECT
                3 AS page_id,
                '焼き直し条約' AS page,
                '/yaki' as url,
                TO_CHAR(create_at,
                    'YYYY-MM-DD') AS "createdAt",
                count(TO_CHAR(create_at,
                        'YYYY-MM-DD')) AS total
            FROM
                sharemoti.yaki
            WHERE
                create_at IS NOT NULL
            GROUP BY
                TO_CHAR(create_at,
                    'YYYY-MM-DD')
            ORDER BY
                TO_CHAR(create_at,
                    'YYYY-MM-DD')
                DESC
            LIMIT 5
        ),
        p4 AS (
            SELECT
                4 AS page_id,
                '俳句' AS page,
                '/haiku' as url,
                TO_CHAR(create_at,
                    'YYYY-MM-DD') AS "createdAt",
                count(TO_CHAR(create_at,
                        'YYYY-MM-DD')) AS total
            FROM
                sharemoti.haiku
            WHERE
                create_at IS NOT NULL
            GROUP BY
                TO_CHAR(create_at,
                    'YYYY-MM-DD')
            ORDER BY
                TO_CHAR(create_at,
                    'YYYY-MM-DD')
                DESC
            LIMIT 5
        ),
        p5 AS (
            SELECT
                5 AS page_id,
                '学校' AS page,
                '/school' as url,
                TO_CHAR(create_at,
                    'YYYY-MM-DD') AS "createdAt",
                count(TO_CHAR(create_at,
                        'YYYY-MM-DD')) AS total
            FROM
                sharemoti.school
            WHERE
                create_at IS NOT NULL
            GROUP BY
                TO_CHAR(create_at,
                    'YYYY-MM-DD')
            ORDER BY
                TO_CHAR(create_at,
                    'YYYY-MM-DD')
                DESC
            LIMIT 5
        ),
        p6 AS (
            SELECT
                6 AS page_id,
                '学校コメント' AS page,
                '/school' as url,
                TO_CHAR(create_at,
                    'YYYY-MM-DD') AS "createdAt",
                count(TO_CHAR(create_at,
                        'YYYY-MM-DD')) AS total
            FROM
                sharemoti.school_comment
            WHERE
                create_at IS NOT NULL
            GROUP BY
                TO_CHAR(create_at,
                    'YYYY-MM-DD')
            ORDER BY
                TO_CHAR(create_at,
                    'YYYY-MM-DD')
                DESC
            LIMIT 5
        ),
        p7 AS (
            SELECT
                7 AS page_id,
                'スマブラの切り抜き' AS page,
                '/ssbu_clip' as url,
                TO_CHAR(date(sp.create_at),'YYYY-MM-DD') AS "createdAt",
                count(date(sp.create_at)) AS total
            FROM
                sharemoti.ssbu_clip AS sp
            WHERE
                date(sp.create_at) IS NOT NULL
            GROUP BY
                date(sp.create_at)
            ORDER BY
                date(sp.create_at)
                DESC
            LIMIT 5
        ),
        p8 AS (
            SELECT
                8 AS page_id,
                '画像' AS page,
                '/img' as url,
                TO_CHAR(date(img.create_at),'YYYY-MM-DD') AS "createdAt",
                count(date(img.create_at)) AS total
            FROM
                sharemoti.image AS img
            WHERE
                date(img.create_at) IS NOT NULL
            GROUP BY
                date(img.create_at)
            ORDER BY
                date(img.create_at)
                DESC
            LIMIT 5
        ),
        -- 各windowクエリをunion
        subtotal AS (
            SELECT
                *
            FROM
                p1
            UNION
            SELECT
                *
            FROM
                p2
            UNION
            SELECT
                *
            FROM
                p3
            UNION
            SELECT
                *
            FROM
                p4
            UNION
            SELECT
                *
            FROM
                p5
            UNION
            SELECT
                *
            FROM
                p6
            UNION
            SELECT
                *
            FROM
                p7
            UNION
            SELECT
                *
            FROM
                p8
        )
        -- 追加日順、ページID順でクエリ
        SELECT
            *
        FROM
            subtotal
        ORDER BY
            "createdAt" DESC,
            page_id
    """
    query_data = query + " limit %(pageSize)s offset %(offset)s"
    args = {
        'pageSize' : page_size,
        'offset' : (max(page_no - 1,0))*page_size
    }
    df = query_model.execute_df(query_data, args)
    
    count_df = query_model.execute_df(query)
    total_count = len(count_df)
    page_count = int(math.ceil(total_count / page_size))
    return df,page_count
import requests
import datetime
import time
import re


from bs4 import BeautifulSoup
from tqdm import tqdm


from src.route.service.module.utils import const, interface


p = const.Path()
dbname = p.db_holotwitter()
query_base = const.DbBase(dbname)

def extract_username(url: str) -> str:
    """
    URLからTwitterのユーザー名を抽出する関数
    """
    match = re.search(r'twitter\.com/(\w+)', url)
    if match:
        return match.group(1)
    else:
        raise ValueError("URLからユーザー名を抽出できませんでした")


def get_links(id:str):
    acount_url = "https://seesaawiki.jp/hololivetv/d/%B8%F8%BC%B0%A5%A2%A5%AB%A5%A6%A5%F3%A5%C8#footnote1"
    res = requests.get(acount_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    table = soup.find(id=id)# 'content_block_7'
    links = []
    for a in table.find_all('a'):
        if a.get('href') is not None:
            if 'twitter' in a.get('href'):
                links.append(extract_username(a.get('href')))
    return links

def get_twitter_acount():
    """
    メインのTwitterアカウントを取得
    """
    return get_links('content_block_7')

def get_twitter_sub_acount():
    """
    サブのTwitterアカウントを取得ß
    """
    return get_links('content_block_10')

def parse_date(epoch_seconds:int):
    """
    エポック時間を文字列の日時に変換
    """
    dt = datetime.datetime.fromtimestamp(epoch_seconds, datetime.timezone.utc)
    formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date

def get_pagination_url(user_id:str , last_tweet_id=''):
    """
    ハッシュタグと最後のツイートIDを元にツイートを取得
    """
    base = 'https://search.yahoo.co.jp/realtime/api/v1/pagination?crumb=VD7gZgAAAABgY-7orF8v420hrcO1TjRjHR0Oat89SJCMNmF0cUV2Q14zvdkubx9pMBgDHCGiK9EWGOxEyLnJb2IVpXmNB157&p=id%3A'
    url = f'{base}{user_id}&rkf=3&b=1'
    if last_tweet_id:
        return url + f'&oldestTweetId={last_tweet_id}&start='
    else:
        return url

def format_data(item:dict):
    if 'mentions' in item and len(item['mentions']) > 0:
        return None
        
    # ツイート
    tweet = interface.HolotwitterTweet(
        item['id'],
        item.get('displayTextFragments', ''),
        parse_date(item['createdAt']),
        item.get('rtCount', 0),
        item.get('likesCount', 0),
        item.get('screenName', '')
    )

    # ユーザー
    user = None
    if 'name' in item:
        user = interface.HolotwitterUser(
            item.get('name', ''),
            item.get('screenName', ''),
            item.get('profileImage', '')
        )

    # メディア
    medias = []
    if 'media' in item:
        for m in item['media']:
            medias.append(
                interface.HolotwitterMedia(
                    item['id'],
                    m.get('type', ''),
                    m['item'].get('url', ''),
                    m['item'].get('mediaUrl', ''),
                    m.get('metaImageUrl', '')
                )
            )

    # URL
    urls = []
    if 'urls' in item:
        for u in item['urls']:
            urls.append(
                interface.HolotwitterUrl(
                    item['id'],
                    u.get('expandedUrl', '')
                )
            )
    return tweet, user, medias, urls

def get_list(url:str):
    """
    URLを元にツイートのリストを取得
    """
    time.sleep(0.5)
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"response status_code -> {response.status_code} {response}")
    tweet_list = []
    media_list = []
    url_list = []
    user = None
    for tweet in response.json().get('timeline', {}).get('entry', []):
        tweet_items = format_data(tweet)
        if tweet_items:
            tw, us, medias, urls = tweet_items
            tweet_list.append(tw)
            media_list.extend(medias)
            url_list.extend(urls)
            if us:
                user = us

    if len(response.json().get('timeline', {}).get('entry', [])) == 0:
        last_tweet_id = ''
    else:
        last_tweet_id = response.json().get('timeline', {}).get('entry', [])[-1]['id']

    return tweet_list, user, media_list, url_list, last_tweet_id

def get_tweet(user_id:str):
    """
    ツイートを取得する
    """
    tweets = []
    medias = []
    user = None
    urls = []
    first_url = get_pagination_url(user_id)
    tweet_list, us, media_list, url_list, last_tweet_id = get_list(first_url)

    if us:
        user = us
    
    tweets.extend(tweet_list)
    medias.extend(media_list)
    urls.extend(url_list)
    while True:
        url = get_pagination_url(user_id, last_tweet_id)
        tweet_list, us, media_list, url_list, last_tweet_id = get_list(url)
        if user is None:
            user = us
        tweets.extend(tweet_list)
        medias.extend(media_list)
        urls.extend(url_list)
        if last_tweet_id == '':
            break
        if len(tweet_list) > 0:
            print(f"\r{tweet_list[-1].created_at}", end="")
    return tweets, user, medias, urls



def make_table():    
    tweet_query = """
    CREATE TABLE IF NOT EXISTS tweet (
        id INTEGER PRIMARY KEY,
        text TEXT,
        created_at TEXT,
        rt_count INTEGER,
        likes_count INTEGER,
        user_screen_name TEXT
    );
    """

    user_query = """
    CREATE TABLE IF NOT EXISTS user (
        name TEXT,
        screen_name TEXT PRIMARY KEY,
        profile_image TEXT
    );
    """

    media_query = """
    CREATE TABLE IF NOT EXISTS media (
        tweet_id INTEGER,
        type TEXT,
        url TEXT,
        media_url TEXT,
        meta_image_url TEXT,
        FOREIGN KEY (tweet_id) REFERENCES tweet (id),
        PRIMARY KEY (tweet_id, media_url)
    );
    """

    url_query = """
    CREATE TABLE IF NOT EXISTS url (
        tweet_id INTEGER,
        expanded_url TEXT,
        FOREIGN KEY (tweet_id) REFERENCES tweet (id),
        PRIMARY KEY (tweet_id, expanded_url)
    );
    """
    for query in [tweet_query, user_query, media_query, url_query]:
        query_base.execute_commit(query)



def save_tweet(condition:interface.HolotwitterTweet):
    # 要素の存在チェック
    check_df = query_base.execute_df(
        'SELECT * from tweet where id = :id',
        {
            'id' : condition.id
        }
    )

    if len(check_df) == 0:
        # insert
        query = """
        INSERT INTO tweet(
            id,
            text,
            created_at,
            rt_count,
            likes_count,
            user_screen_name
        )
        VALUES(
            :id,
            :text,
            :createdAt,
            :rtCount,
            :likesCount,
            :userScreenName
        )
        """
    else:
        # update
        query = """
        UPDATE tweet
        SET
            text = :text,
            rt_count = :rtCount,
            likes_count = :likesCount
        where
            id = :id
        """
    args = condition.to_args()
    query_base.execute_commit(query, args)



def save_user(condition:interface.HolotwitterUser):
    # 要素の存在チェック
    check_df = query_base.execute_df(
        'SELECT * from user where screen_name = :screenName',
        {
            'screenName' : condition.screen_name
        }
    )

    if len(check_df) == 0:
        query = """
        INSERT INTO user(
            name,
            screen_name,
            profile_image
        )
        VALUES(
            :name,
            :screenName,
            :profileImage
        )
        """
    else:
        query = """
        UPDATE user
        SET
            name = :name,
            profile_image = :profileImage
        WHERE
            screen_name = :screenName
        """
    args = condition.to_args()
    query_base.execute_commit(query, args)

def save_media(condition:interface.HolotwitterMedia):
    query = """
    INSERT INTO media(
        tweet_id,
        type,
        url,
        media_url,
        meta_image_url
    )
    SELECT * FROM(
        VALUES(
            :tweetId,
            :type,
            :url,
            :mediaUrl,
            :metaImageUrl
        )
    ) as add_item
    WHERE NOT EXISTS (
        SELECT * FROM media
        WHERE
            tweet_id = :tweetId and
            media_url = :mediaUrl
    )
    
    """
    args = condition.to_args()
    query_base.execute_commit(query, args)
    

def save_url(condition:interface.HolotwitterUrl):
    query = """
    INSERT INTO url(
        tweet_id,
        expanded_url
    )
    SELECT * FROM(
        VALUES(
            :tweetId,
            :expandedUrl
        )
    ) as add_item
    WHERE NOT EXISTS (
        SELECT * FROM url
        WHERE
            tweet_id = :tweetId and
            expanded_url = :expandedUrl
    )
    
    """
    args = condition.to_args()
    query_base.execute_commit(query, args)


def scraping():
    # テーブル作成
    make_table()
    
    # アカウント情報の取得
    twitter_acount = get_twitter_acount()
    twitter_sub_acount = get_twitter_sub_acount()
    twitter_acount.extend(twitter_sub_acount)
    
    # アカウント別にツイートを取得
    for user_id in tqdm(twitter_acount):
        tweets, user, medias, urls = get_tweet(user_id)
    
        # レコード追加
        [save_tweet(t) for t in tweets]
        [save_media(m) for m in medias]
        [save_url(u) for u in urls]
        if user:
            save_user(user)
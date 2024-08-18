import os
import sys
api_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
print(api_path)
sys.path.append(api_path)

from src.route.service.module import twitter_sqlite
from src.route.service import twitter_service
from src.route.service.module.utils import const
from tqdm import tqdm
from src.route.service.module.utils import const

@const.line_handler
def main():
    DATE_RANGE = 14

    """
    BASE
    """
    opt = const.Option()
    base_hashtags = opt.twitter_base_hashtags()
    for hashtag in tqdm(base_hashtags,desc='base'):
        df = twitter_service.get_tweet(hashtag,DATE_RANGE)
        twitter_sqlite.update(df,hashtag,'base')

    """
    HOLO
    """
    holo_hashtags = [item.hashtag for item in opt.twitter_holo_hashtags()]
    for hashtag in tqdm(holo_hashtags,desc='holo'):
        df = twitter_service.get_tweet(hashtag,DATE_RANGE)
        twitter_sqlite.update(df,hashtag,'holo')
main()
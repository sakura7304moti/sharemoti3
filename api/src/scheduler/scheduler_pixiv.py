import os
import sys
api_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
print(api_path)
sys.path.append(api_path)

from src.route.service.module import pixiv_scraper
from src.route.service.module.utils import const

@const.line_handler
def main():
    pixiv_scraper.holo_pixiv_update()

main()
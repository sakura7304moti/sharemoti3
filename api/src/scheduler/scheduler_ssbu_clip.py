import os
import sys
api_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
print(api_path)
sys.path.append(api_path)

from src.route.service.module import ssbu_clip
from src.route.service.module.utils import const

@const.line_handler
def main():
    ssbu_clip.save_clips()

main()
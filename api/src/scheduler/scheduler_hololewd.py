import os
import sys
api_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
print(api_path)
sys.path.append(api_path)

from src.route.service import hololewd_service
from src.route.service.module.utils import const

@const.line_handler
def main():
    hololewd_service.update_db()

main()
from src.route.service.module import ssbu_clip_toukei as query_service

def category_rank(text:str):
    return query_service.category_rank(text)
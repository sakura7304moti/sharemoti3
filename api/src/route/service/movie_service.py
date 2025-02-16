import pandas as pd
from src.route.service.module import movie, movie_hashtag, movie_staff, movie_thumbnail
from src.route.service.module.utils import interface


# アップロードに使う関数
def create_movie(condition: interface.Movie) -> int:
    movie.create(condition)
    return movie.get_id(condition.file_name)


def create_hashtag(movie_id: int, name: str):
    movie_hashtag.create(movie_id, name)


def create_thumbnail(path: str):
    movie_thumbnail.create_thumbnail(path)


def update_thumbnail_all():
    movie_thumbnail.update_thumbnail_all()


# 編集に使う関数
def update_movie(condition: interface.Movie):
    movie.update(condition)


def update_staff(staff_cd: int, name: str):
    movie_staff.update(staff_cd, name)


def update_group(name: str, is_group: bool):
    movie_hashtag.update_group(name, is_group)


def change_hashtagname(before_name: str, after_name: str):
    movie_hashtag.change_tagname(before_name, after_name)


# 削除に使う関数
def delete_movie(movie_id: int):
    movie.delete(movie_id)
    movie_hashtag.delete_movie(movie_id)


def delete_hashtag(movie_id: int):
    movie_hashtag.delete_movie(movie_id)


def get_movie_id(file_name: str):
    return movie.get_id(file_name)


def delete_hashtag_by_name(name: str):
    movie_hashtag.delete_hashtag_by_name(name)


# 検索に使う関数
def hashtag_list():
    return movie_hashtag.hashtag_list()


def search_movie(keyword: str, hashtag: str, page_no: int, page_size: int):
    df = movie.search(keyword, hashtag, page_no, page_size)
    total_count = movie.search_total_count(keyword, hashtag, page_size)
    id_list = df["id"].to_list()
    hashtag_df = movie.get_movie_hashtags(id_list)
    return df, total_count, hashtag_df


def get_thumbnail_path(file_name: str):
    return movie_thumbnail.get_thumbnail_path(file_name)


def get_movie(id: int):
    df = movie.get_movie(id)
    hashtag_df = movie.get_movie_hashtags([id])
    return df, hashtag_df

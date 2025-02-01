from src.route.service.module import movie, movie_hashtag, movie_staff
from src.route.service.module.utils import interface


# アップロードに使う関数
def create_movie(condition: interface.Movie) -> int:
    movie.create(condition)
    return movie.get_id(condition.file_name)


def create_hashtag(movie_id: int, name: str):
    movie_hashtag.create(movie_id, name)


# 編集に使う関数
def update_movie(condition: interface.Movie):
    movie.update(condition)


def update_staff(staff_cd: int, name: str):
    movie_staff.update(staff_cd, name)


# 削除に使う関数
def delete_movie(movie_id: int):
    movie.delete(movie_id)
    movie_hashtag.delete_movie(movie_id)


def delete_hashtag(movie_id: int):
    movie_hashtag.delete_movie(movie_id)


def get_movie_id(file_name: str):
    return movie.get_id(file_name)

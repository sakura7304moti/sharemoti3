from api.src.route.service.module import schoollist

"""
学校一覧
"""

def make_db():
    schoollist.init()

def save(word:str = ""):
    return schoollist.save(word)

def delete(word:str = ""):
    return schoollist.delete(word)

def search(word:str = ""):
    return schoollist.search(word)
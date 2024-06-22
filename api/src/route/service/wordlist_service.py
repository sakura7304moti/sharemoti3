from api.src.route.service.module import wordlist
"""
名言集
"""
def create_db():
    """
    DB作成
    """
    wordlist.init()

def save(word: str = "", desc: str = ""):
    """
    存在しなければ追加
    存在するなら更新
    """
    return wordlist.save(word, desc)

def delete(word: str = "", desc:str = ""):
    """
    レコード削除
    """
    return wordlist.delete(word, desc)

def search(text:str = ""):
    """
    レコード検索
    """
    return wordlist.search(text)
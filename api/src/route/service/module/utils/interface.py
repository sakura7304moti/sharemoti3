import datetime
from typing import List

class WordList2Record:  # 名言集2
    def __init__(self, word: str, desc: str,createAt:str,updateAt:str):
        self.word = word
        self.desc = desc
        self.createAt = datetime.datetime.strptime(createAt,'%Y-%m-%d %H:%M:%S')
        self.updateAt = datetime.datetime.strptime(updateAt,'%Y-%m-%d %H:%M:%S')

    def __dict__(self):
        return {"word": self.word, "desc": self.desc,"createAt":self.createAt.strftime('%Y-%m-%d %H:%M:%S'),"updateAt":self.updateAt.strftime('%Y-%m-%d %H:%M:%S')}

class NameListRecord:  # あだ名集
    def __init__(self, key: str, val: str):
        self.key = key
        self.val = val

    def __dict__(self):
        return {"key": self.key, "val": self.val}
    

class YakiListRecord:  # 焼き直し条約
    def __init__(self, word: str, yaki: str):
        self.word = word
        self.yaki = yaki

    def __dict__(self):
        return {"word": self.word, "yaki": self.yaki}
    
class SchoolListRecord:  # 学校一覧
    def __init__(self, word: str):
        self.word = word

    def __dict__(self):
        return {"word": self.word}
    
class MannerListRecord:  # 日本国失礼憲法
    def __init__(self, word: str):
        self.word = word

    def __dict__(self):
        return {"word": self.word}
    
class HaikuListRecord:#俳句一覧
    def __init__(self,id:int,first:str,second:str,third:str,poster:str,detail:str,createAt:str,updateAt:str):
        self.id = id
        self.first = first
        self.second = second
        self.third = third
        self.detail = detail
        self.poster = poster
        self.createAt = datetime.datetime.strptime(createAt,'%Y-%m-%d %H:%M:%S')
        self.updateAt = datetime.datetime.strptime(updateAt,'%Y-%m-%d %H:%M:%S')

    def __dict__(self):
        return {"id":self.id,"first":self.first,"second":self.second,"third":self.third,"poster":self.poster,"detail":self.detail,"createAt":self.createAt.strftime('%Y-%m-%d %H:%M:%S'),"updateAt":self.updateAt.strftime('%Y-%m-%d %H:%M:%S')}

class HaikuListStatusResult:#俳句一覧の追加結果
    def __init__(self,success:bool,errorText:str):
        self.success = success
        self.errorText = errorText
    
    def __dict__(self):
        return {"success":self.success,"errorText":self.errorText}
    
class ImageListRecord:#画像一覧
    def __init__(self,
                 id:int,
                 file_name:str,
                 ext:str,
                 title:str,
                 detail:str,
                 create_at:str,
                 update_at:str):
        self.id = id
        self.file_name = file_name
        self.ext = ext
        self.title = title
        self.detail = detail
        self.create_at = datetime.datetime.strptime(create_at,'%Y-%m-%d %H:%M:%S')
        self.update_at = datetime.datetime.strptime(update_at,'%Y-%m-%d %H:%M:%S')
        
    def __dict__(self):
        return {"id":self.id,"fileName":self.file_name,"ext":self.ext, "title":self.title,"detail":self.detail,"createAt":self.create_at.strftime('%Y-%m-%d %H:%M:%S'),"updateAt":self.update_at.strftime('%Y-%m-%d %H:%M:%S')}
    def __str__(self):
        return f"ImageListRecord(id={self.id}, file_name={self.file_name},ext={self.ext}, title={self.title}, " \
               f"detail={self.detail}, create_at={self.create_at}, update_at={self.update_at})"

    
class ImageListStatusResult:#画像の追加結果
    def __init__(self,success:bool,errorText:str):
        self.success = success
        self.errorText = errorText
    
    def __dict__(self):
        return {"success":self.success,"errorText":self.errorText}
    
class SsbuNameRecord:#スマブラのキャラ名と画像URL
    def __init__(self,name:str,url:str,icon:str):
        self.name = name
        self.url = url
        self.icon = icon
    def __dict__(self):
        return {"name":self.name,"url":self.url,"icon":self.icon}

class KinshiListRecord:  # 禁止キャラ一覧
    def __init__(self,id:int, char_name: str, ssbu_name: str,  desc: str,createAt:str,updateAt:str):
        self.id = id
        self.char_name = char_name
        self.ssbu_name = ssbu_name
        self.desc = desc
        self.createAt = datetime.datetime.strptime(createAt,'%Y-%m-%d %H:%M:%S')
        self.updateAt = datetime.datetime.strptime(updateAt,'%Y-%m-%d %H:%M:%S')

    def __dict__(self):
        return {"id":self.id, "charName": self.char_name, "ssbuName":self.ssbu_name, "desc": self.desc,"createAt":self.createAt.strftime('%Y-%m-%d %H:%M:%S'),"updateAt":self.updateAt.strftime('%Y-%m-%d %H:%M:%S')}

class NameList2Record:  #あだ名一覧2
    def __init__(
        self,
        id:int,
        name:str,
        ssbu_name:str,
        create_at:str,
        update_at:str
                ):
        self.id = id
        self.name = name
        self.ssbu_name = ssbu_name
        self.create_at = create_at
        self.update_at = update_at

    def __str__(self):
        return f"NameList2Record(id={self.id}, name='{self.name}', ssbu_name='{self.ssbu_name}', create_at='{self.create_at}', update_at='{self.update_at}')"
        
    def __dict__(self):
        return {
            'id': self.id,
            'name': self.name,
            'ssbuName': self.ssbu_name,
            'createAt': self.create_at,
            'updateAt': self.update_at
        }

class YakiList2Record:  #焼き直し条約2
    def __init__(
        self,
        id:int,
        word:str,
        yaki:str,
        create_at:str,
        update_at:str
                ):
        self.id = id
        self.word = word
        self.yaki = yaki
        self.create_at = create_at
        self.update_at = update_at

    def __dict__(self):
        return {
            'id': self.id,
            'word': self.word,
            'yaki': self.yaki,
            'createAt': self.create_at,
            'updateAt': self.update_at
        }


class DbResult:#追加・更新の結果
    def __init__(self,success:bool,errorText:str):
        self.success = success
        self.errorText = errorText
    
    def __dict__(self):
        return {"success":self.success,"errorText":self.errorText}
    
class KaraokeListRecord:#カラオケ音声の一覧
    def __init__(self,
                 id:int,
                 file_name:str,
                 date:str):
        self.id = id
        self.file_name = file_name
        self.date = date
        
    def __dict__(self):
        return {"id":self.id,"fileName":self.file_name,"date":self.date}
    def __str__(self):
        return f"ID: {self.id}, File Name: {self.file_name}, Date: {self.date}"

class VoiceListRecord:#ボイス
    def __init__(self,
                 id:int,
                 file_name:str):
        self.id = id
        self.file_name = file_name
        
    def __dict__(self):
        return {"id":self.id,"fileName":self.file_name}
    def __str__(self):
        return f"ID: {self.id}, File Name: {self.file_name}"
    
class RadioListRecord:#ラジオの一覧
    def __init__(self,
                 id:int,
                 file_name:str,
                 date:str):
        self.id = id
        self.file_name = file_name
        self.date = date
        
    def __dict__(self):
        return {"id":self.id,"fileName":self.file_name,"date":self.date}
    def __str__(self):
        return f"ID: {self.id}, File Name: {self.file_name}, Date: {self.date}"
    
class ssbuListRecord:#スマブラのクリップ
    def __init__(self,
                 id:int,
                 file_name:str,
                 date:str,
                 year:str):
        self.id = id
        self.file_name = file_name
        self.date = date
        self.year = year
        
    def __dict__(self):
        return {"id":self.id,"fileName":self.file_name,"date":self.date,"year":self.year}
    def __str__(self):
        return f"ID: {self.id}, File Name: {self.file_name}, Date: {self.date}, Year: {self.year}"
    
class SsbuNameRecord:#スマブラのキャラ名と画像URL
    def __init__(self,name:str,url:str,icon:str):
        self.name = name
        self.url = url
        self.icon = icon
    def __dict__(self):
        return {"name":self.name,"url":self.url,"icon":self.icon}

class MovieListRecord:#完成品
    def __init__(self,
                 id:int,
                 file_name:str,
                 poster:str):
        self.id = id
        self.file_name = file_name
        self.poster = poster
        
    def __dict__(self):
        return {"id":self.id,"fileName":self.file_name,"poster":self.poster}
    def __str__(self):
        return f"ID: {self.id}, File Name: {self.file_name}, Poster: {self.poster}"

class HoloName:
    def __init__(self,hashtag,url):
        self.hashtag = hashtag
        self.url = url

    def __dict__(self):
        return {"hashtag":self.hashtag,"url":self.url}

class TwitterQueryRecord:
    hashtag: str
    mode: str
    url: str
    date: datetime.date
    images: list[str]
    userId: str
    userName: str
    likeCount: int

    def __init__(
        self,
        hashtag: str,
        mode: str,
        url: str,
        date: str,
        images: str,
        userId: str,
        userName: str,
        likeCount: int,
    ):
        self.hashtag = hashtag
        self.mode = mode
        self.url = url
        self.date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        self.images = images.split(",")
        self.userId = userId
        self.userName = userName
        self.likeCount = likeCount

    def __str__(self):
        return (
            f"Hashtag: {self.hashtag}\n"
            f"Mode: {self.mode}\n"
            f"URL: {self.url}\n"
            f"Date: {self.date}\n"
            f"Images: {self.images}\n"
            f"User ID: {self.userId}\n"
            f"User Name: {self.userName}\n"
            f"Like Count: {self.likeCount}\n"
        )

    def __dict__(self):
        return {
            "hashtag": self.hashtag,
            "mode": self.mode,
            "url": self.url,
            "date": self.date.strftime("%Y-%m-%d"),
            "images": self.images,
            "userId": self.userId,
            "userName": self.userName,
            "likeCount": self.likeCount,
        }
    
# `SongQueryRecord` クラスは、日付、メンバー、リンク、曲名、その他の詳細を含む曲クエリのレコードを表します。
class SongQueryRecord:
    date:str
    member:str
    link:str
    song_name:str
    detail:str

    def __init__(
            self,
            date:str,
            member:str,
            link:str,
            song_name:str,
            detail:str,
    ):
        self.date =date
        self.member = member
        self.link = link
        self.song_name = song_name
        self.detail = detail

    def __str__(self):
        return {
            f"Date:{self.date}\n"
            f"Member:{self.member}\n"
            f"Link:{self.link}\n"
            f"SongName:{self.song_name}\n"
            f"Detail:{self.detail}\n"
        }
    
    def __dict__(self):
        return {
            "date":self.date,
            "member":self.member,
            "link":self.link,
            "songName":self.song_name,
            "detail":self.detail
        }
    
# `HoloSongAlbum` クラスは、アルバム名、アーティスト、プレイリスト リンク、日付、画像リンクなどのプロパティを持つ曲アルバムを表します。
class HoloSongAlbum:
    albumName:str
    artist:str
    playlistLink:str
    date:str
    imageLink:str
    
    def __init__(self,albumName:str,artist:str,playlistLink:str,date:str,imageLink:str):
        self.albumName = albumName
        self.artist = artist
        self.playlistLink = playlistLink
        self.date = date
        self.imageLink = imageLink
        
    def __dict__(self):
        return {
            "albumName":self.albumName,
            "artist":self.artist,
            "playlistLink":self.playlistLink,
            "date":self.date,
            "imageLink":self.imageLink
        }
    
    def __str__(self):
        return f"Album Name: {self.albumName}\nArtist: {self.artist}\nPlaylist Link: {self.playlistLink}\nDate: {self.date}\nImage Link: {self.imageLink}"
    
class HoloMemoryRecord:
    title: str
    member: str
    date: str
    link:str
    memory: str
    detail: str

    def __init__(self, title: str, member: str, date: str, link:str, memory: str, detail: str):
        self.title = title
        self.member = member
        self.link = link
        self.date = date
        self.memory = memory
        self.detail = detail

    def __dict__(self):
        return {
            "title": self.title,
            "member": self.member,
            "link":self.link,
            "date": self.date,
            "memory": self.memory,
            "detail": self.detail
        }

    def __str__(self):
        return f"{self.title} - {self.member} - {self.link} - {self.date} - {self.memory} - {self.detail}"

class ChannelInfo:
    def __init__(self,channel_id,channel_name,description,header_url,avatar_url):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.description = description
        self.header_url = header_url
        self.avatar_url = avatar_url
        
    def __str__(self):
        return f"""channel_name -> {self.channel_name}
channel_id -> {self.channel_id}
header_url -> {self.header_url}
avatar_url -> {self.avatar_url}
---- description -----
{self.description}
        """
    
    def __dict__(self):
        return {
            "channelId":self.channel_id,
            "channelName":self.channel_name,
            "description":self.description,
            "headerUrl":self.header_url,
            "avatarUrl":self.avatar_url
        }


class MovieInfo:
    def __init__(self,id,url,title,date,channel_id,view_count,thumbnail_url,movie_type):
        self.id = id
        self.url = url
        self.title = title
        self.date = date
        self.channel_id = channel_id
        self.view_count = view_count
        self.thumbnail_url = thumbnail_url
        self.movie_type = movie_type

    def __str__(self):
        return f"""if -> {self.id}
url -> {self.url}
title -> {self.title}
date -> {self.date}
channel_id -> {self.channel_id}
view_count -> {self.view_count}
thumbnail_url -> {self.thumbnail_url}
movieType -> {self.movie_type}"""
    
    def __dict__(self):
        return {
            "id":self.id,
            "url":self.url,
            "title":self.title,
            "date":self.date,
            "channelId":self.channel_id,
            "viewCount":self.view_count,
            "thumbnailUrl":self.thumbnail_url,
            "movieType":self.movie_type
        }
    
    
class Archive:
    def __init__(self,channel:ChannelInfo,movie:List[MovieInfo],live:List[MovieInfo],short:List[MovieInfo]):
        self.channel = channel
        self.movie = movie
        self.live = live
        self.short = short

    def __dict__(self):
        return {
            "channel": self.channel.__dict__(),
            "movie": [m.__dict__() for m in self.movie],
            "live": [l.__dict__() for l in self.live],
            "short": [s.__dict__() for s in self.short]
        }
    
#hololewdのテーブル
class HololewdQueryRecord:
    def __init__(
        self,
        flair_text:str,
        url:str,
        date:str,
        score:int
    ):
        self.flair_text = flair_text
        self.url = url
        self.date = date
        self.score = score

    def __str__(self):
        return (f"HololewdTable(flair_text='{self.flair_text}', "
                f"url='{self.url}', date='{self.date}', score={self.score})")

    def __dict__(self):
        return {
            'flairText': self.flair_text,
            'url': self.url,
            'date': self.date,
            'score': self.score
        }
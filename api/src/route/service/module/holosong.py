"""
ホロライブの歌ってみたやオリ曲のスクレイピング
"""
import requests
from bs4 import BeautifulSoup
import re

from src.route.service.module.utils import const, interface
opt = const.Option()

def get_cover_songs() -> list[interface.SongQueryRecord]:
    records = []

    # 指定したURLからHTMLを取得
    url = opt.holo_wiki_cover()
    response = requests.get(url)

    # BeautifulSoupでHTMLを解析
    soup = BeautifulSoup(response.text, 'html.parser')
    table_element = soup.find(id="table_edit_1 content_block_2")
    tr_elements = table_element.find("tbody").find_all("tr")

    # trループ
    for tr in tr_elements:
        td_elements = tr.find_all("td")
        #各要素を取得
        td_date = td_elements[0].get_text().replace('/','-')
        td_member = td_elements[1].get_text()
        td_link = ''
        td_song_name = ''
        a_tag = td_elements[2].find("a")
        if a_tag is not None:
            td_link = a_tag.get("href")
            td_song_name = a_tag.get_text()

        td_detail = td_elements[3].get_text()
        rec = interface.SongQueryRecord(td_date,td_member,td_link,td_song_name,td_detail)
        records.append(rec)
    return records

def get_original_songs() -> list[interface.SongQueryRecord]:
    records = []
    url = opt.holo_wiki_original()
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all('div',class_="wiki-section-3")
    for element in elements:
        text = element.text
        title = text.splitlines()[0].replace('"','”')
        member_match = re.search(r"メンバー：(.+?)\n", text)
        if member_match:
            members = member_match.group(1)
        date_match = re.search(r"音源公開日：(\d{4}/\d{2}/\d{2})\n", text)
        if date_match:
            release_date = date_match.group(1).replace('/','-')
        a_tags = element.find_all('a', {'class': 'outlink', 'href': True, 'target': '_blank'})
        youtube_link = [a for a in a_tags if 'youtube' in a.text.lower()]
        if len(youtube_link) > 0:
            youtube_url = youtube_link[0]['href']
            rec = interface.SongQueryRecord(release_date,members,youtube_url,title,'')
            if youtube_url != 'https://www.youtube.com/watch?v=VKyEVCPEV6c':
                records.append(rec)
    return records

def get_memory_movies() -> list[interface.HoloMemoryRecord]:
    url = opt.holo_wiki_memory()
    
    # 指定したURLからHTMLを取得
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser') 
    table_element = soup.find(id="table_edit_1 content_block_45")
    tr_elements = table_element.find("tbody").find_all("tr")

    records = []
    # trループ
    for tr in tr_elements:
        td_elements = tr.find_all("td")
        #各要素を取得
        td_date = td_elements[0].get_text().replace('/','-')
        td_member = td_elements[1].get_text()
        td_link = ''
        td_memory = td_elements[3].get_text()
        td_detail = td_elements[4].get_text()
        a_tag = td_elements[2].find("a")
        if a_tag is not None:
            td_link = a_tag.get("href")
            td_title = a_tag.get_text().replace('"','').replace("'",'')
            if '非公開' not  in td_title:
                rec = interface.HoloMemoryRecord(td_title,td_member,td_date,td_link,td_memory,td_detail)
                records.append(rec)
    return records
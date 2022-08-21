import requests
import undetected_chromedriver as uc
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Dict, List, Tuple, Any
import config
from headers import get_headers
import re


class Anime(ABC):
    site_url: str
    api_url: str
    video_file_name: str
    video_extension: str = ".mp4"

    @abstractmethod
    def search_anime(self, session, anime_name: str):
        ...

    @abstractmethod
    async def get_episode_sessions(self, session, anime_session: str):
        ...

    @abstractmethod
    def get_episode_stream_data(self, episode_session: str):
        ...


class Animepahe(Anime):
    site_url: str = "https://animepahe.com"
    api_url: str = "https://animepahe.com/api?"
    video_file_name: str = None  # variable will be assign while scraping for kwik f link
    manifest_location = "./uwu.m3u8"
    manifest_filename = "uwu.m3u8"
    master_manifest_location = "./master.m3u8"
    master_manifest_filename = "uwu.m3u8"

    def search_anime(self, session, input_anime):
        """A scraper for searching an anime user requested

        Args:
            session: request session object
            input_anime (str): name of the anime user entered

        Returns:
            json: response with the most significant match
        """
        search_headers = get_headers()

        search_params = {
            'm': 'search',
            'q': input_anime,
        }

        return session.get(f"{self.site_url}/api", params=search_params, headers=search_headers).json()["data"]

    def get_episode_sessions(self, session, anime_session: str, page_no: str = "1") -> List[Dict[str, str | int]] | None:
        """scraping the sessions of all the episodes of an anime

        Args:
            session: request session object
            anime_session (str): session of an anime (changes after each interval)
            page_no (str, optional): Page number when the episode number is greater than 30. Defaults to "1".

        Returns:
            List[Dict[str, str | int]] | None: Json with episode details
        """
        episodes_headers = get_headers({"referer": "{}/{}".format(self.site_url, anime_session)})

        episodes_params = {
            'm': 'release',
            'id': anime_session,
            'sort': 'episode_asc',
            'page': page_no,
        }

        return session.get(f"{self.site_url}/api", params=episodes_params, headers=episodes_headers).json()

    async def get_anime_description(self, session, anime_session: str) -> Dict[str, str]:
        """scraping the anime description

        Args:
            session: request session object
            anime_session (str): session of an anime (changes after each interval)

        Returns:
            Dict[str, str]: description {
                'Synopsis': str, 
                'eng_anime_name': str, 
                'Type': str, 
                'Episodes': str, 
                'Status': str, 
                'Aired': str, 
                'Season': str, 
                'Duration': str,
            }
        """
        description_header = get_headers({"referer": "{}/{}".format(self.site_url, anime_session)})
        description_response = session.get(f"{self.site_url}/anime/{anime_session}", headers=description_header)

        description_bs = BeautifulSoup(description_response.text, 'html.parser')

        description = {}

        synopsis = description_bs.find('div', {'class': 'anime-synopsis'}).text.replace('\"', '')
        description['Synopsis'] = synopsis

        anime_info = description_bs.find('div', {'class': 'anime-info'}).find_all('p')
        details = []
        for x in anime_info:
            details.append(x.text.replace('\n', ''))
        for i in range(len(details)):
            if 'English' in details[i]:
                description['eng_name'] = details[i][9:]
            if 'Type' in details[i]:
                description['Type'] = details[i][6:]
            if 'Episodes' in details[i]:
                description['Episodes'] = details[i][10:]
            if 'Status' in details[i]:
                description['Status'] = details[i][7:]
            if 'Aired' in details[i]:
                description['Aired'] = details[i][6:].replace('to', ' to')
            if 'Season' in details[i]:
                description['Season'] = details[i][8:]
            if 'Duration' in details[i]:
                description['Duration'] = details[i][10:]

        return description

    def get_episode_stream_data(self, episode_session: str) -> Dict[str, List[Dict[str, str]]]:
        """getting the streaming details

        Args:
            episode_session (str): session of an episode (changes after each interval)

        Returns:
            Dict[str, List[Dict[str, str]]]: stream_data {
                'data':[{'quality': {'kwik_pahewin': str(url)}}]
            }
        """
        # episode_session = self.episode_session_dict[episode_no]
        # ep_headers = get_headers(extra='play/{}/{}'.format(anime_session, episode_session))

        ep_params = {
            'm': 'links',
            'id': episode_session,
            'p': 'kwik',
        }

        ep_headers = get_headers()

        return requests.get(f"{self.site_url}/api", params=ep_params, headers=ep_headers).json()["data"]

    async def get_manifest_file(self, kwik_url: str) -> (str, str):
        stream_headers = get_headers(extra={"referer": self.site_url})

        stream_response = requests.get(kwik_url, headers=stream_headers)
        bs = BeautifulSoup(stream_response.text, 'html.parser')

        all_scripts = bs.find_all('script')
        pattern = r'\|\|\|.*\'\.'
        pattern_list = (re.findall(pattern, str(all_scripts[6]))[0]).split('|')[88:98]

        uwu_root_domain = f"https://{pattern_list[9]}-{pattern_list[8]}.{pattern_list[7]}.{pattern_list[6]}.{pattern_list[5]}"

        uwu_url = '{}/{}/{}/{}/{}.{}'.format(uwu_root_domain, pattern_list[4], pattern_list[3],
                                             pattern_list[2], pattern_list[1], pattern_list[0])

        return requests.get(uwu_url, headers=get_headers(extra={"origin": "https://kwik.cx", "referer": "https://kwik.cx/"})).text, uwu_root_domain


class MyAL:
    anime_types_dict = {
        "airing": "airing",
        "upcoming": "upcoming",
        "tv": "tv",
        "movie": "movie",
        "ova": "ova",
        "ona": "ona",
        "special": "special",
        "by_popularity": "bypopularity",
        "favorite": "favorite",
    }

    def get_top_anime(self, anime_type: str, limit: str):
        """request to scrape top anime from MAL website
        Args:
            anime_type (str): either of ['airing', 'upcoming', 'tv', 'movie', 'ova', 'ona', 'special', 'by_popularity', 'favorite']
            limit (str): page number (number of tops in a page)
        Returns:
            Dict[str, Dict[str, str]]: {
                "<rank>" : {
                    "img_url" : (str)url,
                    "title" : (str), 
                    "anime_type" : (str),
                    "episodes" : (str), 
                    "score" : (str), 
                }, 
                ...
                "next_top":"api_server_address/top_anime?type=anime_type&limit=limit"
            }
        """
        top_anime_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-GB,en;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        }

        top_anime_params = {
            'type': self.anime_types_dict[anime_type],
            'limit': limit,
        }

        top_anime_response = requests.get('https://myanimelist.net/topanime.php', params=top_anime_params,
                                          headers=top_anime_headers)

        bs_top = BeautifulSoup(top_anime_response.text, 'html.parser')

        rank = bs_top.find_all("span", {"class": ['rank1', 'rank2', 'rank3', 'rank4']})
        ranks = []
        for i in rank:
            ranks.append(i.text)

        img = bs_top.find_all("img", {"width": "50", "height": "70"})
        imgs = []
        for x in img:
            src = x.get("data-src")
            start, end = 0, 0
            for i in range(len(src)):
                if src[i] == '/' and src[i + 1] == 'r':
                    start = i
                if src[i] == '/' and src[i + 1] == 'i':
                    end = i
            imgs.append(src.replace(src[start:end], ""))

        title = bs_top.find_all("h3", {"class": "anime_ranking_h3"})

        info = bs_top.find_all("div", {"class": "information"})
        episodes = []
        a_type = []
        for x in info:
            val = x.text.replace('\n', '').replace(' ', '')
            start, end = 0, 0
            for i in range(len(val)):
                if val[i] == '(':
                    start = i
                if val[i] == ')':
                    end = i
            episodes.append(val[start + 1:end])
            a_type.append(val[:start])

        score = bs_top.find_all("span", {"class": [
            "score-10", "score-9", "score-8", "score-7", "score-6", "score-5", "score-4", "score-3", "score-2",
            "score-1", "score-na"
        ]})

        top_anime = []

        for i in range(len(ranks)):
            rank = ranks[i]
            if ranks[i] == "-":
                rank = "na"
            top_anime.append({"rank": rank, "img_url": imgs[i], "title": title[i].text, "anime_type": a_type[i],
                              "episodes": episodes[i].replace('eps', ''), "score": score[i].text})

        response: Dict[str, Any] = {"data": top_anime}

        try:
            next_top = bs_top.find("a", {"class": "next"}).get("href")
            response["next_top"] = f"{config.API_SERVER_ADDRESS}/top_anime{next_top}"
        except AttributeError:
            response["next_top"] = None

        try:
            prev_top = bs_top.find("a", {"class": "prev"}).get("href")
            response["prev_top"] = f"{config.API_SERVER_ADDRESS}/top_anime{prev_top}"
        except AttributeError:
            response["prev_top"] = None

        return response
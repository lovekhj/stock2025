from typing import Any
import requests
from bs4 import BeautifulSoup
from file_manager import FileManager
import datetime
import pandas as pd


def request_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    }
    response = requests.get(url, headers = headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    return soup

def naver_finace_news():
    url = f"https://finance.naver.com/news/mainnews.naver?&page=1"
    soup = request_url(url)
    # newslists = soup.select("div.mainNewsList._replaceNewsLink > ul > li > dl > dd.articleSubject")
    newslists = soup.select("div.mainNewsList._replaceNewsLink > ul > li > dl > dd.articleSubject")
    print(newslists)
 

if __name__ == '__main__':
    naver_finace_news()
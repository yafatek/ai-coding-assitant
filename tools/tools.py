import os

import googleapiclient.discovery
import requests
from bs4 import BeautifulSoup

search_engine_id = os.environ.get('SEARCH_ENGIN_ID')
api_key = os.environ.get('GOOGLE_SEARCH_API_KEY')


def search_custom_engine(search_query: str):
    """
    Searches a Google Custom Search Engine.
    Args:
      search_query: The search query.
    Returns: A list of search results. usually contains urls use url to l
    """
    print('[*] start searching...')
    service = googleapiclient.discovery.build("customsearch", "v1", developerKey=api_key, cache_discovery=False)
    res = service.cse().list(q=search_query, cx=search_engine_id).execute()
    return res['items']


def scrape_website(search_url: str):
    """
    Scrapes data from a website.
    Args:
      search_url: The URL of the website to scrape.
    Returns: an array of paragraphs in the websites
    """
    print('[*] start scraping...')
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, "html.parser")
    return [p.get_text() for p in soup.find_all("p")]

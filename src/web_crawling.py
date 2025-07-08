from typing import List, Dict, Optional

import requests
from bs4 import BeautifulSoup
import logging

LOGGER = logging.getLogger(__name__)
URL = 'https://www.angelcomedy.co.uk/bill-murray/'

def webscrape_bill_murray_homepage(url: str) -> Dict[str, List[str]] | None:
    """
    Extract all events from bill murray homepage.

    Input:
    ** url: str for the bill murray homepage

    Output:
    ** events_and_urls: dict of the events and their urls on the homepage
    """
    # Send a GET request to the webpage
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the <h2> tag with the exact text "What's on"
        header = soup.find('h2', string=lambda text: text and text.strip().lower() == "what's on")
        if header:
            # Find the first <div> directly after this <h2>
            div = header.find_next_sibling('div')
            if div:
                events_and_urls = extract_events_and_urls_from_div(div)
                # Find all <article> tags inside that div
                return events_and_urls
            else:
                LOGGER.error("No <div> found after the <h2>.")
                return None
        else:
            LOGGER.error("No <h2> with text 'What's on' found.")
            return None

def extract_events_and_urls_from_div(div: BeautifulSoup) -> Optional[Dict]:
    """
    Extract event url from event article.

    Input:
    ** div: article object from the webpage

    Output:
    ** event_url: string containing the event url or "No URL for event." if none found
    """

    articles = div.find_all('article')
    events_and_urls = {
        "events": [],
        "urls": []
    }
    for i, article in enumerate(articles, start=1):
        events_and_urls["events"].append(article.get_text(strip=True))
        events_and_urls["urls"].append(extract_event_link_from_article(article))
        LOGGER.info(f"Article {i}:")
        LOGGER.info(article.get_text(strip=True))
        LOGGER.info("-" * 40)
    return events_and_urls

def extract_event_link_from_article(article: BeautifulSoup) -> Optional[str]:
    """
    Extract event url from event article.

    Input:
    ** article: article object from the webpage

    Output:
    ** event_url: string containing the event url or "No URL for event." if none found
    """
    link_tag = article.find('a')
    if link_tag and link_tag.has_attr('href'):
        event_url = link_tag['href']
        LOGGER.info(f"Article {article.get_text(strip=True)} link: {event_url}")
        return event_url
    else:
        LOGGER.error(f"Article {article.get_text(strip=True)} has no link")
        return "No URL for event."

def extract_relevant_comedians_from_events(
        comedians: List[str],
        events_and_urls: Dict[str, List[str]] | None
) -> List[Dict[str, List[str]]]:
    """
    Extract comedians defined in config from events and urls.
    
    Input:
    ** comedians: list of comedians we're looking for
    ** events_and_urls: dictionary of lists of events and urls from web page
    
    Output:
    ** comedians_and_urls: list of comedian dictionaries containing any upcoming events and the urls for that comedian.
    """
    if events_and_urls:
        if 'events' not in events_and_urls or 'urls' not in events_and_urls:
            return []

        comedians_and_urls = []

        for comedian in comedians:
          matches = [item for item in events_and_urls['events'] if comedian.lower() in item.lower()]
          if len(matches) > 0:
            urls = [events_and_urls['urls'][events_and_urls['events'].index(match)] for match in matches]
            comedians_and_urls.append({
                "Comedian": comedian,
                "Events": matches,
                "Urls": urls
            })

        return comedians_and_urls
    else:
        return []

def extract_relevant_events_from_bill_murray_homepage(comedians: List[str]) -> List[Dict[str, List[str]]]:
    """
    Extract relevant events from bill-murray homepage.

    Input:
    ** comedians: list of comedians we're looking for

    Output:
    ** comedians_and_urls: list of comedian dictionaries containing any upcoming events and the urls for that comedian.
    """
    events_and_urls = webscrape_bill_murray_homepage(URL)
    if events_and_urls:
        return extract_relevant_comedians_from_events(comedians, events_and_urls)
    else:
        return []


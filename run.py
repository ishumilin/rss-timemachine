import requests
import feedparser
import json
import time
from bs4 import BeautifulSoup
import argparse

CDX_API_URL_TEMPLATE = "https://web.archive.org/cdx/search/cdx?url={}&output=json"
MAX_RETRIES = 5
RETRY_DELAY = 2  # Initial delay in seconds

def fetch_cdx_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch CDX data: {response.status_code}")
        return None

def fetch_rss_feed(url):
    return feedparser.parse(url)

def fetch_with_retries(url, max_retries, delay):
    for attempt in range(max_retries):
        print(f"Attempt {attempt + 1} to fetch URL: {url}")
        try:
            feed = fetch_rss_feed(url)
            if feed.bozo == 0:
                return feed
            else:
                print(f"Error parsing feed at {url}: {feed.bozo_exception}")
        except Exception as e:
            print(f"Exception occurred while fetching URL: {e}")
        
        time.sleep(delay)
        delay *= 2  # Exponential backoff

    print(f"Max retries reached for URL: {url}")
    return None

def parse_feed(feed):
    entries = []
    for entry in feed.entries:
        raw_content = entry.content[0].value if 'content' in entry else ""
        soup = BeautifulSoup(raw_content, "html.parser")
        clean_content = soup.get_text(separator="\n").strip()

        parsed_entry = {
            'title': entry.title,
            'description': entry.description,
            'link': entry.link,
            'published': entry.published,
            'content': clean_content,
        }
        entries.append(parsed_entry)
    return entries

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def main():
    parser = argparse.ArgumentParser(description='Fetch and process website RSS feeds through the Wayback Machine.')
    parser.add_argument('website', type=str, help='The website URL to fetch the RSS feed for.')
    args = parser.parse_args()
    website = args.website

    cdx_api_url = CDX_API_URL_TEMPLATE.format(website)

    cdx_data = fetch_cdx_data(cdx_api_url)
    
    if cdx_data is None:
        print("No CDX data available.")
        return
    
    archives = cdx_data[1:]  # Skip the header
    all_entries = []
    seen_links = set()
    
    for archive in archives:
        timestamp = archive[1]
        url = f"https://web.archive.org/web/{timestamp}/http://{website}"
        print(f"Processing {url}")
        
        feed = fetch_with_retries(url, MAX_RETRIES, RETRY_DELAY)
        if feed is None:
            continue

        parsed_entries = parse_feed(feed)

        for entry in parsed_entries:
            if entry['link'] not in seen_links:
                seen_links.add(entry['link'])
                all_entries.append(entry)

    if all_entries:
        save_to_json(all_entries, "all_rss_feeds.json")
        print("All RSS feeds have been successfully saved to 'all_rss_feeds.json'")
    else:
        print("No RSS entries were successfully processed.")

if __name__ == "__main__":
    main()
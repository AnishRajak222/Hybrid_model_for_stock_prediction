import requests
from bs4 import BeautifulSoup
from newspaper import  build  # type: ignore
from RapidAPI import *
from NewsAPI_ORG import *
from YfinanceHeadlines import *

# List of keywords for the IT sector
IT_KEYWORDS = [
    "Information Technology", "IT", "Tech", "Technology Sector",
    "IT Companies", "Software", "IT Services", "Tech Industry",
    "Digital Transformation", "Cybersecurity","Innovation", "AI", "blockchain" , "cloud computing",
    "Indian Information Technology", "India IT", "Indian Tech", "Indian Technology Sector",
    "Indian IT Companies", "Indian Software", "Indian IT Services", "Indian Tech Industry",
    "Indian Digital Transformation", "Indian Cybersecurity", 
    "AI India", "Blockchain India", "Cloud Computing India", "HCL", "Infosys", "TCS", "Wipro"
]



def fetch_all_headlines_Static(IT_KEYWORDS):
    print("Fetching Static sites..")
    # News sites configuration
    NEWS_SITES = [
        {
            "name": "Moneycontrol",
            "url_pattern": "https://www.moneycontrol.com/news/tags/{keyword}.html",
            "headline_tag": "h2",
            "headline_class": "content_headline"
        },
        {
            "name": "Economic Times",
            "url_pattern": "https://economictimes.indiatimes.com/topic/{keyword}",
            "headline_tag": "a",
            "headline_class": "title"
        }
        ]

    all_headlines_list = []

    #Loop each keyword
    for site in NEWS_SITES:
        for keyword in IT_KEYWORDS:
            keyword_formatted = keyword.lower().replace(" ", "-")

        #Loop each site configuration
            # Format the URL for each site with the current keyword
            url = site["url_pattern"].format(keyword=keyword_formatted)
            print(f"Fetching from {site['name']}: {url}")  # Debug print
            # Send the HTTP request
            response = requests.get(url)
            print(f"Status Code ({site['name']}): {response.status_code}")
            if response.status_code != 200:
                continue  # Skip if there was an issue with the request

            # Parse the HTML content
            soup = BeautifulSoup(response.text, "html.parser")
            # Extract headlines using the specified tag and class for each site
            headlines = [
                h.get_text(strip=True) for h in soup.find_all(site["headline_tag"], class_=site["headline_class"])
            ]

            # Append each headline to the list with the site name for clarity
            for headline in headlines:
                all_headlines_list.append(f"{site['name']}: {headline}")
    # print(all_headlines_list)
    return all_headlines_list







# Function to fetch and filter headlines for Dynamic Sites
def fetch_all_headlines_Dynamic(IT_KEYWORDS):
    print("Fetching Dynamic sites..")
    headlines = []
    NEWS_SOURCES = [    "https://www.moneycontrol.com/",    "https://economictimes.indiatimes.com/markets",    "https://www.business-standard.com/",    "https://www.businesstoday.in/"]

    # print("Fetching news from Newspaper websites...")
    for source_url in NEWS_SOURCES:
        news_site = build(source_url, memoize_articles=False)  # Disable caching for fresh data
        for article in news_site.articles[:20]:  # Limit to first 20 articles for demo
            try:
                article.download()
                article.parse()
                title = article.title
                # Check if any keyword matches the headline
                if any(keyword.lower() in title.lower() for keyword in IT_KEYWORDS):
                    headlines.append(title)
            except Exception as e:
                print(f"Error processing article from {source_url}: {e}")
                pass
    return headlines





def fetch_all_headlines():
    headlines=fetch_all_headlines_Static(IT_KEYWORDS)
    headlines.extend(fetch_all_headlines_Dynamic(IT_KEYWORDS))
    headlines.extend(FetchHeadlinesYfinance())
    
    # headlines.extend(Fetch_Headlines_RapidAPI())
    # headlines.extend(Fetch_Headlines_NewsAPI())
    # print(headlines)
    return headlines



# print(fetch_all_headlines_Static(IT_KEYWORDS))
# print(fetch_all_headlines_Dynamic(IT_KEYWORDS))
# Fetch_Headlines_RapidAPI()





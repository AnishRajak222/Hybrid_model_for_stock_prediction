import requests

url = "https://news-api65.p.rapidapi.com/api/v1/news/y/search"
# querystring = {"keyword": "WIPRO.NS"}

headers = {
    "x-rapidapi-key": "2e2a784840msh4f42e2bd3fc7853p1de91cjsn3a7b41a5404f",
	"x-rapidapi-host": "news-api65.p.rapidapi.com"
}
def StockNews(querystring):
    response = requests.get(url, headers=headers, params=querystring)
    news_data = response.json()  # Convert response to JSON
    print("\n"*5)
    # Ensure we have data and it's a list
    Headline=[]
    print(response)
    if isinstance(news_data, list):
        for article in news_data[:5]:  # Limit to 5 articles
            title = article.get("title", "No Title")  # Fetch title
            link = article.get("link", "No Link")  # Fetch URL
            print(f"Title: {title}\nURL: {link}\n{'-' * 50}")
            Headline.append(title)
    else:
        print("No news articles found or incorrect response format.")
        pass
    return Headline

def FetchHeadlinesYfinance():
    print("Fetching Headlines from Yfinance...")
    x= [
    "HCLTECH.NS",
    "INFY.NS",
    "TCS.NS",
    "WIPRO.NS",
    "TECHM.NS",
    "LTIM.NS",
    "PERSISTENT.NS",
    "OFSS.NS",
    "POLICYBZR.NS",
    "SASKEN.NS",
    "QUICKHEAL.NS",
    "BSOFT.NS"]
    headlines=[]
    for i in x:
        temp={"keyword": i}
        print(f"'keyword': {i}")
        headlines.extend(StockNews(temp))
    return headlines

if __name__ == "__main__":
    print(FetchHeadlinesYfinance())
    # StockNews({"keyword":"TCS.NS"})

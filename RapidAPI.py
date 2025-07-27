import http.client
import json

def fetch_articles_R_api():
    conn = http.client.HTTPSConnection("share-market-news-api-india.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "6ec096c156msh9d4e3b5341d5c2bp129091jsnfc75950e6d16",
        'x-rapidapi-host': "share-market-news-api-india.p.rapidapi.com"
    }
    
    conn.request("GET", "/marketNews", headers=headers)
    res = conn.getresponse()
    data = res.read()
    # print("Raw response data:", data)  # Added line to print raw data
    if data:
        try:
            articles = json.loads(data.decode("utf-8"))
            return articles
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            return None
    else:
        print("No data received from the API.")
        return None


def Fetch_Headlines_RapidAPI( ):
    keywords=[
    "Information Technology", "IT", "Tech", "Technology Sector",
    "IT Companies", "Software", "IT Services", "Tech Industry",
    "Digital Transformation", "Cybersecurity", "Innovation", 
    "AI", "blockchain", "cloud computing",'HCL' ,'INFOSYS','TCS','WIPRO']
    articles = fetch_articles_R_api()
    if articles is None:
        print("No articles fetched or error in fetching articles.")
        return []
    filtered_headlines = []
    for article in articles:
        title = article.get("Title", "").lower()  # Convert for case-insensitive matching
        if any(keyword.lower() in title for keyword in keywords):  # Check for each keyword in title
            filtered_headlines.append(title)
    
    return filtered_headlines

# Fetch the articles


# Filter headlines based on keywords
# Print the filtered results
if __name__ =="__main__":
    filtered_headlines = Fetch_Headlines_RapidAPI()

    c=0
    for headline in filtered_headlines:
        c+=1
        print(f"\n{c}{headline}")

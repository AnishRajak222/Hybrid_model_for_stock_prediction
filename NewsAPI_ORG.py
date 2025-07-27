import requests

# Function to scrape headlines and descriptions for a list of keywords
def Fetch_Headlines_NewsAPI():
    print("Fetching from NEWS API...")
    keywords = [
        "Indian Information Technology", "India IT", "Indian Tech", "Indian Technology Sector",
        "Indian IT Companies", "Indian Software", "Indian IT Services", "Indian Tech Industry",
        "Indian Digital Transformation", "Indian Cybersecurity", 
        "AI India", "Blockchain India", "Cloud Computing India", "HCL", "Infosys", "TCS", "Wipro"
    ]
    headlines_data = [] 

    for keyword in keywords:
        # Construct the URL with the keyword and other parameters
        APIKEY = 'fa9d58a241654953a6779b16f48cb2ad'
        url = f'https://newsapi.org/v2/everything?q={keyword}&from=2024-11-07&sortBy=popularity&apiKey={APIKEY}'
        response = requests.get(url)

        # Parse the JSON response
        data = response.json()

        # Check if the response is valid and contains articles
        if data['status'] == 'ok' and data['totalResults'] > 0:
            for article in data['articles']:
                # Extract the description field
                headline_info = article['description']
                headlines_data.append(headline_info)
        else:
            # Skip keywords with no results
            pass

    # Return the list of headlines and descriptions
    if not headlines_data:
        print("No headline")
    return headlines_data

# Call the function to fetch headlines
if __name__ == '__main__':
    headlines = Fetch_Headlines_NewsAPI()
    
    # Print the result to verify output
    print("Fetched Headlines:", headlines)

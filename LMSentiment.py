import pandas as pd
import re

# Load Loughran-McDonald Dictionary from CSV
def load_lm_dictionary(filepath):
    df = pd.read_csv(filepath)

    # Ensure correct column names (Check your CSV headers)
    word_col = "Word"
    pos_col = "Positive" if "Positive" in df.columns else "Positiv"
    neg_col = "Negative" if "Negative" in df.columns else "Negat"

    # Convert to dictionary with lowercase words
    sentiment_dict = {
        "positive": set(df[df[pos_col] > 0][word_col].str.lower().str.strip()),  
        "negative": set(df[df[neg_col] > 0][word_col].str.lower().str.strip()),  
    }
    return sentiment_dict

# Function to analyze sentiment for each text and compute final sentiment score
def analyze_sentiment(text_list, sentiment_dict):
    results = []
    total_weighted_score = 0
    total_weight = 0

    for text in text_list:
        words = re.findall(r'\b\w+\b', text.lower())  # Tokenize text
        positive_count = sum(1 for word in words if word in sentiment_dict["positive"])
        negative_count = sum(1 for word in words if word in sentiment_dict["negative"])
        total_sentiment_words = positive_count + negative_count

        # Normalize score to range [-1, +1]
        score = (positive_count - negative_count) / total_sentiment_words if total_sentiment_words > 0 else 0.0

        # Accumulate weighted score for final aggregation
        total_weighted_score += score * total_sentiment_words
        total_weight += total_sentiment_words

        results.append({"text": text, "score": round(score, 4), "sentiment_word_count": total_sentiment_words})
    
    # Calculate the final aggregated sentiment score
    final_score = total_weighted_score / total_weight if total_weight > 0 else 0.0

    return results, round(final_score, 4)

# Function that takes text list and returns final sentiment score
def LMSentimentScore(headlines):
    lm_dict = load_lm_dictionary(r"D:\Project\Loughran-McDonald_MasterDictionary_1993-2023(1).csv")  # Load dictionary
    sentiment_results, final_sentiment_score = analyze_sentiment(headlines, lm_dict)
    
    # Print individual results ( Sentiment Score for each sentence)
    # for res in sentiment_results:
    #     print(res)

    print("\nFinal Aggregated Sentiment Score:", final_sentiment_score)
    
    return final_sentiment_score


# Fetch headlines and compute final sentiment score
if __name__ == "__main__":

    #Testing 1
    # from YfinanceHeadlines import * #Remove this after tests are finished
    # headlines = FetchHeadlinesYfinance()
    # final_score = LMSentimentScore(headlines)

    ## Testing 2
    # Sample_string=['Worst Performance in Q3']
    # print("Final sentiment score: ",LMSentimentScore(Sample_string))
    pass
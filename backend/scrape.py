from apify_client import ApifyClient
from dotenv import load_dotenv
import os
import json
import pandas as pd
import requests
import streamlit as st

# # Load environment variables from a .env file
# load_dotenv()

# # Get the necessary tokens from the environment variables
# APIFY_API_TOKEN = os.getenv("apify_token")

# ACCESS_TOKEN = os.getenv("REDDIT_ACCESS_TOKEN")
# CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
# CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
# USERNAME = os.getenv("REDDIT_USERNAME")
# PASSWORD = os.getenv("REDDIT_PASSWORD")
# USER_AGENT = os.getenv("REDDIT_USER_AGENT")


# Get API tokens and credentials
APIFY_API_TOKEN = st.secrets["apify"]["apify_token"]

ACCESS_TOKEN = st.secrets["reddit"]["REDDIT_ACCESS_TOKEN"]
CLIENT_ID = st.secrets["reddit"]["REDDIT_CLIENT_ID"]
CLIENT_SECRET = st.secrets["reddit"]["REDDIT_CLIENT_SECRET"]
USERNAME = st.secrets["reddit"]["REDDIT_USERNAME"]
PASSWORD = st.secrets["reddit"]["REDDIT_PASSWORD"]
USER_AGENT = st.secrets["reddit"]["REDDIT_USER_AGENT"]

def scrape_tweets(search_query):
    """
    Scrapes popular and relevant tweets (including replies) based on the provided search query
    using Apify's Tweet Scraper V2 actor.

    Args:
        search_query (str): The query to search for tweets.

    Returns:
        str: A formatted string containing all tweet texts indexed and grouped under the search query.
    """
    # Initialize the Apify client
    client = ApifyClient(APIFY_API_TOKEN)
    
    # Define the actor input.
    run_input = {
        "max_posts": 10,
        "query": search_query,
        "search_type": "Top"
    }
    
    # Call the Tweet Scraper V2 actor and wait for it to finish
    run = client.actor("ghSpYIW3L1RvT57NT").call(run_input=run_input)
    
    tweet_texts = []
    
    # Iterate over each item in the dataset and extract tweet text
    dataset = client.dataset(run["defaultDatasetId"])
    for idx, item in enumerate(dataset.iterate_items(), start=1):
        tweet_texts.append(f"{idx}. {item.get('text', '').strip()}")

    # Combine all tweet texts into a single formatted string
    formatted_tweets = f"Search Query: {search_query}\n" + "\n".join(tweet_texts) + "\n"
    
    return formatted_tweets



def scrape_instagram(search_query):
    """
    Scrapes Instagram search results for a given query using Apify's Instagram Search Scraper.
    
    Args:
        search_query (str): The search query for Instagram.
        
    Returns:
        str: A formatted string containing all captions indexed and grouped under the search query.
    """
    # Initialize the Apify client
    client = ApifyClient(APIFY_API_TOKEN)
    
    # Remove spaces from the query
    cleaned_query = search_query.replace(" ", "")

    # Prepare the Actor input
    run_input = {
        "hashtags": [cleaned_query],
        "resultsType": "posts",
        "resultsLimit": 5
    }

    # Run the Actor and wait for it to finish
    run = client.actor("reGe1ST3OBgYZSsZJ").call(run_input=run_input)

    # Collect captions
    captions = []

    # Fetch captions from the dataset
    dataset = client.dataset(run["defaultDatasetId"])
    for idx, item in enumerate(dataset.iterate_items(), start=1):
        caption = item.get("caption", "").strip()
        if caption:  # Only include non-empty captions
            captions.append(f"{idx}. {caption}")

    # Format the output string
    formatted_captions = f"Search Query: {search_query}\n" + "\n".join(captions) + "\n"

    return formatted_captions



def get_reddit_access_token():
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    data = {
        'grant_type': 'password',
        'username': USERNAME,
        'password': PASSWORD
    }
    headers = {'User-Agent': USER_AGENT}

    response = requests.post(
        'https://www.reddit.com/api/v1/access_token',
        auth=auth,
        data=data,
        headers=headers
    )

    if response.status_code != 200:
        raise Exception(f"Failed to get access token: {response.text}")

    return response.json().get('access_token')


def scrape_reddit(subreddit, query, limit=10):
    ACCESS_TOKEN = get_reddit_access_token()  # Always fetch a fresh token

    headers = {
        "Authorization": f"bearer {ACCESS_TOKEN}",
        "User-Agent": USER_AGENT
    }

    url = f"https://oauth.reddit.com/r/{subreddit}/search?q={query}&restrict_sr=1&sort=relevance&limit={limit}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return f"Error: Unable to fetch data from Reddit (Status Code {response.status_code})"

    data = response.json()

    output = f" **Subreddit:** r/{subreddit}\n **Query:** {query}\n\n"
    for post in data['data']['children']:
        post_data = post['data']
        title = post_data.get('title', 'No Title')
        context = post_data.get('selftext', 'No Context Available')

        output += f"**Title:** {title}\n"
        output += f"**Context:** {context[:500]}...\n"

    return output.strip()

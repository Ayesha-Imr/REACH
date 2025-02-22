from backend import database, llm, extract, scrape

def register(username, password):
    return database.sign_up(username, password)

def login(username, password):
    return database.log_in(username, password)

def url_extraction(url):
    return extract.url_extract(url)

def sitemap_extract(url):
    return extract.scrape_sitemap(url)

def local_extract(file_path): 
    return extract.file_local_extract(file_path)    

def summary(info):
    return llm.get_summary(info)

def create_chunks(text, chunk_size, overlap_size):
    return database.chunk(text, chunk_size, overlap_size)

def chunks_list(chunked_text, source, description):
    return database.get_chunks_list(chunked_text, source, description)

def insert_data(chunks_list, userid):
    return database.add_data(chunks_list, userid)

def startup_info(userid):
    return database.get_startup_info(userid)

def keywords(info):
    return llm.get_keywords(info)

def get_tweets(search_query):
    tweets = []
    for query in search_query:
        tweets.append(scrape.scrape_tweets(query))
    return tweets

def get_instagram_data(search_query):
    insta_data = []
    for query in search_query:
        insta_data.append(scrape.scrape_instagram(query))
    return insta_data

def get_reddit_data(search_query):
    reddit_data = []
    subreddits = search_query.subreddits
    queries = search_query.queries
    
    for subreddit, query in zip(subreddits, queries):
        reddit_data.append(scrape.scrape_reddit(subreddit, query))
    
    return reddit_data

def instagram_insights(info, data):
    combined_data = ' '.join(data)
    return llm.get_instagram_insights(info, combined_data)

def reddit_insights(info, data):
    combined_data = ' '.join(data)
    return llm.get_reddit_insights(info, combined_data)

def twitter_insights(info, data):
    combined_data = ' '.join(data)
    return llm.get_twitter_insights(info, combined_data)

def agent(query, startup_info):
    return llm.ask_agent(query, startup_info)





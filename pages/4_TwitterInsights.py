import streamlit as st
from backend import main
from streamlit import session_state

st.set_page_config(page_title="Twitter Insights", page_icon="🐦")

st.title("Twitter Insights")

if 'user_id' not in session_state:
    st.warning("Please log in or sign up first.")
else:
    if st.button("Get Twitter Insights"):
        with st.spinner("Fetching startup info..."):
            startup_info = main.startup_info(session_state.user_id)
            print(startup_info)
        
        if "keywords" not in session_state:
            with st.spinner("Extracting keywords..."):
                keywords = main.keywords(startup_info)
                print(keywords)
                session_state.keywords = keywords
                twitter_keywords = keywords.twitter 
        else:
            twitter_keywords = session_state.keywords.twitter
        
        with st.spinner("Fetching tweets..."):
            print(twitter_keywords)
            tweets = main.get_tweets(twitter_keywords)
            print(tweets)
        
        with st.spinner("Generating insights..."):
            insights = main.twitter_insights(startup_info, tweets)
        
        st.success("Twitter Insights generated successfully!")
        st.write(insights)
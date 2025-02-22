import streamlit as st
from backend import main
from streamlit import session_state

st.set_page_config(page_title="Instagram Insights", page_icon="📷")

st.title("Instagram Insights")

if 'user_id' not in session_state:
    st.warning("Please log in or sign up first.")
else:
    if st.button("Get Instagram Insights"):
        with st.spinner("Fetching startup info..."):
            startup_info = main.startup_info(session_state.user_id)
            print(startup_info)
        
        if "keywords" not in session_state:
            with st.spinner("Extracting keywords..."):
                keywords = main.keywords(startup_info)
                print(keywords)
                session_state.keywords = keywords
                instagram_keywords = keywords.instagram 
        else:
            instagram_keywords = session_state.keywords.instagram
            
        with st.spinner("Fetching tweets..."):
            print(instagram_keywords)
            insta_data = main.get_tweets(instagram_keywords)
            print(insta_data)
        
        with st.spinner("Generating insights..."):
            insta_insights = main.instagram_insights(startup_info, insta_data)
            print(insta_insights)
        
        st.success("Instagram Insights generated successfully!")
        st.write(insta_insights)

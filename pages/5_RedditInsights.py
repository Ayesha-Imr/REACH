import streamlit as st
from backend import main
from streamlit import session_state

st.set_page_config(page_title="Reddit Insights", page_icon="🔺")

st.title("Reddit Insights")

if 'user_id' not in session_state:
    st.warning("Please log in or sign up first.")
else:
    if st.button("Get Reddit Insights"):
        with st.spinner("Fetching startup info..."):
            startup_info = main.startup_info(session_state.user_id)
            print(startup_info)

        if "keywords" not in session_state:
            with st.spinner("Extracting keywords..."):
                keywords = main.keywords(startup_info)
                print(keywords)
                session_state.keywords = keywords
                reddit_keywords = keywords.reddit 
        else:
            reddit_keywords = session_state.keywords.reddit
        
        with st.spinner("Fetching Reddit data..."):
            print(reddit_keywords)
            reddit_data = main.get_reddit_data(reddit_keywords)
            print(reddit_data)
        
        with st.spinner("Generating insights..."):
            generated_reddit_insights = main.reddit_insights(startup_info, reddit_data)
        
        st.success("Reddit Insights generated successfully!")
        st.write(generated_reddit_insights)
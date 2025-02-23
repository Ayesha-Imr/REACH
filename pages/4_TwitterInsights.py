import streamlit as st
from backend import main
from streamlit import session_state

# Set up page configuration
st.set_page_config(page_title="Twitter Insights", page_icon="🐦", layout="wide")

# Custom Styling
st.markdown(
    """
    <style>
        .title {
            font-size: 36px;
            font-weight: bold;
            color: #1DA1F2;
            text-align: center;
            margin-bottom: -10px;
        }
        .subtitle {
            font-size: 18px;
            color: #555;
            text-align: center;
            margin-bottom: 30px;
        }
        .section {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .success {
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            color: #1DA1F2;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Page Title
st.markdown('<h1 class="title">🐦 Twitter Insights</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Discover what’s trending in your market and refine your Twitter strategy.</p>', unsafe_allow_html=True)

# Authentication Check
if 'user_id' not in session_state:
    st.warning("⚠️ Please log in or sign up first to access Twitter Insights.")
    st.stop()  # Prevents further execution if the user is not logged in

# Button to generate insights
if st.button("🔍 Get Twitter Insights", key="get_twitter_insights"):
    with st.spinner("📡 Fetching startup info..."):
        startup_info = main.startup_info(session_state.user_id)
    
    if "keywords" not in session_state:
        with st.spinner("🔑 Extracting relevant Twitter keywords..."):
            keywords = main.keywords(startup_info)
            session_state.keywords = keywords
            twitter_keywords = keywords.twitter 
    else:
        twitter_keywords = session_state.keywords.twitter

    with st.spinner("🐦 Fetching relevant tweets..."):
        tweets = main.get_tweets(twitter_keywords)

    with st.spinner("📊 Generating insights from Twitter data..."):
        insights = main.twitter_insights(startup_info, tweets)

    # Display insights nicely
    if insights:
        st.success("✅ Twitter Insights generated successfully!")

        # Display platform
        st.markdown(f"### 📢 Platform: {insights.platform}")

        # Market Trends
        with st.expander("📈 **Market Trends**", expanded=True):
            st.markdown(f"💡 {insights.market_trends}")

        # Customer Insights
        with st.expander("👥 **Customer Insights**", expanded=True):
            st.markdown(f"🔍 {insights.customer_insights}")

        # Competitive Landscape
        with st.expander("🏆 **Competitive Landscape**", expanded=True):
            st.markdown(f"⚔️ {insights.competitive_landscape}")

        # Content Strategy
        with st.expander("📝 **Content Strategy**", expanded=True):
            st.markdown(f"📢 {insights.content_strategy}")

        # Marketing Tactics
        with st.expander("🎯 **Marketing Tactics**", expanded=True):
            st.markdown(f"🚀 {insights.marketing_tactics}")

    else:
        st.error("❌ No insights were generated. Please try again later.")



import streamlit as st
from backend import main
from streamlit import session_state

# Set up page configuration
st.set_page_config(page_title="Instagram Insights", page_icon="📷", layout="wide")

# Custom Styling
st.markdown(
    """
    <style>
        .title {
            font-size: 36px;
            font-weight: bold;
            color: #E4405F;
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
            color: #E4405F;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Page Title
st.markdown('<h1 class="title">📷 Instagram Insights</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Uncover content trends, audience behavior, and influencer impact on Instagram.</p>', unsafe_allow_html=True)

# Authentication Check
if 'user_id' not in session_state:
    st.warning("⚠️ Please log in or sign up first to access Instagram Insights.")
    st.stop()

# Button to generate insights
if st.button("🔍 Get Instagram Insights", key="get_instagram_insights"):
    with st.spinner("📡 Fetching startup info..."):
        startup_info = main.startup_info(session_state.user_id)

    if "keywords" not in session_state:
        with st.spinner("🔑 Extracting relevant Instagram keywords..."):
            keywords = main.keywords(startup_info)
            session_state.keywords = keywords
            instagram_keywords = keywords.instagram
    else:
        instagram_keywords = session_state.keywords.instagram

    with st.spinner("📷 Fetching relevant Instagram data..."):
        insta_data = main.get_instagram_data(instagram_keywords)

    with st.spinner("📊 Generating insights from Instagram data..."):
        insights = main.instagram_insights(startup_info, insta_data)

    # Display insights nicely
    if insights:
        st.success("✅ Instagram Insights generated successfully!")

        # Display platform
        st.markdown(f"### 📢 Platform: {insights.platform}")

        # Content Trends
        with st.expander("📸 **Content Trends**", expanded=True):
            st.markdown(f"💡 {insights.content_trends}")

        # Audience Behavior
        with st.expander("👥 **Audience Behavior**", expanded=True):
            st.markdown(f"🔍 {insights.audience_behavior}")

        # Influencer Landscape
        with st.expander("🌟 **Influencer Landscape**", expanded=True):
            st.markdown(f"🔥 {insights.influencer_landscape}")

        # Content Strategy
        with st.expander("📝 **Content Strategy**", expanded=True):
            st.markdown(f"📢 {insights.content_strategy}")

        # Engagement Tactics
        with st.expander("🎯 **Engagement Tactics**", expanded=True):
            st.markdown(f"🚀 {insights.engagement_tactics}")

    else:
        st.error("❌ No insights were generated. Please try again later.")

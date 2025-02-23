import streamlit as st
import os

# Set up page configuration
st.set_page_config(page_title="REACH - Home", page_icon="🚀", layout="wide")

# Custom Styling
st.markdown(
    """
    <style>
        .title {
            font-size: 50px;
            font-weight: bold;
            color: #2C3E50;
            text-align: center;
            margin-bottom: -10px;
        }
        .subtitle {
            font-size: 30px;
            color: #555;
            text-align: center;
            margin-bottom: 30px;
        }
        .section {
            background-color: #f9f9f9;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .highlight {
            color: #E74C3C;
            font-weight: bold;
        }
        .image-container {
            text-align: center;
            margin-bottom: 30px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title & Subtitle
st.markdown('<h1 class="title">🚀 Welcome to REACH</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Helping Founders Reach the Right Audience at the Right Time</p>', unsafe_allow_html=True)

# Feature Overview 
st.markdown(
    """
    <div class="section">
    <p>
    <span class="highlight">REACH</span> <strong>unlocks your market’s pulse</strong>. Instantly understand your 
    <strong>target audience</strong> by uploading your startup’s materials, such as <strong>website links</strong> 
    and <strong>pitch decks</strong>. Our AI analyzes <strong>real-time trends</strong> on 
    <strong>Instagram, Twitter, and Reddit</strong>, delivering deep insights into 
    <strong>customer needs, competitor activity, and emerging opportunities</strong>.
    </p>
    
    <h4>✨ What You Get with REACH:</h4>
    <ul>
        <li><strong>AI-powered marketing strategies</strong> tailored for your startup</li>
        <li><strong>Trend analysis</strong> across key social platforms</li>
        <li><strong>Competitor insights</strong> to help refine your positioning</li>
        <li><strong>A RAG-based AI agent</strong> for deep market analysis</li>
    </ul>

    <p><strong>Navigate using the sidebar</strong> to explore the features!</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Get absolute path to the diagrams folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIAGRAMS_DIR = os.path.join(BASE_DIR, "diagrams")

# Flow Diagrams Expander
with st.expander("📊 **How REACH Works: Flow Diagrams**", expanded=False):
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image(os.path.join(DIAGRAMS_DIR, "reach-diag-1.png"), caption="Step 1: Data Upload Flow", use_column_width=False, width=400)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image(os.path.join(DIAGRAMS_DIR, "reach-diag-2.png"), caption="Step 2: LLM Analysis & Insights Flow", use_column_width=False, width=400)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image(os.path.join(DIAGRAMS_DIR, "reach-diag-3.png"), caption="Step 3: AI Agent Flow", use_column_width=False, width=400)
    st.markdown('</div>', unsafe_allow_html=True)
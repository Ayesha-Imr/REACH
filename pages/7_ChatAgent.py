import streamlit as st
from backend import main
from streamlit import session_state

# Set up page configuration
st.set_page_config(page_title="AI Agent Chat", page_icon="🤖", layout="wide")

# Custom Styling
st.markdown(
    """
    <style>
        .title {
            font-size: 36px;
            font-weight: bold;
            color: #4CAF50;
            text-align: center;
            margin-bottom: -10px;
        }
        .subtitle {
            font-size: 18px;
            color: #555;
            text-align: center;
            margin-bottom: 30px;
        }
        .chat-container {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .user-message {
            font-weight: bold;
            color: #333;
        }
        .bot-message {
            font-weight: bold;
            color: #4CAF50;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Page Title
st.markdown('<h1 class="title">🤖 AI Agent Chat</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Engage with our AI Agent to gain insights and guidance on your startup.</p>', unsafe_allow_html=True)

# Authentication Check
if 'user_id' not in session_state:
    st.warning("⚠️ Please log in or sign up first to access the AI Chat.")
    st.stop()

# Initialize chat history
if 'chat_history' not in session_state:
    session_state.chat_history = []

if 'user_input' not in session_state:
    session_state.user_input = ""

startup_info = main.startup_info(session_state.user_id)

# Function to handle user input
def send_message():
    user_input = session_state.user_input
    if user_input:
        with st.spinner("🤖 Thinking..."):
            response = main.agent(user_input, startup_info)
            session_state.chat_history.append({"user": user_input, "bot": response})
            session_state.user_input = ""  # Clear the input field

# Chat input
st.text_input("Type your message:", value=session_state.user_input, key="user_input", on_change=send_message, autocomplete="off")

# Display chat history
st.markdown("### 🗨️ Chat History")
for chat in session_state.chat_history:
    with st.container():
        st.markdown(f"<div class='chat-container'><span class='user-message'>**You:**</span> {chat['user']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-container'><span class='bot-message'>**Agent:**</span> {chat['bot']}</div>", unsafe_allow_html=True)
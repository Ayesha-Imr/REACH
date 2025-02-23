import streamlit as st
from backend import main
from streamlit import session_state

# Set up page
st.set_page_config(page_title="Login", page_icon="🔑", layout="centered")

# Custom Styling
st.markdown(
    """
    <style>
        .title {
            font-size: 36px;
            font-weight: bold;
            color: #2C3E50;
            text-align: center;
        }
        .subtitle {
            font-size: 18px;
            color: #555;
            text-align: center;
            margin-bottom: 20px;
        }
        .form-container {
            background-color: #f9f9f9;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            margin: 0 auto;
        }
        .button {
            width: 100%;
            background-color: #2C3E50;
            color: white;
            font-weight: bold;
            padding: 10px;
            border-radius: 5px;
        }
        .error, .success {
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Page Title - No extra divs, preventing blank spaces
st.markdown('<h1 class="title">🔑 Welcome Back</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Log in to access your REACH insights.</p>', unsafe_allow_html=True)

# Authentication Logic
if 'user_id' in session_state:
    st.info("✅ You are already logged in.")

else:
    with st.container():  # Ensuring only necessary content is displayed
        username = st.text_input("👤 Username", placeholder="Enter your username", autocomplete="off")
        password = st.text_input("🔑 Password", placeholder="Enter your password", type="password", autocomplete="off")

        if st.button("Log In", key="login", help="Click to access your account"):
            if username and password:
                user_id = main.login(username, password)
                if user_id:
                    st.success("✅ Login successful! Redirecting...", icon="🚀")
                    session_state.user_id = user_id
                    st.rerun()
                else:
                    st.error("❌ Incorrect username or password. Please try again.")
            else:
                st.error("⚠️ Please enter both username and password.")

st.markdown('<p style="text-align: center;">New to REACH? <a href="/SignUp" target="_self">Create an account</a></p>', unsafe_allow_html=True)

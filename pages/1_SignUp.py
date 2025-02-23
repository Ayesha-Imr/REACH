import streamlit as st
from backend import main
from streamlit import session_state

# Set up page
st.set_page_config(page_title="Sign Up", page_icon="🔐", layout="centered")

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

# Page Title - Removed any unnecessary blank elements
st.markdown('<h1 class="title">🔐 Create Your Account</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Join REACH and start unlocking powerful market insights.</p>', unsafe_allow_html=True)

# Authentication Logic
if 'user_id' in session_state:
    st.info("✅ You are already logged in.")

else:
    with st.container():  # Avoiding empty div issues
        username = st.text_input("👤 Username", placeholder="Choose a unique username", autocomplete="off")
        password = st.text_input("🔑 Password", placeholder="Create a strong password", type="password", autocomplete="off")

        if st.button("Sign Up", key="signup", help="Click to create your account"):
            if username and password:
                user_id = main.register(username, password)
                if user_id:
                    st.success("✅ Sign up successful! Redirecting...", icon="🎉")
                    session_state.user_id = user_id  
                    main.set_userid(user_id)  
                    st.switch_page("pages/3_DataUpload.py")
                else:
                    st.error("❌ Sign up failed. Username may already exist or there was an issue.")
            else:
                st.error("⚠️ Please enter both username and password.")

st.markdown('<p style="text-align: center;">Already have an account? <a href="/Login" target="_self">Log in here</a></p>', unsafe_allow_html=True)

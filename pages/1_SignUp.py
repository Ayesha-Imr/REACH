import streamlit as st
from backend import main
from streamlit import session_state

st.set_page_config(page_title="Sign Up", page_icon="🔐")

st.title("Sign Up")

if 'user_id' in session_state:
    st.info("You are already logged in.")

else:
    username = st.text_input("Username", autocomplete="off")
    password = st.text_input("Password", type="password", autocomplete="off")

    if st.button("Sign Up"):
        if username and password:
            user_id = main.register(username, password)
            if user_id:
                st.success("Sign up successful!")
                session_state.user_id = user_id
                st.switch_page("pages/3_DataUpload.py")
            else:
                st.error("Sign up failed. Please try again.")
        else:
            st.error("Please enter both username and password.")
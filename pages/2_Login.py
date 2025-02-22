import streamlit as st
from backend import main
from streamlit import session_state

st.set_page_config(page_title="Login", page_icon="🔑")

st.title("Login")

if 'user_id' in session_state:
    st.info("You are already logged in.")
else:
    username = st.text_input("Username", autocomplete="off")
    password = st.text_input("Password", type="password", autocomplete="off")

    if st.button("Log In"):
        if username and password:
            user_id = main.login(username, password)
            if user_id:
                st.success("Login successful!")
                session_state.user_id = user_id
                st.rerun()  
            else:
                st.error("Login failed. Please check your username and password.")
        else:
            st.error("Please enter both username and password.")
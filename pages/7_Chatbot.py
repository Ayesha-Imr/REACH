import streamlit as st
from backend import main
from streamlit import session_state

st.set_page_config(page_title="Chatbot", page_icon="🤖")

st.title("Chatbot")

if 'user_id' not in session_state:
    st.warning("Please log in or sign up first.")
else:
    st.write("This is the chatbot page where users can interact with an AI.")
    
    if 'chat_history' not in session_state:
        session_state.chat_history = []

    if 'user_input' not in session_state:
        session_state.user_input = ""

    startup_info = main.startup_info(session_state.user_id)

    def send_message():
        user_input = session_state.user_input
        if user_input:
            with st.spinner("Thinking..."):
                response = main.agent(user_input, startup_info)
                session_state.chat_history.append({"user": user_input, "bot": response})
                session_state.user_input = ""  # Clear the input field

    user_input = st.text_input("You:", value=session_state.user_input, key="user_input", on_change=send_message, autocomplete="off")
    
    for chat in session_state.chat_history:
        st.write(f"**You:** {chat['user']}")
        st.write(f"**Agent:** {chat['bot']}")
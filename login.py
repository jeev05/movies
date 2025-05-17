import streamlit as st

users = {"alice": "wonderland123", "bob": "builder456"}

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
        else:
            st.error("Invalid username or password")
else:
    st.title("Home Page")
    st.write(f"Welcome, **{st.session_state.username}**!")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""

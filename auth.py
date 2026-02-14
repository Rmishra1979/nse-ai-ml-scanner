
import streamlit as st

def login_screen():
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if username == "admin" and password == "admin123":
        st.sidebar.success("Logged in")
        return username
    return None

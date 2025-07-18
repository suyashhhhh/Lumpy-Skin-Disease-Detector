import streamlit as st
import hashlib
import logging
from src.database import add_user, login_user

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def auth_menu():
    st.subheader("🔐 Authentication")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    menu = ["Login", "Sign Up"]
    choice = st.radio("Select Option", menu)

    if choice == "Login":
        if st.button("Login"):
            hashed_pw = hash_password(password)
            user = login_user(username, hashed_pw)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.page = "dashboard"
                logging.info(f"User logged in: {username}")
                st.rerun()  # ✅ Fix: Forces Streamlit to reload properly
            else:
                st.error("Invalid username or password")

    elif choice == "Sign Up":
        if st.button("Create Account"):
            try:
                hashed_pw = hash_password(password)
                add_user(username, hashed_pw)
                st.success("Account created! You can now log in.")
                logging.info(f"New user registered: {username}")
            except Exception as e:
                st.error("Error creating account.")
                logging.error(f"Signup error: {e}")

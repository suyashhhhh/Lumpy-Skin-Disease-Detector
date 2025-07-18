# 🔁 Set page config MUST be first Streamlit command
import streamlit as st
st.set_page_config(page_title="Cow Health App", page_icon="🐄", layout="wide")

# ✅ Now safely import everything else
import logging
from src.database import create_usertable
from src.auth import auth_menu
from src.dashboard import dashboard

# -------------------- Setup Logging --------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def main():
    st.markdown("<h1 style='text-align: center;'>🐄 Cow Health Detection App</h1>", unsafe_allow_html=True)
    create_usertable()

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'page' not in st.session_state:
        st.session_state.page = "auth"

    # 🔒 Minimal Sidebar
    with st.sidebar:
        st.markdown("### 📌 Powered by")
        st.markdown("""
        - **Technology**: Python, TensorFlow, Streamlit  
        - **Model**: MobileNetV2  
        - **Database**: SQLite  
        - **Purpose**: Detect Lumpy Skin Disease in Cows using Images  
        - **Security**: Hashed passwords, User Login System  
        """)

    if st.session_state.logged_in and st.session_state.page == "dashboard":
        dashboard()
    else:
        auth_menu()

    add_footer()

from src.footer import add_footer

if __name__ == "__main__":
    main()

# src/footer.py
import streamlit as st

def add_footer():
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            color: #555;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            z-index: 9999;
            box-shadow: 0 -1px 5px rgba(0, 0, 0, 0.1);
        }
        </style>

        <div class="footer">
            Designed by <b>Suyash & Team</b> 🚀
        </div>
        """,
        unsafe_allow_html=True
    )

import streamlit as st
import logging
import time
from PIL import Image, UnidentifiedImageError
from src.model import predict_image
from src.database import save_prediction, get_prediction_history

# --- Custom CSS ---
st.markdown("""
    <style>
    /* Hide Streamlit default UI */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}

    /* Center the content */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 900px;
        margin: auto;
    }

    /* Styled Buttons */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        padding: 10px 24px;
        font-size: 16px;
        transition: all 0.3s ease-in-out;
        display: block;
        margin: auto;
    }

    .stButton>button:hover {
        background-color: #45a049;
        transform: scale(1.02);
    }

    .stFileUploader {
        border: 2px dashed #aaa;
        background-color: #222;
        padding: 20px;
        border-radius: 10px;
        color: white;
    }

    img {
        border-radius: 10px;
        border: 2px solid #555;
        display: block;
        margin: auto;
    }

    .element-container {
        animation: fadeIn 1.2s ease-in;
    }

    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }
    </style>
""", unsafe_allow_html=True)

# --- Prediction Message Generator ---
def interpret_prediction(result, confidence):
    result = result.strip().lower()

    if result == "lumpy cow":
        if confidence >= 90:
            return f"🚨 Critical case of Lumpy Skin Disease ({confidence:.2f}%). Immediate veterinary care is needed!"
        elif confidence >= 75:
            return f"⚠️ High likelihood of Lumpy Skin Disease ({confidence:.2f}%). Please consult a vet soon."
        elif confidence >= 60:
            return f"🧐 Possible symptoms of Lumpy Skin Disease ({confidence:.2f}%). Monitoring and early action advised."
        elif confidence >= 40:
            return f"🤔 Slight chance of Lumpy Skin Disease ({confidence:.2f}%). Consider checking with a vet."
        else:
            return f"🙂 Very low signs of Lumpy Skin Disease ({confidence:.2f}%). Likely healthy, but stay alert."
    
    elif result == "healthy cow":
        if confidence >= 90:
            return f"✅ The cow appears perfectly healthy ({confidence:.2f}%). No concerns!"
        elif confidence >= 75:
            return f"😄 The cow shows strong signs of good health ({confidence:.2f}%)."
        elif confidence >= 60:
            return f"🙂 The cow seems healthy ({confidence:.2f}%). Periodic checks are still a good idea."
        elif confidence >= 40:
            return f"🤔 Mostly healthy appearance ({confidence:.2f}%). Keep an eye on symptoms."
        else:
            return f"⚠️ Low confidence in classification ({confidence:.2f}%). Consider manual inspection or a second test."

    else:
        return f"⚠️ Unexpected prediction: {result} ({confidence:.2f}%). Please re-upload or check model output."

# --- Main Dashboard Function ---
def dashboard():
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({'logged_in': False, 'username': '', 'page': 'login'}))

    st.markdown(f"<h3 style='text-align: center;'>👋 Welcome, <span style='color:#FF4B4B'>{st.session_state.username}</span></h3>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>🩺 Cow Disease Detection Dashboard</h4>", unsafe_allow_html=True)
    st.markdown("---")

    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            uploaded_file = st.file_uploader("Upload a cow image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

    if uploaded_file:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(uploaded_file, caption="Preview Image", width=450)
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            if st.button("Upload & Predict"):
                with st.spinner("Analyzing image..."):
                    time.sleep(1.5)
                try:
                    img = Image.open(uploaded_file).convert("RGB")
                    result, confidence = predict_image(img)
                    filename = uploaded_file.name

                    st.success(f"🧪 Prediction: **{result} ({confidence:.2f}%)**")
                    st.info(interpret_prediction(result, confidence))

                    save_prediction(st.session_state.username, filename, f"{result} ({confidence:.2f}%)")
                    logging.info(f"Prediction by {st.session_state.username}: {filename} - {result} ({confidence:.2f}%)")

                except UnidentifiedImageError:
                    st.warning("⚠️ Could not identify image file.")
                    logging.warning("Unidentified image error.")
                except Exception as e:
                    st.warning(f"⚠️ Error: {e}")
                    logging.error(f"Prediction error: {e}")

    with st.expander("📜 View Past Predictions"):
        history = get_prediction_history(st.session_state.username)
        if history:
            st.write("### Your Prediction History:")
            st.dataframe([{"Filename": row[0], "Result": row[1]} for row in history])
        else:
            st.info("No predictions found.")


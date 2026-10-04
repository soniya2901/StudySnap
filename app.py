import os
import streamlit as st
import time
from PIL import Image
from google import genai

# Page settings
st.set_page_config(
    page_title="StudySnap",
    page_icon="📚",
    layout="centered"
)

# Gemini setup
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key not found. Please set GEMINI_API_KEY.")
    st.stop()

client = genai.Client(api_key=api_key)

# App title
st.title("📚 StudySnap")
st.subheader("🤖 AI Vision ChatBot for Students")

st.write(
    "Upload your study material and ask questions about it."
)

# Upload image
uploaded_image = st.file_uploader(
    "📷 Upload your study image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_image:
    image = Image.open(uploaded_image)

    st.image(
        image,
        caption="Your uploaded study material",
        use_container_width=True
    )

    question = st.text_input(
        "💬 Ask a question about this image:"
    )

    if question:
      with st.spinner("🤖 Studying your image..."):
        try:
            for attempt in range(3):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=[
                            image,
                            question
                        ]
                    )
                    break
                except Exception as e:
                    if attempt == 2:
                        raise e
                    time.sleep(2 ** attempt)

            st.subheader("✨ StudySnap Answer")
            st.write(response.text)

        except Exception as e:
            st.error(f"Something went wrong: {e}")
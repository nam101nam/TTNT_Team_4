import streamlit as st
import requests
from PIL import Image
import io

# The new, correct API endpoint
API_URL = "http://localhost:8000/api/predict"

st.set_page_config(
    page_title="Human Presence Detector",
    page_icon="👤",
    layout="centered",
)

st.title("👤 Human Presence Detector")
st.write("Upload an image to see if the model detects a person.")
st.write("---")

# File uploader
uploaded_file = st.file_uploader(
    label="Choose an image (PNG/JPG/JPEG)",
    type=["png", "jpg", "jpeg"]
)

# When a file is uploaded, display a preview and the Predict button
if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Your uploaded image", use_column_width=True)

        if st.button("Predict"):
            with st.spinner("Sending image to the API and waiting for the result..."):
                
                # Prepare the file to be sent in the request
                buffer = io.BytesIO()
                image.save(buffer, format='JPEG')
                buffer.seek(0)
                
                files = {
                    "file": (uploaded_file.name, buffer, "image/jpeg")
                }

                try:
                    # Send the request to the API
                    response = requests.post(API_URL, files=files)
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to the API: {e}")
                else:
                    if response.status_code == 200:
                        data = response.json()
                        prediction = data.get("prediction", "Unknown")
                        confidence = data.get("confidence", 0.0)
                        st.success(f"Prediction: **{prediction.upper()}** (Confidence: {confidence:.2f})")
                    else:
                        try:
                            error_msg = response.json().get("detail", response.text)
                        except Exception:
                            error_msg = response.text
                        st.error(f"API returned an error (status {response.status_code}): {error_msg}")
    except Exception as e:
        st.error(f"An error occurred while processing the image: {e}")
else:
    st.info("Please upload an image file to make a prediction.")

st.write("---")
st.markdown(
    "This model has been trained to distinguish between images that contain a person and those that do not."
)

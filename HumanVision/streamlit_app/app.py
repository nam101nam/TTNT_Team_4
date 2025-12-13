import streamlit as st
import requests
from PIL import Image
import io

# API URL
API_URL = "http://localhost:8000/api/predict"

st.set_page_config(
    page_title="Human Presence Detector",
    page_icon="👤",
    layout="wide",
)
# --- PHẦN TIÊU ĐỀ ĐÃ ĐƯỢC CĂN GIỮA ---
st.markdown(
    """
    <div style='text-align: center;'>
        <h1>👤 Human Presence Detector</h1>
        <p style='font-size: 18px;'>Upload an image to see if the model detects a person.</p>
    </div>
    """,
    unsafe_allow_html=True
)
st.write("---")

col1, col2 = st.columns([1, 1], gap="medium")

# --- CỘT TRÁI: UPLOAD VÀ HIỂN THỊ ẢNH ---
with col1:
    st.subheader("1. Input Image")
    uploaded_file = st.file_uploader(
        label="Choose an image (PNG/JPG/JPEG)",
        type=["png", "jpg", "jpeg"]
    )

    image = None

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file).convert("RGB")

            # --- SỬA ĐỔI ĐỂ CĂN GIỮA ---
            # Tạo 3 cột con bên trong cột trái theo tỷ lệ [1, 3, 1]
            # Cột ở giữa (số 3) sẽ rộng nhất để chứa ảnh, 2 cột bên cạnh làm khoảng đệm
            c1, c2, c3 = st.columns([1, 3, 1])

            with c2:
                # Đặt ảnh vào cột giữa -> Ảnh sẽ nằm giữa
                st.image(image, caption="Your uploaded image Preview", width=350)
            # ---------------------------

        except Exception as e:
            st.error(f"Error opening image: {e}")

# --- CỘT PHẢI: NÚT BẤM VÀ KẾT QUẢ ---
with col2:
    st.subheader("2. Prediction Result")

    if image is not None:
        st.write("Image loaded successfully. Click the button below to analyze.")

        if st.button("Predict", type="primary", use_container_width=True):

            with st.spinner("Analyzing image..."):
                buffer = io.BytesIO()
                image.save(buffer, format='JPEG')
                buffer.seek(0)

                files = {
                    "file": (uploaded_file.name, buffer, "image/jpeg")
                }

                try:
                    response = requests.post(API_URL, files=files)
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to the API: {e}")
                else:
                    if response.status_code == 200:
                        data = response.json()
                        prediction = data.get("prediction", "Unknown")
                        confidence = data.get("confidence", 0.0)

                        if prediction == "person":
                            st.success(f"### RESULT: PERSON")
                            st.metric(label="Confidence", value=f"{confidence:.2%}")
                        else:
                            st.warning(f"### RESULT: NO PERSON")
                            st.metric(label="Confidence", value=f"{confidence:.2%}")

                    else:
                        try:
                            error_msg = response.json().get("detail", response.text)
                        except Exception:
                            error_msg = response.text
                        st.error(f"API Error ({response.status_code}): {error_msg}")
    else:
        st.info("👈 Please upload an image in the left panel to start.")

st.write("---")
st.caption("This model has been trained to distinguish between images that contain a person and those that do not.")
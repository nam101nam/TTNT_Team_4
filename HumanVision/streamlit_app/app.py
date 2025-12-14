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


# --- HÀM HỖ TRỢ: CẮT ẢNH VUÔNG ---
def crop_center_square(pil_img):
    img_width, img_height = pil_img.size
    min_dim = min(img_width, img_height)
    left = (img_width - min_dim) / 2
    top = (img_height - min_dim) / 2
    right = (img_width + min_dim) / 2
    bottom = (img_height + min_dim) / 2
    return pil_img.crop((left, top, right, bottom))


# --- TIÊU ĐỀ ---
st.markdown(
    """
    <div style='text-align: center;'>
        <h1>👤 Human Presence Detector</h1>
        <p style='font-size: 18px;'>Upload an image or take a photo to see if the model detects a person.</p>
    </div>
    """,
    unsafe_allow_html=True
)
st.write("---")

# --- BỐ CỤC CHÍNH: TRÁI (2 phần) - PHẢI (1 phần) ---
# Tăng kích thước cột trái lên 2 để chứa đủ (Input + Preview)
main_col1, main_col2 = st.columns([2, 1], gap="large")

# Biến toàn cục
image = None
final_filename = "image.jpg"

# ==========================================
# CỘT TRÁI: INPUT VÀ PREVIEW (NẰM NGANG NHAU)
# ==========================================
with main_col1:
    st.subheader("1. Input & Preview")

    # Tạo 2 cột con bên trong cột trái
    input_col, preview_col = st.columns(2, gap="medium")

    # --- Cột con 1: Các nút nhập liệu (Upload/Camera) ---
    with input_col:
        st.markdown("**Step 1: Choose Image**")
        uploaded_file = st.file_uploader(
            label="Upload Image",
            type=["png", "jpg", "jpeg"],
            label_visibility="collapsed"  # Ẩn label cho gọn
        )

        st.write("--- OR ---")

        enable_camera = st.checkbox("📸 Use Camera")
        camera_file = None
        if enable_camera:
            camera_file = st.camera_input("Take Photo", label_visibility="collapsed")

    # --- XỬ LÝ ẢNH ---
    input_source = None
    if camera_file is not None:
        input_source = camera_file
        final_filename = "camera_capture.jpg"
    elif uploaded_file is not None:
        input_source = uploaded_file
        final_filename = uploaded_file.name

    if input_source is not None:
        try:
            raw_image = Image.open(input_source).convert("RGB")
            if input_source == camera_file:
                image = crop_center_square(raw_image)
            else:
                image = raw_image
        except Exception as e:
            st.error(f"Error: {e}")

    # --- Cột con 2: Hiển thị Preview ---
    with preview_col:
        st.markdown("**Step 2: Preview**")
        if image is not None:
            # Hiển thị ảnh đã chọn/chụp
            st.image(image, caption=f"Ready ({image.size[0]}x{image.size[1]})", use_container_width=True)
        else:
            # Hiển thị khung chờ khi chưa có ảnh
            st.info("👈 Select an image on the left to see preview here.")

# ==========================================
# CỘT PHẢI: KẾT QUẢ
# ==========================================
with main_col2:
    st.subheader("2. Result")

    if image is not None:
        st.write("Ready to analyze.")

        # Nút Predict
        if st.button("Predict Result", type="primary", use_container_width=True):

            with st.spinner("Processing..."):
                buffer = io.BytesIO()
                image.save(buffer, format='JPEG')
                buffer.seek(0)
                files = {"file": (final_filename, buffer, "image/jpeg")}

                try:
                    response = requests.post(API_URL, files=files)
                except requests.exceptions.RequestException as e:
                    st.error(f"Connection Error: {e}")
                else:
                    if response.status_code == 200:
                        data = response.json()
                        prediction = data.get("prediction", "Unknown")
                        confidence = data.get("confidence", 0.0)

                        st.write("---")
                        if prediction == "person":
                            st.success(f"### 🧍 PERSON")
                            st.metric("Confidence", f"{confidence:.2%}")
                        else:
                            st.warning(f"### 🚫 NO PERSON")
                            st.metric("Confidence", f"{confidence:.2%}")
                    else:
                        st.error("API Error")
    else:
        st.write("Waiting for image input...")

st.write("---")
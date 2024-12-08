# pip install paddleocr
# pip install paddlepaddle
# streamlit run ocr_jpn.py --server.maxUploadSize 1000

import streamlit as st
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import pytesseract
from streamlit_drawable_canvas import st_canvas
import numpy as np

# Streamlit App Configuration
st.set_page_config(page_title="OCR App with paddle", layout="wide")

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang="japan")  # Enable Japanese OCR with orientation detection


# Title
st.title("📄 OCR App with paddle")
st.write("Upload a JPEG image, select a region, and perform OCR on that region. Selecting a new region cancels the previous one.")

# File Uploader
uploaded_file = st.file_uploader("Drag and drop a JPEG file here:", type=["jpg", "jpeg"])

# Initialize session state variables
if 'ocr_result' not in st.session_state:
    st.session_state.ocr_result = ""
if 'canvas_result' not in st.session_state:
    st.session_state.canvas_result = None

if uploaded_file is not None:
    # Open the image
    image = Image.open(uploaded_file)

    # Display the image in the left column
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Uploaded Image")

        # Streamlit-Drawable-Canvas for selecting a region
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)",  # Transparent red
            stroke_width=3,
            background_image=image,
            update_streamlit=True,
            height=image.size[1],
            width=image.size[0],
            drawing_mode="rect",  # Rectangle mode
            key="canvas",
            # Reset canvas on new selection by clearing the previous state
        )

    # Check for rectangle selection and perform OCR
    with col2:
        if canvas_result.json_data is not None:
            objects = canvas_result.json_data["objects"]
            if objects:
                # Get the latest drawn rectangle (the most recent one)
                rect_coords = objects[-1]  # Use the most recent rectangle
                x, y = rect_coords["left"], rect_coords["top"]
                w, h = rect_coords["width"], rect_coords["height"]

                # Crop the image to the selected area
                cropped_image = image.crop((x, y, x + w, y + h))

                st.subheader("Cropped Region")
                st.image(cropped_image, caption="Selected Region", use_column_width=False)

                # Convert cropped PIL image to numpy array for PaddleOCR
                cropped_image_np = np.array(cropped_image)

                # Perform OCR on the cropped region
                with st.spinner("Performing OCR on the selected region..."):
                    # Perform OCR on the cropped region with vertical text handling
                    # custom_config = r'--psm 5 -c textord_vertical_text=1'
                    # extracted_text = pytesseract.image_to_string(cropped_image, lang="jpn", config=custom_config)

                    results = ocr.ocr(cropped_image_np, det=True, rec=True)

                    # Extract and display the recognized text
                    extracted_text = "\n".join([line[1][0] for line in results[0]])
                    st.text_area("Extracted Text", extracted_text)

                # Update OCR result in session state
                st.session_state.ocr_result = extracted_text

                # Reset the canvas state after drawing the rectangle
                st.session_state.canvas_result = canvas_result

                st.subheader("Extracted Text")
                st.text_area("OCR Result", value=st.session_state.ocr_result, height=300)
            else:
                st.info("Draw a rectangle on the left image to select an OCR region.")
        else:
            st.info("Draw a rectangle on the left image to select an OCR region.")
else:
    st.info("Please upload a JPEG image to get started.")

# Footer
st.write("Powered by [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and [Streamlit Drawable Canvas](https://github.com/andfanilo/streamlit-drawable-canvas).")


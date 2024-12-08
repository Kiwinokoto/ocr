# pip install easyocr
# pip install streamlit
# pip install streamlit-drawable-canvas
from PIL import Image
import streamlit as st
import numpy as np
import easyocr
from streamlit_drawable_canvas import st_canvas

# Streamlit App Configuration
st.set_page_config(page_title="OCR App with ez", layout="wide")

# Initialize EasyOCR reader
reader = easyocr.Reader(["ja"], gpu=False)  # 'ja' for Japanese, GPU can be enabled if available

# Title
st.title("📄 OCR App with ez")
st.write("Upload a JPEG image, select a region, and perform OCR on that region. Selecting a new region cancels the previous one.")

# File Uploader
uploaded_file = st.file_uploader("Drag and drop a JPEG file here:", type=["jpg", "jpeg", "png"])

# Initialize session state variables

if uploaded_file is not None:
    # Open the image
    image = Image.open(uploaded_file)

    # Display the image in the left column
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Uploaded Image")

        # Streamlit-Drawable-Canvas for selecting a region
        canvas_result = st_canvas(
            fill_color="rgba(255, 100, 100, 0.6)",  # Transparent pastel red
            stroke_width=2,
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

                # Convert cropped PIL image to numpy array for EasyOCR
                cropped_image_np = np.array(cropped_image)

                # Perform OCR on the cropped region
                with st.spinner("Performing OCR on the selected region..."):
                    results = reader.readtext(cropped_image_np)

                    # Extract and display the recognized text
                    extracted_text = "\n".join([line[1] for line in results])
                    st.text_area("Extracted Text", extracted_text)
            else:
                st.info("Draw a rectangle on the left image to select an OCR region.")
        else:
            st.info("Draw a rectangle on the left image to select an OCR region.")
else:
    st.info("Please upload a JPEG image to get started.")

# Footer
st.write("Powered by [EasyOCR](https://github.com/JaidedAI/EasyOCR) and [Streamlit Drawable Canvas](https://github.com/andfanilo/streamlit-drawable-canvas).")

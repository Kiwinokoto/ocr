# About : 

# env
# conda create -n env_prompt python pip requests numpy pandas pytest gdown streamlit PyPDF2 pycryptodome pdf2image
# openai tiktoken pytesseract tesseract pillow transformers langchain poppler
# au final not sure i need openai and tiktoken here
# best solution for price, speed and confidentiality would pbbly be local model, but
# my hardware is limited, and streamlit has a limited cache capacity -> free huggingface api better for now
# conda env export > environment.yml


# librairies
import streamlit as st
from PyPDF2 import PdfReader
# from pdf2image import convert_from_path
# from pytesseract import image_to_string
import pytesseract
from PIL import Image
import os
from typing import List
import re
from transformers import pipeline
import requests
import time
from huggingface_hub import InferenceApi

st.set_page_config(page_title="OCR App", layout='wide')


# File Uploader
uploaded_file = st.file_uploader("Drag and drop a JPEG file here:", type=["jpg", "jpeg"])

# Process the uploaded image
if uploaded_file is not None:
    # Open the image using PIL
    image = Image.open(uploaded_file)

    # Split the layout into two columns
    col1, col2 = st.columns(2)

    # Display the image in the left column
    with col1:
        st.subheader("Uploaded Image")
        st.image(image, caption="Uploaded Image", use_column_width=True)

    # Perform OCR
    with st.spinner("Performing OCR..."):
        extracted_text = pytesseract.image_to_string(image, lang="eng")  # Change 'eng' to desired languages

    # Display the extracted text in the right column
    with col2:
        st.subheader("Extracted Text")
        st.text_area("OCR Result", value=extracted_text, height=600)
else:
    st.info("Please upload a JPEG image to get started.")

# Footer
st.write("Powered by [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and Streamlit.")



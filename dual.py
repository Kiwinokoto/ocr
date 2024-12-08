import streamlit as st
from PIL import Image

# Dynamically set the file upload size
# streamlit run dual.py --server.maxUploadSize 1000


# Set the title of the app
st.title("Book Image Organizer")

# Input text for the book name
book_name = st.text_input("Enter the name of the book:")

if book_name:
    st.markdown(f"### Upload images for the book: **{book_name}**")
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Drag and Drop Area 1")
        uploaded_files_col1 = st.file_uploader(
            "Upload images for Column 1",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
            key="col1"
        )
        if uploaded_files_col1:
            # Sort the files by their names
            sorted_files_col1 = sorted(uploaded_files_col1, key=lambda x: x.name)
            
            st.markdown("### First 10 Uploaded Images (Sorted by Name):")
            for file in sorted_files_col1[:10]:  # Display only the first 10 sorted files
                image = Image.open(file)
                st.image(image, caption=file.name, use_column_width=True)
            if len(sorted_files_col1) > 10:
                st.write(f"...and {len(sorted_files_col1) - 10} more images.")

    with col2:
        st.header("Drag and Drop Area 2")
        uploaded_files_col2 = st.file_uploader(
            "Upload images for Column 2",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
            key="col2"
        )
        if uploaded_files_col2:
            # Sort the files by their names
            sorted_files_col2 = sorted(uploaded_files_col2, key=lambda x: x.name)
            
            st.markdown("### First 10 Uploaded Images (Sorted by Name):")
            for file in sorted_files_col2[:10]:  # Display only the first 10 sorted files
                image = Image.open(file)
                st.image(image, caption=file.name, use_column_width=True)
            if len(sorted_files_col2) > 10:
                st.write(f"...and {len(sorted_files_col2) - 10} more images.")


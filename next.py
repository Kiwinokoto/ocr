import streamlit as st
from PIL import Image

# Function to reset the index in session state
def reset_index():
    st.session_state.start_idx_col1 = 0
    st.session_state.start_idx_col2 = 0

# Initialize session state for both columns
if "start_idx_col1" not in st.session_state:
    st.session_state.start_idx_col1 = 0
if "start_idx_col2" not in st.session_state:
    st.session_state.start_idx_col2 = 0

st.title("Book Image Organizer")

book_name = st.text_input("Enter the name of the book:", on_change=reset_index)

if book_name:
    st.markdown(f"### Upload images for the book: **{book_name}**")
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
            
            # Display images based on the current index
            start = st.session_state.start_idx_col1
            end = start + 10
            st.markdown(f"### Showing images {start + 1} to {min(end, len(sorted_files_col1))}")
            for file in sorted_files_col1[start:end]:
                image = Image.open(file)
                st.image(image, caption=file.name, use_column_width=True)
            
            # Next button
            if st.button("Next (Column 1)", key="next_col1"):
                if end < len(sorted_files_col1):
                    st.session_state.start_idx_col1 += 10

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
            
            # Display images based on the current index
            start = st.session_state.start_idx_col2
            end = start + 10
            st.markdown(f"### Showing images {start + 1} to {min(end, len(sorted_files_col2))}")
            for file in sorted_files_col2[start:end]:
                image = Image.open(file)
                st.image(image, caption=file.name, use_column_width=True)
            
            # Next button
            if st.button("Next (Column 2)", key="next_col2"):
                if end < len(sorted_files_col2):
                    st.session_state.start_idx_col2 += 10


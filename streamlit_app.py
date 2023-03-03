import streamlit as st
import cv2
import numpy as np

st.title("Image Watermark Removal and Cropping App")

# Function to remove watermark from image
def remove_watermark(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Thresholding to create a mask of the watermark
    ret, mask = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)
    # Invert the mask
    mask_inv = cv2.bitwise_not(mask)
    # Apply the mask to the image to remove the watermark
    result = cv2.bitwise_and(image, image, mask=mask_inv)
    return result

# Function to crop image to 16:9 or 4:3 aspect ratio
def crop_image(image, aspect_ratio):
    height, width = image.shape[:2]
    if aspect_ratio == "16:9":
        new_width = int(height * 16 / 9)
        if new_width > width:
            new_width = width
            new_height = int(width * 9 / 16)
            start_x = 0
            start_y = int((height - new_height) / 2)
        else:
            new_height = height
            start_x = int((width - new_width) / 2)
            start_y = 0
    elif aspect_ratio == "4:3":
        new_width = int(height * 4 / 3)
        if new_width > width:
            new_width = width
            new_height = int(width * 3 / 4)
            start_x = 0
            start_y = int((height - new_height) / 2)
        else:
            new_height = height
            start_x = int((width - new_width) / 2)
            start_y = 0
    cropped = image[start_y:start_y+new_height, start_x:start_x+new_width]
    return cropped

# Sidebar for selecting aspect ratio
aspect_ratio = st.sidebar.selectbox("Select aspect ratio", ["16:9", "4:3"])

# File uploader for uploading image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read image from uploaded file
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    # Remove watermark from image
    image_without_watermark = remove_watermark(image)
    # Display original and processed images side by side
    col1, col2 = st.beta_columns(2)
    col1.header("Original Image")
    col1.image(image, use_column_width=True)
    col2.header("Processed Image")
    col2.image(image_without_watermark, use_column_width=True)
    # Crop image to selected aspect ratio
    cropped_image = crop_image(image_without_watermark, aspect_ratio)
    # Download button for processed image
    st.download_button(
        label="Download processed image",
        data=cropped_image,
        file_name="processed_image.png",
        mime="image/png"
    )

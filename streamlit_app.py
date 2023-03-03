import streamlit as st
import cv2
import numpy as np
from PIL import Image
import requests


# Helper function to remove watermark from image
def remove_watermark(image):
    # TODO: Implement watermark removal algorithm
    return image


# Helper function to crop image to a specific aspect ratio
def crop_image(image, aspect_ratio):
    # Get current image dimensions
    height, width, _ = image.shape

    # Calculate target dimensions based on aspect ratio
    target_height = height
    target_width = width
    if aspect_ratio == '16:9':
        target_width = round(height * 16 / 9)
    elif aspect_ratio == '4:3':
        target_width = round(height * 4 / 3)

    # Calculate crop offsets
    x_offset = round((width - target_width) / 2)
    y_offset = 0

    # Crop image
    cropped_image = image[y_offset:y_offset+target_height, x_offset:x_offset+target_width]

    return cropped_image


# Helper function to enhance image clarity
def enhance_clarity(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply bilateral filter to smooth out noise while preserving edges
    blurred = cv2.bilateralFilter(gray, 11, 17, 17)

    # Apply unsharp mask to enhance edges
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpened = cv2.filter2D(blurred, -1, kernel)

    # Convert image back to RGB format
    enhanced_image = cv2.cvtColor(sharpened, cv2.COLOR_GRAY2RGB)

    return enhanced_image


# Main function to process image
def process_image(image_url, aspect_ratio):
    # Load image from URL or file upload
    if image_url.startswith('http'):
        response = requests.get(image_url)
        image = np.array(Image.open(BytesIO(response.content)))
    else:
        image = np.array(Image.open(image_url))

    # Remove watermark
    image = remove_watermark(image)

    # Crop image to aspect ratio
    image = crop_image(image, aspect_ratio)

    # Enhance image clarity
    image = enhance_clarity(image)

    # Convert image back to PIL format
    processed_image = Image.fromarray(image)

    return processed_image


# Streamlit app code
st.title('内部 App-自动化img')
st.write('功能反馈微信: Allin6118')

# Get user input
image_url = st.text_input('Enter image URL:')
aspect_ratio = st.selectbox('Select aspect ratio:', ['16:9', '4:3'])
button_clicked = st.button('Process Image')

# Process image when button is clicked
if button_clicked:
    try:
        processed_image = process_image(image_url, aspect_ratio)
        st.image(processed_image, use_column_width=True)
        st.download_button('Download Image', data=processed_image.tobytes(), file_name='processed_image.jpg', mime='image/jpeg')
    except Exception as e:
        st.error(str(e))

'''
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import requests
from io import BytesIO
from augly.image import overlay_onto_solid_color_background


# Helper function to remove watermark from image
def remove_watermark(image):
    # TODO: Implement watermark removal algorithm
    return image


# Helper function to crop image to a specific aspect ratio
def crop_image(image, aspect_ratio):
    # Get current image dimensions
    height, width, _ = image.shape

    # Calculate target dimensions based on aspect ratio
    target_height = height
    target_width = width
    if aspect_ratio == '16:9':
        target_width = round(height * 16 / 9)
    elif aspect_ratio == '4:3':
        target_width = round(height * 4 / 3)

    # Calculate crop offsets
    x_offset = round((width - target_width) / 2)
    y_offset = 0

    # Crop image
    cropped_image = image[y_offset:y_offset+target_height, x_offset:x_offset+target_width]

    return cropped_image


# Helper function to enhance image clarity
def enhance_clarity(image):
    enhanced_image = overlay_onto_solid_color_background(image, color="white", alpha=0.2)
    return enhanced_image


# Main function to process image
def process_image(image_url, aspect_ratio):
    # Load image from URL or file upload
    if image_url.startswith('http'):
        response = requests.get(image_url)
        image = np.array(Image.open(BytesIO(response.content)))
    else:
        image = np.array(Image.open(image_url))

    # Remove watermark
    image = remove_watermark(image)

    # Crop image to aspect ratio
    image = crop_image(image, aspect_ratio)

    # Enhance image clarity
    image = enhance_clarity(image)

    # Convert image back to PIL format
    processed_image = Image.fromarray(image)

    return processed_image


# Streamlit app code
st.title('内部 App-自动化img')
st.write('功能反馈微信: Allin6118')

# Get user input
image_url = st.text_input('Enter image URL:')
aspect_ratio = st.selectbox('Select aspect ratio:', ['16:9', '4:3'])
button_clicked = st.button('Process Image')

# Process image when button is clicked
if button_clicked:
    try:
        processed_image = process_image(image_url, aspect_ratio)
        st.image(processed_image, use_column_width=True)
        st.download_button('Download Image', data=processed_image.tobytes(), file_name='processed_image.jpg', mime='image/jpeg')
    except Exception as e:
        st.error(str(e))
'''

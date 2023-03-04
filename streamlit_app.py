import streamlit as st
import requests
from PIL import Image

st.set_page_config(page_title="图片剪裁", layout="wide")

st.sidebar.title("选择图片")
url = st.sidebar.text_input("输入图片URL")
if url:
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    st.image(img, caption="原图", width=500)

    st.sidebar.title("选择剪裁比例")
    ratio = st.sidebar.radio("比例", ["原比例", "16:9", "4:3"])

    if ratio == "16:9":
        width, height = img.size
        if width * 9 > height * 16:
            new_width = height * 16 // 9
            left = (width - new_width) // 2
            right = left + new_width
            img = img.crop((left, 0, right, height))
        else:
            new_height = width * 9 // 16
            top = (height - new_height) // 2
            bottom = top + new_height
            img = img.crop((0, top, width, bottom))
    elif ratio == "4:3":
        width, height = img.size
        if width * 3 > height * 4:
            new_width = height * 4 // 3
            left = (width - new_width) // 2
            right = left + new_width
            img = img.crop((left, 0, right, height))
        else:
            new_height = width * 3 // 4
            top = (height - new_height) // 2
            bottom = top + new_height
            img = img.crop((0, top, width, bottom))

    st.image(img, caption="剪裁后的图片", width=500)

    st.sidebar.title("保存图片")
    file_name = st.sidebar.text_input("输入保存文件名", value="cropped_image.jpg")
    if st.sidebar.button("保存图片"):
        img.save(file_name)

else:
    st.sidebar.text("请输入图片URL")

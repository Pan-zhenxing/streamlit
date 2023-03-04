import streamlit as st
from PIL import Image
import requests
# 设置应用标题和页面布局
st.set_page_config(page_title="剪裁图片", layout="wide")

# 定义一个侧边栏，用于输入图片地址或上传本地图片
st.sidebar.title("上传或输入图片")
input_type = st.sidebar.radio("选择图片类型", ["URL", "本地文件"])
if input_type == "URL":
    url = st.sidebar.text_input("输入图片URL")
    if url:
        img = Image.open(requests.get(url, stream=True).raw)
else:
    uploaded_file = st.sidebar.file_uploader("上传图片", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        img = Image.open(uploaded_file)

# 如果有图片输入，则显示原图
if "img" in locals():
    st.image(img, caption="原图", width=500)

    # 定义一个侧边栏，用于进行剪裁
    st.sidebar.title("剪裁")
    ratio = st.sidebar.radio("选择图片比例", ["原比例", "16:9", "4:3"])

    # 如果用户选择了比例，则进行裁剪
    if ratio != "原比例":
        width, height = img.size
        if ratio == "16:9":
            new_height = width * 9 // 16
            if new_height > height:
                new_width = height * 16 // 9
                left = (width - new_width) // 2
                right = left + new_width
                img = img.crop((left, 0, right, height))
            else:
                top = (height - new_height) // 2
                bottom = top + new_height
                img = img.crop((0, top, width, bottom))
        elif ratio == "4:3":
            new_height = width * 3 // 4
            if new_height > height:
                new_width = height * 4 // 3
                left = (width - new_width) // 2
                right = left + new_width
                img = img.crop((left, 0, right, height))
            else:
                top = (height - new_height) // 2
                bottom = top + new_height
                img = img.crop((0, top, width, bottom))

    # 显示剪裁后的图片
    st.image(img, caption="剪裁后的图片", width=500)

    # 定义一个按钮，用于下载剪裁后的图片
    if st.button("下载图片"):
        st.download_button(
            label="下载图片",
            data=img,
            file_name="processed_image.jpg",
            mime="image/jpg",
        )

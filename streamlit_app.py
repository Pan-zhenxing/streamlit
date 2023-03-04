import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# 设置应用标题和页面布局
st.set_page_config(page_title="图片工具内存1.0", layout="wide")

# 定义一个侧边栏，用于输入图片地址或上传本地图片
st.sidebar.title("测试版本0.1")
st.sidebar.title("报错反馈微信：Allin6118")
st.sidebar.title("上传或输入图片")
input_type = st.sidebar.radio("选择图片类型", ["URL", "本地文件"])
if input_type == "URL":
    url = st.sidebar.text_input("输入图片URL")
    if url:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
else:
    uploaded_file = st.sidebar.file_uploader("上传图片", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        img = Image.open(uploaded_file)

# 如果有图片输入，则显示原图
if "img" in locals():
    st.image(img, caption="原图", width=500)

    # 定义一个侧边栏，用于选择剪切比例
    st.sidebar.title("剪切比例")
    ratio = st.sidebar.radio("选择图片比例", ["16:9", "4:3", "自定义"])

    # 如果用户选择了比例，则进行裁剪
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
    else:
        # 自定义比例，需要用户输入剪切的区域
        left = st.sidebar.number_input("左", 0, img.size[0], step=1)
        top = st.sidebar.number_input("上", 0, img.size[1], step=1)
        right = st.sidebar.number_input("右", 0, img.size[0], step=1)
        bottom = st.sidebar.number_input("下", 0, img.size[1], step=1)
        img = img.crop((left, top, right, bottom))

    # 显示处理后的图片和下载按钮
    st.image(img, caption="处理后的图片", width=500)
    st.download_button(
        label="下载图片",
        data=BytesIO(img.convert("RGB").tobytes()),
        file_name="processed_image.jpg",
        mime="image/jpg",
    )

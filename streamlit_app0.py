import streamlit as st
from PIL import Image, ImageFilter
import requests
from io import BytesIO

# 定义一个函数，用于下载处理后的图片
def download_img(img):
    bio = BytesIO()
    img.save(bio, format="JPEG")
    bio.seek(0)
    return bio.read()

# 设置应用标题和页面布局
st.set_page_config(page_title="去水印和提高图片品质", layout="wide")

# 定义一个侧边栏，用于输入图片地址或上传本地图片
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

    # 定义一个侧边栏，用于去水印和提高图片品质
    st.sidebar.title("图片处理")
    watermark = st.sidebar.checkbox("去除水印")
    #enhance = st.sidebar.checkbox("提高品质")
    ratio = st.sidebar.radio("选择图片比例", ["原比例", "16:9", "4:3"])

    # 如果用户选择去水印，则进行去水印处理
    if watermark:
        img_array = st.image_to_array(img)
        img_array[..., -1] = 255 - img_array[..., -1] # 将水印区域像素的alpha通道反转
        img = Image.fromarray(img_array)

    # 如果用户选择提高图片品质，则进行增强处理
    #if enhance:
    #    img = img.filter(ImageFilter.SHARPEN)

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
            img = img.crop
    # 定义一个按钮，用于下载处理后的图片
    if st.button("下载图片"):
        st.image(img, caption="处理后的图片", width=500)
        st.download_button(
            label="下载图片",
            data=download_img(img),
            file_name="processed_image.jpg",
            mime="image/jpg",
        )
 

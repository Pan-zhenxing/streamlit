import streamlit as st
from PIL import Image

st.title("图片剪切工具")

# 获取网络上的图片
url = st.text_input("请输入图片 URL")
if url:
    img = Image.open(requests.get(url, stream=True).raw)
    st.image(img, caption="原图", use_column_width=True)

    # 设置剪切比例
    ratio = st.sidebar.radio("选择图片比例", ["原比例", "16:9", "4:3"])
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

    # 显示剪切后的图片
    st.image(img, caption="剪切后的图片", use_column_width=True)

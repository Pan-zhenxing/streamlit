import streamlit as st
from PIL import Image, ImageEnhance

# 设置应用标题和说明
st.title("图片处理应用")
st.write("上传或输入图片地址，对图片进行处理并下载。")

# 创建上传图片功能
uploaded_file = st.file_uploader("上传本地图片", type=["jpg", "jpeg", "png"])

# 创建输入图片地址功能
image_url = st.text_input("输入图片地址")

# 如果有图片上传或地址输入，显示原图
if uploaded_file is not None:
    # 打开并显示原图
    image = Image.open(uploaded_file)
    st.image(image, caption="原图", use_column_width=True)

elif image_url != "":
    # 打开并显示原图
    image = Image.open(image_url)
    st.image(image, caption="原图", use_column_width=True)

# 创建去除水印功能
if st.button("去除水印"):
    # 获取原图并创建副本
    new_image = image.copy()
    
    # 获取涂抹去除水印
    edited_image = st.image(new_image, caption="去除水印", use_column_width=True, 
                            width=int(new_image.width/2), height=int(new_image.height/2))
    draw = ImageDraw.Draw(new_image)
    edited = False
    
    # 监听鼠标事件
    while edited_image.image_data is not None:
        # 获取鼠标位置
        event = edited_image.get_events()[0]
        x, y = event.x, event.y
        
        if event.type == "MouseDown":
            edited = True
        
        # 如果涂抹，将鼠标位置为中心，半径为10的区域填充白色
        if edited and event.type == "MouseMove":
            draw.rectangle((x-10, y-10, x+10, y+10), fill=(255, 255, 255))
            edited_image.image(new_image)
        
        if event.type == "MouseUp":
            edited = False

# 创建裁剪功能
if st.button("裁剪"):
    # 获取原图并创建副本
    new_image = image.copy()
    
    # 计算新图像的大小
    ratio = st.selectbox("选择比例", options=["16:9", "4:3"])
    if ratio == "16:9":
        new_width = int(new_image.height * 16 / 9)
        if new_width > new_image.width:
            new_width = new_image.width
            new_height = int(new_width * 9 / 16)
        else:
            new_height = new_image.height
    else:
        new_width = int(new_image.height * 4 / 3)
        if new_width > new_image.width:
            new_width = new_image.width
            new_height = int(new_width * 3 / 4)
        else:
            new_height = new_image.height
    
    # 裁剪图像并显示
    new_image = new_image.crop((0, 0, new_width, new_height))
    st.image(new_image, caption="裁剪", use_column_width=True)

# 创建提高图片品质功能
if st.button("提高品质"):
    # 获取原图并创建副本
    new_image = image.copy()
    
    # 提
    enhancer = ImageEnhance.Sharpness(new_image)
    enhance_factor = st.slider("选择增强度", min_value=1, max_value=10, step=1)
    new_image = enhancer.enhance(enhance_factor)

    # 显示增强后的图像
    st.image(new_image, caption="增强", use_column_width=True)
    if st.button("下载"):
        # 下载修改后的图像
        st.download_button("下载图片", data=new_image, file_name="processed_image.jpg", mime="image/jpeg")

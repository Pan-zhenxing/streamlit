import os
os.system('pip install speech_recognition')
'''import streamlit as st
import speech_recognition as sr
from gpt3 import GPT3
from playsound import playsound

#设置API_KEY
API_KEY = os.getenv('APIKEY')

# 前台显示部分
st.title('在线聊天机器人')
st.write('请单击**[开始]**开始聊天。')

# 按钮点击事件
if st.button('开始'):
    # 初始化语音识别对象
    r = sr.Recognizer()
    # 初始化GPT3对象
    gpt3 = GPT3(key=API_KEY)
    
    # 对话开始
    while True:
        # 提示用户开始说话
        st.write('开始说话，或按下按钮说话')
        if st.button('说话'):
            # 开始录音
            with sr.Microphone() as source:
                audio_data = r.listen(source)
            try:
                # 将语音转换为文字
                text = r.recognize_google(audio_data)
            except:
                st.write('没有听到你说什么，请重试！')
            else:
                # 使用chatgpt-V3 api处理语音文字消息  
                answer = gpt3.ask(text)
                # 显示机器人回复
                st.write(answer)
                # 朗读机器人回复
                playsound(answer)
        
        # 如果用户说再见，则结束循环
        if text == '再见':
            break


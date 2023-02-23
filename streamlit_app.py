import streamlit as st
import requests


@st.cache  # 语音识别 API 将会缓存
def recognize_speech(wav_data):
    url = '9exsX1dSHPQVpdb9Qqbscd4S'
    wav_data = wav_data.read()
    response = requests.post(url, data=wav_data).json()
    return response


# 定义按钮动作
def record_action(btn):
    # 显示录音按钮
    if btn:
        st.audio('''
        data:audio/wav;base64,UklGRjQGAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQQBAAD/////
CAIFAEAcAHqGvgH/AAABAAgAJAUAJwC4Bihm1gH/AwACABEAFQBDACUA8tq3AH/AAA
BAAEACgBXAG8A5QPSMsoA/wMAHwAAAF8ATQCHAMMAjScSAP8ABQAWABQAAQDjAAf/
BwC4Bihm1gH/AwATEgAyAFsAUgHjAO8A+//uAP8AAQATACsAXQCKAMsAmEHM/6QA
/wEAGgBXAFoAWQB3AKoD3P/RAf8AAgB6AGQAfQBOAJYAwSCI/6UAhP8DABYAHgAr
AIEAlADIARIB8v+eA/8ABQA7AEIAZACFAMAApSCu/6sA/wQAHwCAAIEA7AC/ATIB
m/+7Af8ABQA1AGQARgBlAG4A4f+GAP8DAE4AMABqAHoAewC0AONAHv/XAP8ABQAs
AD0ARgBeAKMAiP+lAP8DAQAWACoAVQBzAP4AQ//gAP8AAgA4AEEAdwBOAMkAkf+g
AP8DAE0AHAArAFcAlgDCALX/2QH/AAIAGAAgAHIALwD5AM8Ay/+UAGYAZgBob25n
        ''', format='audio/wav', start_playing=True)
        btn.label = '正在录音...'
        response = recognize_speech(st.file_uploader("", type="audio/wav"))
        st.write('你说：', response['text'])
        btn.label = "开始录音"
        return response['text']


# 主函数
def main():
    btn = st.button("开始录音")
    # 获取录音结果
    st.write("请问有什么可以帮助您？")
    user_input = record_action(btn)

    # 将用户输入拼接到聊天内容末尾
    msg = '你可以说：再见'
    response = user_input

    # 定义停止循环标志
    goodbye = False
    # 开启循环
    while True:
        st.write(msg)
        # 向 chatbot 发送用户输入，获取 chatbot 回答
        response = requests.post('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', data={'text': response}).json()['response']
        st.write(response)

        # 检测用户最后输入是否为再见，如果是的话，停止循环
        if response[-2:] == '再见':
            goodbye = True
            st.write('欢迎下次使用～')

        # 如果用户没有说再见，重新启动循环
        if not goodbye:
            btn = st.button("开始录音")
            # 获取录音结果
            response = record_action(btn)
        else:
            break


if __name__ == '__main__':
    main()

```

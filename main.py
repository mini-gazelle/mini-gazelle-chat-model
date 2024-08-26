import streamlit as st
from langchain.memory import ConversationBufferMemory

from utils import get_chat_response

st.title("💬 Chat_Model", help="他是一个聊天机器人你可以和他聊聊你此时的疑惑")

# 侧边栏
###################################################################################################
with st.sidebar:
    platform = st.selectbox("你要选择哪个平台的大模型？",
                            ["阿里云", "OpenAI"])
    creativity = st.slider("✨ 模型的创造力（数字小说明更严谨，数字大说明更多样）", min_value=0.0,
                           max_value=1.5, value=0.2, step=0.1)
    if platform == "阿里云":
        model = st.radio("请你选择模型：(通义千问)",
                         ["qwen-turbo", "qwen-plus", "qwen-max"])
        openai_api_key = st.text_input("请输入DASHSCOPE_API密钥：", type="password")
        st.markdown("[获取DASHSCOPE_API密钥](https://dashscope.console.aliyun.com/apiKey)")
    elif platform == "OpenAI":
        model = st.radio("请你选择模型：(ChatGPT)",
                         ["gpt-3.5-turbo", "gpt-4o", "gpt-4"])
        openai_api_key = st.text_input("请输入OpenAI API密钥：", type="password")
        st.markdown("[获取OpenAI API密钥](https://api.aigc369.com/register?aff=87kh)")

# 主要框架
###################################################################################################
# 将记忆添加到管理状态当中
if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
    st.session_state["messages"] = [{"role": "ai",
                                     "content": "你好，我是你的AI助手，有什么可以帮你的吗？"}]
# 循环打印管理状态中messages的内容
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])
# 输入框
prompt = st.chat_input()
if prompt:
    if not openai_api_key:
        st.info("请输入你的API Key")
        st.stop()
    st.session_state["messages"].append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)

    with st.spinner("AI正在思考中，请稍等..."):
        response = get_chat_response(prompt, st.session_state["memory"],
                                     openai_api_key, model, platform, creativity)
    msg = {"role": "ai", "content": response}
    st.session_state["messages"].append(msg)
    st.chat_message("ai").write(response)
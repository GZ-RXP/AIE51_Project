import streamlit as st
from streamlit_server_state import server_state, server_state_lock
from pages.util.llmUtil import process_message

role= "assistant"
st.session_state["role"] = role

with server_state_lock["chat_messages"]:
    if "chat_messages" not in server_state:
        server_state["chat_messages"] = []
with server_state_lock["configuration"]:
    if "configuration" not in server_state:
        server_state["configuration"] = {
            "enable_AI_response": False,
            "enable_NER": False,
            "enable_intent_detection": False,
            "enable_report": False
        }

def on_message_input():
    new_message_text = st.session_state["message_input"]
    if not new_message_text:
        return

    new_message_packet = process_message(new_message_text,role)
    # {
    #     "role": role,
    #     "sentence": new_message_text,
    #     "bio_labels": "",
    #     "intent": "",
    # }
    
    with server_state_lock["chat_messages"]:
        server_state["chat_messages"] = server_state["chat_messages"] + [
            new_message_packet
        ]
    st.session_state["message_input"] = ""

def format_messages(messages,enable_NER=False,enable_intent_detection=False):
    formatted_messages = ""
    for message in messages:
        formatted_messages +=f"- {'医生' if message['role']=='assistant' else '患者'}: {message['sentence']}  \n"
        if enable_NER:
            formatted_messages +=f"  - NER   : {message['bio_labels']}  \n"
        if enable_intent_detection:
            formatted_messages +=f"  - intent: {message['intent']}  \n"
    return formatted_messages

# header
st.write("# 欢迎使用智能医疗问诊助手 👋")
st.write("## 您的角色是：医生 👨‍⚕️")
# settings
st.write("#### 当前系统设置")
scol1, scol2,scol3,scol4 = st.columns([1,1,1,1],gap="small", vertical_alignment="bottom")
with scol1:
    enable_AI_response = st.toggle("启用 AI 回复", key="enable_AI_response", value=server_state["configuration"]["enable_AI_response"])
with scol2:
    enable_NER = st.toggle("启用 NER", key="enable_NER", value=server_state["configuration"]["enable_NER"])
with scol3:
    enable_intent_detection = st.toggle("启用意图检测", key="enable_intent_detection", value=server_state["configuration"]["enable_intent_detection"])
with scol4:
    enable_report = st.toggle("启用报告生成", key="enable_report", value=server_state["configuration"]["enable_report"])
# chat history
col1, col2 = st.columns([4,1],gap="small", vertical_alignment="bottom")
with col1:
    st.write("### 对话记录")
with col2:
    st.button("清空",key="clear_messages",on_click=lambda:server_state["chat_messages"].clear())

with st.container(border=True):
    st.write(format_messages( messages= server_state["chat_messages"],enable_NER=enable_NER, enable_intent_detection=enable_intent_detection))
# action area
st.write("### 请输入您的回复")
st.text_input("输入消息", key="message_input", on_change=on_message_input)


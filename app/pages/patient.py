import streamlit as st
from streamlit_server_state import server_state, server_state_lock
from controllers.MessageController import MessageController

if "initialized" not in st.session_state:
    st.switch_page("home.py")

role = "user"
st.session_state["role"] = role

message_controller = MessageController()

enable_AI_response = False
enable_NER = False
enable_norm = False
enable_intent_detection = False
enable_report = False
with server_state_lock["configuration"]:
    print(server_state["configuration"])
    enable_AI_response = server_state["configuration"]["enable_AI_response"]
    enable_NER = server_state["configuration"]["enable_NER"]
    enable_norm = server_state["configuration"]["enable_norm"]
    enable_intent_detection = server_state["configuration"]["enable_intent_detection"]
    enable_report = server_state["configuration"]["enable_report"]

def on_message_input():
    new_message_text = st.session_state["message_input_p"]
    if not new_message_text:
        return

    new_message_packet = message_controller.handle_message(new_message_text,role,enable_NER=enable_NER,enable_norm=enable_norm,enable_intent_detection=enable_intent_detection)

    with server_state_lock["chat_messages"]:
        server_state["chat_messages"] = server_state["chat_messages"] + [
            new_message_packet
        ]
    st.session_state["message_input_p"] = ""
def format_messages(messages):
    formatted_messages = ""
    for message in messages:
        formatted_messages +=f"- {'医生' if message['role']=='assistant' else '患者'}: {message['sentence']}  \n"
    return formatted_messages


st.write("### 欢迎使用智能医疗问诊助手 👋")
st.write("#### 您的角色是：患者 😷")

st.write("#### 对话记录")

with server_state_lock["chat_messages"]:
    with st.container(border=True):
        st.write(format_messages( messages= server_state["chat_messages"]))
    # st.write(server_state["chat_messages"])
    # action area
    if len(server_state["chat_messages"])>0:
        st.text_input("请输入消息", key="message_input_p", on_change=on_message_input)
    else:
        st.text_area("请简要说明您的症状，然后按 Ctrl+Enter 开始对话", key="message_input_p", on_change=on_message_input)


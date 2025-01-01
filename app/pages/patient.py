import streamlit as st
from streamlit_server_state import server_state, server_state_lock
from pages.util.llmUtil import process_message


role = "user"
st.session_state["role"] = role

with server_state_lock["chat_messages"]:
    if "chat_messages" not in server_state:
        server_state["chat_messages"] = []
def on_message_input():
    new_message_text = st.session_state["message_input_p"]
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
    st.session_state["message_input_p"] = ""
def format_messages(messages):
    formatted_messages = ""
    for message in messages:
        formatted_messages +=f"- {'医生' if message['role']=='assistant' else '患者'}: {message['sentence']}  \n"
    return formatted_messages


st.write("# 欢迎使用智能医疗问诊助手 👋")
st.write("## 您的角色是：患者 😷")

st.write("### 对话记录")

with st.container(border=True):
    st.write(format_messages( messages= server_state["chat_messages"]))
    # st.write(server_state["chat_messages"])
st.text_input("Message", key="message_input_p", on_change=on_message_input)


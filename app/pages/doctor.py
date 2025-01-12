import streamlit as st
from streamlit_server_state import server_state, server_state_lock
from controllers.MessageController import MessageController

if "initialized" not in st.session_state:
    st.switch_page("home.py")

role= "assistant"
st.session_state["role"] = role

message_controller = MessageController()

def on_message_input():
    new_message_text = st.session_state["message_input"]
    if not new_message_text:
        return
    
    new_message_packet = message_controller.handle_message(new_message_text,role,enable_NER=enable_NER,enable_norm=enable_norm, enable_intent_detection=enable_intent_detection)
    
    with server_state_lock["chat_messages"]:
        server_state["chat_messages"] = server_state["chat_messages"] + [
            new_message_packet
        ]
    st.session_state["message_input"] = ""

def format_messages(messages,enable_NER=False,enable_norm=False, enable_intent_detection=False):
    formatted_messages = ""
    for message in messages:
        role = '医生' if message['role']=='assistant' else '患者'
        sentence = message['sentence'].replace('\n', '<BR>')
        formatted_messages +=f"- {role}: {sentence}\n"
        if enable_NER:
            formatted_messages +=f"  - NER   : {message['bio_labels']}\n"
        if enable_norm:
            formatted_messages +=f"  - norm  : {message['norm']}\n"
        if enable_intent_detection:
            formatted_messages +=f"  - intent: {message['intent']}\n"
    return formatted_messages


def generate_report():
    if(enable_report and len(server_state["chat_messages"])>0):
        st.write("##### 报告生成中...")
    else:
        st.write("##### 没有对话内容，无法生成报告")

    report = "【病历报告】\n"+message_controller.generate_report(server_state["chat_messages"], enable_report)

    print(report)
    new_message_packet = message_controller.handle_message(report,role,enable_NER=False,enable_norm=False, enable_intent_detection=False)
    with server_state_lock["chat_messages"]:
        server_state["chat_messages"] = server_state["chat_messages"] + [
            new_message_packet
        ]
# header
st.write("### 欢迎使用智能医疗问诊助手 👋")
st.write("#### 您的角色是：医生 👨‍⚕️")
# settings
st.write("#### 当前系统设置")
scol1, scol2,scol3,scol4,scol5 = st.columns([1,1,1,1,1],gap="small", vertical_alignment="bottom")
with scol1:
    enable_AI_response = st.toggle("启用 AI 回复", key="enable_AI_response", value=server_state["configuration"]["enable_AI_response"])
    if(server_state["configuration"]["enable_AI_response"] != enable_AI_response):
        server_state["configuration"]["enable_AI_response"] = enable_AI_response
with scol2:
    enable_NER = st.toggle("启用 NER", key="enable_NER", value=server_state["configuration"]["enable_NER"])
    if(server_state["configuration"]["enable_NER"] != enable_NER):
        server_state["configuration"]["enable_NER"] = enable_NER
with scol3:
    enable_norm = st.toggle("启用Norm", key="enable_norm", value=server_state["configuration"]["enable_norm"])
    if(server_state["configuration"]["enable_norm"] != enable_norm):
        server_state["configuration"]["enable_norm"] = enable_norm
with scol4:
    enable_intent_detection = st.toggle("启用意图检测", key="enable_intent_detection", value=server_state["configuration"]["enable_intent_detection"])
    if(server_state["configuration"]["enable_intent_detection"] != enable_intent_detection):
        server_state["configuration"]["enable_intent_detection"] = enable_intent_detection
with scol5:
    enable_report = st.toggle("启用报告生成", key="enable_report", value=server_state["configuration"]["enable_report"])
    if(server_state["configuration"]["enable_report"] != enable_report):
        server_state["configuration"]["enable_report"] = enable_report



# chat history
col1, col2, col3 = st.columns([7,1,2],gap="small", vertical_alignment="bottom")
with col1:
    st.write("#### 对话记录")
with col2:
    st.button("清空",key="clear_messages",on_click=lambda:server_state["chat_messages"].clear())
with col3:
    if enable_report:
        st.button("生成报告",key="generate_report",on_click=generate_report)

with st.container(border=True,height=500):
    st.markdown(body=format_messages( messages= server_state["chat_messages"],enable_NER=enable_NER, enable_norm=enable_norm,enable_intent_detection=enable_intent_detection),unsafe_allow_html=True)
# action area
if enable_AI_response:
    st.write("#### 当前由智能问诊助手自动回复")
    with server_state_lock["chat_messages"]:
        if len(server_state["chat_messages"])>0 and server_state["chat_messages"][-1]["role"] == "user":
            response = message_controller.get_response(server_state["chat_messages"],enable_ai_response=enable_AI_response)
            new_message_packet = message_controller.handle_message(response,role,enable_NER=enable_NER,enable_norm=enable_norm, enable_intent_detection=enable_intent_detection)
            server_state["chat_messages"] = server_state["chat_messages"] + [
                new_message_packet
            ]
            st.write("##### 等待智能问诊助手回复...")
else:
    st.text_input("请输入消息", key="message_input", on_change=on_message_input)


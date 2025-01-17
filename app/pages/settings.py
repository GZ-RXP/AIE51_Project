import streamlit as st
from streamlit_server_state import server_state, server_state_lock

if "initialized" not in st.session_state:
    st.switch_page("home.py")
#===============================
# Start to render the page
#===============================
st.write("# 欢迎使用智能医疗问诊助手 👋")
st.write("## 系统设置 ⚙️")
enable_AI_response =  st.toggle("启用 AI 回复", key="enable_AI_response", value=server_state["configuration"]["enable_AI_response"])
if(server_state["configuration"]["enable_AI_response"] != enable_AI_response):
    server_state["configuration"]["enable_AI_response"] = enable_AI_response
    st.write("系统设置已保存")
enable_NER = st.toggle("启用 NER", key="enable_NER", value=server_state["configuration"]["enable_NER"])
if(server_state["configuration"]["enable_NER"] != enable_NER):
    server_state["configuration"]["enable_NER"] = enable_NER
    st.write("系统设置已保存")
enable_norm = st.toggle("启用症状判别", key="enable_norm", value=server_state["configuration"]["enable_norm"])
if(server_state["configuration"]["enable_norm"] != enable_norm):
    server_state["configuration"]["enable_norm"] = enable_norm
    st.write("系统设置已保存")
enable_intent_detection = st.toggle("启用意图检测", key="enable_intent_detection", value=server_state["configuration"]["enable_intent_detection"])
if(server_state["configuration"]["enable_intent_detection"] != enable_intent_detection):
    server_state["configuration"]["enable_intent_detection"] = enable_intent_detection
    st.write("系统设置已保存")
enable_report = st.toggle("启用报告生成", key="enable_report", value=server_state["configuration"]["enable_report"])
if(server_state["configuration"]["enable_report"] != enable_report):
    server_state["configuration"]["enable_report"] = enable_report
    st.write("系统设置已保存")
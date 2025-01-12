import streamlit as st
from streamlit_server_state import server_state, server_state_lock


#===============================
#define functions for initialization and configuration
#===============================


def init_configuration():
    with server_state_lock["configuration"]:
        if "configuration" not in server_state:
            print("init configuration")
            server_state["configuration"] = {
                "enable_AI_response": True,
                "enable_NER": True,
                "enable_norm": True,
                "enable_intent_detection": True,
                "enable_report": True
            }
        return server_state["configuration"]
def init_messages():
    with server_state_lock["chat_messages"]:
        if "chat_messages" not in server_state:
            print("init messages")
            server_state["chat_messages"] = []
        return server_state["chat_messages"]
    
#===============================
# start to render the page
#===============================
st.set_page_config(
    page_title="智能医疗问诊助手",
    page_icon="👋",
    layout="wide",
    # menu_items={
    #     '医生': 'pages/doctor.py',
    #     '患者': "pages/patient.py",
    #     '设置': "pages/settings.py"
    # }
)

st.write("# 欢迎使用智能医疗问诊助手 👋")
st.write("## 👈 请从左边选择您的角色")

if "role" in st.session_state:
    if st.session_state["role"] == "user":
        print("Switching to patient page")
        st.switch_page("pages/patient.py")
    elif st.session_state["role"] == "assistant":
        print("Switching to doctor page")
        st.switch_page("pages/doctor.py")
    else:
        print(st.session_state)

if "initialized" not in st.session_state:
    init_messages()
    init_configuration()
    st.session_state["role"] = None
    st.session_state["initialized"] = True
    

import streamlit as st

st.set_page_config(
    page_title="智能医疗问诊助手",
    page_icon="👋",
)

st.write("# 欢迎使用智能医疗问诊助手 👋")
st.write("## 请从左边选择您的角色 👋")

if "role" in st.session_state:
    if st.session_state["role"] == "user":
        print("Switching to patient page")
        st.switch_page("pages/patient.py")
    elif st.session_state["role"] == "assistant":
        print("Switching to doctor page")
        st.switch_page("pages/doctor.py")
    else:
        print(st.session_state)

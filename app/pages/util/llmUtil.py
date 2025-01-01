import streamlit as st
from streamlit_server_state import server_state, server_state_lock

def process_message(user_input,user_role):
    enable_NER = server_state["configuration"]["enable_NER"]
    enable_intent_detection = server_state["configuration"]["enable_intent_detection"]
    new_message_packet = {
        "role": user_role,
        "sentence": user_input,
        "bio_labels": doNER(user_input,enable_NER),
        "intent": doIntentDetection(user_input,enable_intent_detection),
    }
    return new_message_packet
def doNER(text,enbale_NER):
    # if enbale_NER:
    #     raise Exception("NER is not implemented yet")
    return ""

def doIntentDetection(text,enbale_intent_detection):
    # if enbale_intent_detection:
    #     raise Exception("Intent Detection is not implemented yet")
    return ""
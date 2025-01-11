from services.BaseService import BaseService
import streamlit as st
from streamlit_server_state import server_state, server_state_lock
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class NerService(BaseService):
    def __init__(self):
        print(f"Initialized NER Service")
        self.NER_model = self.init_NER()

    
    def init_NER(self):
        base_url = ""
        api_key = ""
        #model = "/gemini/code/Qwen2.5-0.5B-Instruct/"
        model = "Qwen2.5-0.5B-Instruct"
        NER_model = ChatOpenAI(base_url=base_url,
                    api_key=api_key,
                    model=model,
                    # max_tokens=512,
                    # max_completion_tokens = 2048,
                    temperature=0.01,
                    top_p=0.3
                    )
        print("NER model initialized",NER_model)
        sys_prompt = SystemMessagePromptTemplate.from_template(template="""你是一个医疗命名实体专家！请根据当前对话文本内容，识别出每一句话中的BIO实体标签""")
        user_prompt = HumanMessagePromptTemplate.from_template(template="{text}")
        prompt = ChatPromptTemplate.from_messages(messages=[sys_prompt, user_prompt])

        output_parser = StrOutputParser()
        chain = prompt | NER_model | output_parser
        return chain

    def detect_ner(self,text,enbale_NER):
        print("doNER",text,enbale_NER)
        if enbale_NER:
            try:
                response = self.NER_model.invoke(input=[text])
                labels = response.split(" ")[1:]
                inputs = self.split_char(text)
                if len(inputs)>len(labels):
                    labels += ["O"]*(len(inputs)-len(labels))
                if len(inputs)<len(labels):
                    labels = labels[:len(inputs)]
                #return " ".join(labels)
                mapping = {}
                previous_type = ""
                buffer = ""
                for i in range(len(inputs)):
                    if labels[i].startswith("B-") or labels[i]== "O":
                        if(buffer!=""):
                            if previous_type in mapping:
                                mapping[previous_type].append(buffer)
                            else:
                                mapping[previous_type] = [buffer]
                        if labels[i] == "O":
                            buffer = ""
                            previous_type = "O"
                        else:
                            type = labels[i].split("-")[1]
                            buffer += inputs[i]
                            previous_type = type
                    else:
                        buffer += inputs[i]
                if buffer!="":
                    if previous_type in mapping:
                        mapping[previous_type].append(buffer)
                    else:
                        mapping[previous_type] = [buffer]
                print("NER mapping:",mapping)
                return mapping
            except Exception as e:
                print("###Error in NER service", e)
                return "出错了，暂时无法识别实体，请稍后再试。"
        else:
            return ""

    def split_char(self,str):
        english = 'abcdefghijklmnopqrstuvwxyz0123456789'
        output = []
        buffer = ''
        for s in str:
            if s in english or s in english.upper(): #英文或数字
                buffer += s
            else: #中文
                if buffer:
                    output.append(buffer)
                buffer = ''
                output.append(s)
        if buffer:
            output.append(buffer)
        return output
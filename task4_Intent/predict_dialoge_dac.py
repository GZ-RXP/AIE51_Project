from langchain_openai import ChatOpenAI

# 在地址后面加上版本号 /v1
base_url = "http://0.0.0.0:6006/v1"
api_key = "abc123"
model = "DCA_dialogues_0.5B_full1"


# 配置模型连接
model = ChatOpenAI(base_url=base_url,
                  api_key=api_key,
                  model=model,
                  # max_tokens=512,
                  temperature=0.1,
                  top_p=0.3)

from langchain_core.prompts import SystemMessagePromptTemplate
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def predict_by_Langchain(user_input="",model=model):
    """
        请求驱动云的模型进行推理
        得到对应的对话意图label
    """
    sys_prompt= SystemMessagePromptTemplate.from_template(template="""
            你是一个医疗问诊对话意图识别专家。请根据用户输入，识别对话意图
            """)
    user_prompt = HumanMessagePromptTemplate.from_template(template="{text}")
    prompt = ChatPromptTemplate.from_messages(messages=[sys_prompt, user_prompt])
    output_parsers = StrOutputParser()
    chain = prompt | model |output_parsers
    response = chain.invoke(input={"text":user_input})
    return response

if __name__ == '__main__':
    user_input = "患者：今天刚拉肚子"
    response = predict_by_Langchain(user_input=user_input,model=model)
    print(response)
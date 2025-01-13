from langchain_openai import ChatOpenAI
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json

# 在地址后面加上版本号 /v1
base_url = "http://0.0.0.0:6006/v1"
api_key = "abc123"
model = "Qwen2.5-0.5B-Instruct"

# 配置模型连接
model = ChatOpenAI(base_url=base_url,
                  api_key=api_key,
                  model=model,
                  # max_tokens=512,
                  temperature=0.1,
                  top_p=0.3)

def predict_by_Langchain(user_input="",model=model):
    """
        部署 VLLM
        安装 ：pip install vllm
        vllm启动：
            python -m vllm.entrypoints.openai.api_server \
            --host 0.0.0.0 \
            --port 6006 \
            --model Qwen2.5-0.5B-Instruct \
            --api-key abc123 \
            --enable-auto-tool-choice \
            --tool-call-parser hermes
        请求驱动云的模型进行推理得到医患对话，从对话中获取患者症状
    """
    sys_prompt= SystemMessagePromptTemplate.from_template(template="""你是医疗领域症状识别(SR)专家！
    请根据用户输入的医生与患者对话文本内容识别患者的症状类别。
    """)
    #sys_prompt= SystemMessagePromptTemplate.from_template(template="""你是一个有用的肋手！
    #根据用户输入回答。
    #""")
    # 定义user输入 {text} 为变量
    user_prompt = HumanMessagePromptTemplate.from_template(template="{text}")
    prompt = ChatPromptTemplate.from_messages(messages=[sys_prompt, user_prompt])
    output_parsers = StrOutputParser()
    chain = prompt | model |output_parsers
    #response = chain.invoke(input={"text":user_input})
    response_str = chain.invoke(input={"text":user_input})
    data = json.loads(response_str.replace('0','无此症状').replace('1','有此症状').replace('2','无法确定'))
    response = data['symptom']
    return response

if __name__ == '__main__':
    user_input = "那现在咳嗽有痰，加强保暖，多喝水，勤拍背。"
    response = predict_by_Langchain(user_input=user_input,model=model)
    print(response)
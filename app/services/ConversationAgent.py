from services.BaseService import BaseService
from services.ReportGenService import ReportGenService
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from streamlit_server_state import server_state, server_state_lock
from langchain_core.messages import ToolMessage


class ConversationAgent(BaseService):
    def __init__(self):
        print(f"Initialized conversation service")
        self.report_gen_service = ReportGenService()
        self.conversation_model = self.init_conversation()

    

    def init_conversation(self):
        base_url = ""
        api_key = ""
        model_name = "Qwen2.5-7B-Instruct"
        model = ChatOpenAI(base_url=base_url,
                    api_key=api_key,
                    model=model_name,
                    temperature=0.01,
                    top_p=0.3
                    )
        # model_with_tool = model.bind(tools=[generate_report])
        agent_prompt = """你是一个智能医疗诊断助手，请根据用户输入的症状描述，解答用户的问题或给出医学建议，推动对话直至得出医学诊断结论，如果信息不足，请要求用户提供必要的信息。不要重复问同一个问题。如果诊断结果已经得出，请生成病历报告"""
        agent = create_react_agent(model=model, tools=[self.generate_medical_report],state_modifier=agent_prompt)

        # sys_prompt = SystemMessagePromptTemplate.from_template(template="""你是一个智能医疗诊断助手，请根据用户输入的症状描述，解答用户的问题或给出医学建议，推动对话直至得出医学诊断结论，如果信息不足，请要求用户提供必要的信息。不要重复问同一个问题。如果诊断结果已经得出，请生成病历报告""")
        # prompt = ChatPromptTemplate.from_messages(messages=[
        #         sys_prompt, 
        #         MessagesPlaceholder(variable_name="messages")
        #     ]
        # )
        # chain = prompt | agent 
        # return chain
        return agent
    
    def get_response(self, messages, enable_ai_response=False):
        if enable_ai_response:
            try:
                history = ChatMessageHistory()
                for message in messages:
                    if message["role"] == "user":
                        history.add_user_message(message["sentence"])
                    elif message["role"] == "assistant":
                        history.add_ai_message(message["sentence"])
                response = self.conversation_model.invoke(input = {"messages": history.messages})
                print("######## In Conversation Agent: Got Response Message",response["messages"])
                history.clear()
                return response["messages"][-1].content
            except Exception as e:
                print("###Error in conversation service", e)
                return "出错了，暂时无法回答您的问题，请稍后再试。"
        else:
            raise Exception("AI response is disabled")

    def generate_medical_report(self,historical_messages):
        """
        工具描述：用于生成病历报告。
        入参：历史对话记录拼成的string
        出参：返回生成的病历报告,你需要把结果返回给用户
        """
        print("### agent 正在使用工具生成病历报告...###")
        try:
            print("### 尝试生成病历，入参:"+historical_messages)
            report = self.report_gen_service.generate_report_by_agent(historical_messages, enable_report=True)
            print("### agent 生成病历报告结束：",report)
            with server_state_lock["med_report"]:
                if "med_report" not in server_state:
                     server_state["med_report"] = report
            return report
        except Exception as e:
            print("###Error in report generation service", e)
            return "出错了，暂时无法生成病历报告，请稍后再试。"


if __name__ == "__main__":
    conversation_service = ConversationAgent()
    resp = conversation_service.get_response(messages=[    
        {"role": "user", "sentence": "医生，你好！"},
        {"role": "assistant", "sentence": "你好！有什么可以帮助你的吗？"},
        {"role": "user", "sentence": "宝宝拉肚子了，怎么办？"},
        {"role": "assistant", "sentence": "宝宝多大了？拉肚子多久了？"},
        {"role": "user", "sentence": "两个月大，拉了一天了。能够给我诊断结果和病历报告吗？"},
        ], enable_ai_response=True)
    print(resp)


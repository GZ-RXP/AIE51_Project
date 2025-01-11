from services.BaseService import BaseService
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory

class ConversationService(BaseService):
    def __init__(self):
        print(f"Initialized conversation service")
        self.conversation_model = self.init_conversation()
    

    def init_conversation(self):
        base_url = ""
        api_key = ""
        model = "Qwen2.5-7B-Instruct"
        conversation_model = ChatOpenAI(base_url=base_url,
                    api_key=api_key,
                    model=model,
                    # max_tokens=512,
                    # max_completion_tokens = 2048,
                    temperature=0.01,
                    top_p=0.3
                    )
        print("Conversation model initialized",conversation_model)
        sys_prompt = SystemMessagePromptTemplate.from_template(template="""你是一个智能医疗诊断助手，请根据用户输入的症状描述，解答用户的问题或给出医学建议，推动对话直至得出医学诊断结论，如果信息不足，请要求用户提供必要的信息。""")
        prompt = ChatPromptTemplate.from_messages(messages=[
                sys_prompt, 
                MessagesPlaceholder(variable_name="messages")
            ]
        )

        output_parser = StrOutputParser()
        chain = prompt | conversation_model | output_parser
        return chain
    
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
                history.clear()
                return response
            except Exception as e:
                print("###Error in conversation service", e)
                return "出错了，暂时无法回答您的问题，请稍后再试。"
        else:
            raise Exception("AI response is disabled")

if __name__ == "__main__":
    conversation_service = ConversationService()
    resp = conversation_service.get_response(messages=[    
        {"role": "user", "sentence": "医生，你好！"},
        {"role": "assistant", "sentence": "你好！有什么可以帮助你的吗？"},
        {"role": "user", "sentence": "宝宝拉肚子了，怎么办？"},
        {"role": "assistant", "sentence": "宝宝多大了？拉肚子多久了？"},
        {"role": "user", "sentence": "两个月大，拉了一天了。"},
        ], enable_ai_response=True)
    print(resp)


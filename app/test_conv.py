from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory

# 初始化 ChatOpenAI 模型 
base_url = ""
api_key = ""
model = "Qwen2.5-7B-Instruct"
llm = ChatOpenAI(
    base_url=base_url,
    api_key=api_key,
    model=model,
    temperature=0.01,
    top_p=0.3
)

prompt = ChatPromptTemplate.from_messages(
    [
        ( "system", "你是一个有用的助手，请根据对话的历史和用户的输入回答问题",),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = prompt | llm

history = ChatMessageHistory()


while(True):
    message = input("User: ")
    if(message.lower() == "exit"):
        break
    history.add_user_message(message)
    response = chain.invoke({"messages": history.messages})
    history.add_ai_message(response.content)
    print("AI: " + response.content)
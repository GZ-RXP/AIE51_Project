from services.BaseService import BaseService
from langchain_openai import ChatOpenAI
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class ReportGenService(BaseService):
    def __init__(self):
        self.report_model = self.init_report_generation()
        print(f"Initialized report generation service")

    def init_report_generation(self):
        api_key = "EMPTY"
        base_url = ""
        model = "Qwen2.5-0.5B-Instruct_IMCS-MRG_01"
        api_key = ""
        # model = "Qwen2.5-0.5B-Instruct"
        # base_url = "http://direct.virtaicloud.com:47252/v1"
        llm = ChatOpenAI(base_url=base_url,
                    api_key=api_key,
                    model=model,
                    temperature=0.01,
                    top_p=0.3
                    )
        print("Report generation model initialized",llm)
        sys_prompt = SystemMessagePromptTemplate.from_template(template="""你是一个摘要专家！请对用户输入的对话做摘要！请按这个格式输出： 主诉: 现病史: 辅助检查: 既往史: 诊断: 建议:""")
        user_prompt = HumanMessagePromptTemplate.from_template(template="{text}")
        prompt = ChatPromptTemplate.from_messages(messages=[sys_prompt, user_prompt])

        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser
        return chain

    def generate_report(self, messages, enable_report=False):
        print("generate_report in ReportGenService.generate_report")
        if enable_report:
            try:
                text = ""
                for message in messages:
                    text += (message["role"]+":"+message["sentence"] + "\n")
                response = self.report_model.invoke(input = {"text": text})
                return "<table><tr><td>"+response+"</td></tr></table>"
            except Exception as e:
                print("###Error in report generation service:", e)
                return "出错了，暂时无法生成报告，请稍后再试。"
        else:
            return ""
        
    def generate_report_by_agent(self, historical_messages, enable_report=False):
        print("generate_report in ReportGenService.generate_report_by_agent")
        if enable_report:
            try:
                response = self.report_model.invoke(input = {"text": historical_messages})
                return "<table><tr><td>"+response+"</td></tr></table>"
            except Exception as e:
                print("###Error in report generation service:", e)
                return "出错了，暂时无法生成报告，请稍后再试。"
        else:
            return ""

if __name__ == "__main__":
    report_gen_service = ReportGenService()
    report_gen_service.init_report_generation()
    resp = report_gen_service.generate_report(messages=[{"role": "user", "sentence": "医生，你好！"},
                                                 {"role": "assistant", "sentence": "你好！有什么可以帮助你的吗？"},
                                                 {"role": "user", "sentence": "宝宝拉肚子了，怎么办？"},
                                                 {"role": "assistant", "sentence": "宝宝多大了？拉肚子多久了？"},
                                                 {"role": "user", "sentence": "宝宝2岁，拉肚子2天了"},
                                                 {"role": "assistant", "sentence": "建议吃点蒙脱石散，然后观察，注意不要脱水"},
                                                 ], enable_report=True)
    print(resp)
import threading
from services.ConversationService import ConversationService
from services.ConversationAgent import ConversationAgent
# from services.ConversationAgentV2 import get_agent_response,init_conversation
from services.NerService import NerService
from services.ReportGenService  import ReportGenService
from services.IntentDetectService import IntentDetectService
from services.NormService import NormService

class MessageController(object):
    _instance = None # 类属性，用于存储实例
    _lock = threading.Lock()  # 类属性，用于同步访问

    def __new__(cls, *args, **kwargs):

        if not cls._instance:
            with cls._lock:  # 第二次检查，确保只有一个线程创建实例
                if not cls._instance:
                    print(f"Creating new instance for MessageController")
                    instance = super(MessageController, cls).__new__(cls)
                    cls._instance = instance
                    cls._instance.ner_service = NerService()
                    cls._instance.conversation_service = ConversationService()
                    cls._instance.conversation_agent = ConversationAgent()
                    cls._instance.report_gen_service = ReportGenService()
                    cls._instance.intent_detect_service = IntentDetectService()
                    cls._instance.normal_service = NormService()
                else:
                    print(f"Another thread created the instance before acquiring the lock for: MessageController")

        else:
            print(f"Returning existing instance for: MessageController")

        return cls._instance

    def __init__(self):
        super(MessageController, self).__init__()
        print("Initialized with Message Controller")


    def handle_message(self, user_input,user_role,enable_NER=False,enable_norm=False,enable_intent_detection=False,enbale_AI_response=False):
        print("Processing message:",user_role,user_input)
        new_message_packet = {
            "role": user_role,
            "sentence": user_input,
            "bio_labels": self.ner_service.detect_ner(user_input,enable_NER),
            "intent": self.intent_detect_service.detect_intent(user_input,enable_intent_detection),
            "norm": self.normal_service.normalize(text=user_input,role=user_role,enable_norm=enable_norm),
         }
        return new_message_packet
    
    def get_response(self, messages, enable_ai_response=False):
        if enable_ai_response:
            return self.conversation_agent.get_response(messages=messages, enable_ai_response=enable_ai_response)
        else:
            raise Exception("AI Response is disabled")
        
    def generate_report(self, messages, enable_report=False):
        if enable_report:
            return self.report_gen_service.generate_report(messages, enable_report)
        else:
            raise Exception("Report Generation is disabled")


import threading
from services.ConversationService import ConversationService
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
                    cls._instance.report_gen_service = ReportGenService()
                    cls._instance.intent_detect_service = IntentDetectService()
                    cls._instance.normal_service = NormService()
                else:
                    print(f"Another thread created the instance before acquiring the lock for: MessageController")

        else:
            print(f"Returning existing instance for: MessageController")

        return cls._instance

    def __init__(self):
        print(f"Initialized with Message Controller")
        # self.conversation_service = ConversationService()
        # self.ner_service = NerService()
        # self.report_gen_service = ReportGenService()
        # self.intent_detect_service = IntentDetectService()
        # self.normal_service = NormService()

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
            return self.conversation_service.get_response(messages, enable_ai_response)
        else:
            raise Exception("AI Response is disabled")

